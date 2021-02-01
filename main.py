from mysql_forwarder import MySQLForwarder


if __name__ == '__main__':

    sql = MySQLForwarder()

    if sql.connect():
        sql.forward()
