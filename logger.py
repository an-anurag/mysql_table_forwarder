# -*- coding: utf-8 -*-
"""
A customised logger for this project for logging to the file and console
Created on 13/08/2020
@author: Anurag
"""

# imports
import os
import logging


class Logger:
    """
    A customized logger for this forwarder
    """

    def __init__(self, filepath):
        """
        Constructor
        :param filepath:
        """
        self.filepath = filepath
        self.logger = logging.getLogger('MYSQL-FORWARDER')
        self.logger.setLevel(logging.DEBUG)
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # file handler
        file_handller = logging.FileHandler(os.path.join(self.filepath))
        file_handller.setLevel(logging.DEBUG)
        file_handller.setFormatter(self._formatter)
        self.logger.addHandler(file_handller)


logger = Logger(os.path.join(os.path.dirname(__file__), 'error.log')).logger