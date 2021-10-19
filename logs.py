import logging
import datetime
import os
import pathlib


class vmlogs:
    def __init__(self):
        now = datetime.datetime.now()
        self.logPath = os.getcwd()+'\logs\\'
        self.logName = 'vm_logs.log'
        self.logFile = self.logPath+self.logName
        print(self.logFile)
        logging.basicConfig(filename=self.logFile, encoding='utf-8', level=logging.INFO)

    def info_logger(self,content):
        logging.info(content)

    def warning_logger(self,content):
        logging.warning(content)

    def error_logger(self,content):
        logging.error(content)

    def debug_logger(self,content):
        logging.debug(content)

# ins = vmlogs()