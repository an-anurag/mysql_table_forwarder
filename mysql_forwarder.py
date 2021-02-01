
import socket
import datetime

import pytz

from config_reader import config
from query import query
from logger import logger
try:
    from mysql.connector import connect
except ModuleNotFoundError as err:
    logger.error(err)


class MySQLForwarder:
    """
    Get mysql table records and sends logs to syslog
    Below _LOG needs to be modified according to sql query specified in query.py
    """

    _QUERY = query

    _LOG = '''
        timestamp: {}, backlog_id: {}, event_id: {}, corr_engine_ctx: {}, status: {}, plugin_id: {}, plugin_sid: {}, 
        protocol: {}, src_ip: {}, dst_ip: {}, src_port: {}, dst_port: {}, risk: {}, efr: {}, username: {}, source: {},
        similar: {}, removable: {}, in_file: {} csimilar: {}, kid: {}, kingdom: {}, category: {}, subcategory: {}, 
        label: {}, plugin1: {}, plugin_sid1: {}, asset_risk_score: {}, asset_os: {}, tenant_id, {}, asset_cpu: {}, 
        asset_workgroup: {}, asset_memory: {}, asset_department: {}, asset_state: {}, asset_username: {}, 
        asset_acl: {}, asset_route: {}, asset_storage: {}, asset_role: {}, asset_video: {}, asset_model: {}, sensor_ip: {}
        '''

    def __init__(self):
        self.tz = pytz.timezone(config.read('time', 'timezone'))
        self._user = config.read('mysql', 'user')
        self._password = config.read('mysql', 'password')
        self._host = config.read('mysql', 'host')
        self._database = config.read('mysql', 'db')
        self._conn = None
        self._connected = False
        # socket conf
        self._soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._logger_host = config.read('logger-input', 'host')
        self._logger_port = int(config.read('logger-input', 'port'))
        self.mins = int(config.read('other', 'mins_to_look_back'))

    def connect(self):
        """
        Method to connect with MySQL database
        :return: connection object
        """
        try:
            self._conn = connect(host=self._host, database=self._database, user=self._user, password=self._password,
                                 use_pure=False)
            self._conn.autocommit = True
            self._connected = True
        except Exception as e:
            logger.error("Can't connect to database (%s@%s) error: %s" % (self._user, self._host, e))
        return self._conn

    def send_to_logger(self, line):
        """
        Forwards given log to UDP socket
        """
        self._soc.sendto(bytes(line, encoding='utf-8'), (self._logger_host, self._logger_port))

    @staticmethod
    def to_timezone(timestamp, timezone):
        """
        Converts given datetime object to time for given timezone
        formats: "%Y-%m-%d %H:%M:%S"
        """
        # Convert it to an aware datetime object in UTC time.
        d = timestamp.replace(tzinfo=pytz.utc)
        # Convert it to your local timezone (still aware)
        d = d.astimezone(timezone)
        return d.strftime("%Y-%m-%d %H:%M:%S")

    def forward(self):
        """
        Fetch and forward logs to logger
        """
        alarm_store = []

        try:
            # create cursor
            cursor = self._conn.cursor()
            # get current time according to given timezone
            tz_now = self.tz.localize(datetime.datetime.now())
            # get past time according to given minutes
            past = tz_now - datetime.timedelta(minutes=self.mins)
            # convert past time to utc
            utc_past = past.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
            # query db with UTC past time
            cursor.execute(self._QUERY.format(utc_past))
            # print([al for al in cursor.fetchall()])
            alarm_store.append(cursor.fetchall())

            if alarm_store[0]:
                # iterate over results and process it one by one
                for alarm in alarm_store[0]:

                    log = self._LOG.format(
                        self.to_timezone(alarm[0], self.tz), alarm[1], alarm[2], alarm[3], alarm[4], alarm[5],
                        alarm[6], alarm[7], alarm[8], alarm[9], alarm[10], alarm[11], alarm[12], alarm[13],
                        alarm[14], alarm[15], alarm[16], alarm[17], alarm[18], alarm[19], alarm[20], alarm[21],
                        alarm[22], alarm[23], alarm[24], alarm[25], alarm[26], alarm[27], alarm[28], alarm[29],
                        alarm[30], alarm[31], alarm[32], alarm[33], alarm[34], alarm[35], alarm[36], alarm[37],
                        alarm[38], alarm[39], alarm[40], alarm[41], alarm[42]
                    ).replace('\n', ' ').replace('  ', '')
                    # send to logger
                    self.send_to_logger(line=log)
                    print(log)
            else:
                print("No records found")

            # flush alarm store
            alarm_store.clear()

            # finally close cursor
            cursor.close()

        except Exception as error:
            logger.error(error)
