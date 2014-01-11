import logging
import logging.handlers
import subprocess
import sys
import os

class SILogging(object):

    def __init__(self,
                log_filename='/var/log/si_server/actions.log'):

        self.logger = logging.getLogger('Tema2SI_WebServer_Logger')
        self.filename = log_filename
        self.handler = None
    
        #This is a default filename. If directory does not
        #exist we will'
        directory = os.path.dirname(log_filename)
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

        #This if is because Python is, honestly, stupid!
        if not len(self.logger.handlers):
            self.logger.setLevel(logging.DEBUG)
            fmt = logging.Formatter("[%(asctime)s] %(name)s : %(levelname)s : %(message)s")

            # Add the log message handler to the logger
            # Using python's logrotation
            self.handler = logging.handlers.RotatingFileHandler(log_filename, mode='a',
                                                            maxBytes=1000000,
                                                            backupCount=5)
            self.handler.setFormatter(fmt)
            self.logger.addHandler(self.handler)

    def log(self, level, message):
        if(level == "info"):
            self.logger.info(message)
        elif(level == "debug"):
            self.logger.debug(message)

    def changeFilename(self, new_filename):

        if(self.handler != None):
            self.handler.close()
            self.logger.removeHandler(self.handler)

        directory = os.path.dirname(new_filename)
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

        self.filename = new_filename

        self.handler = logging.handlers.RotatingFileHandler(new_filename, mode='a',
                                                        maxBytes=1000000,
                                                        backupCount=5)
        fmt = logging.Formatter("[%(asctime)s] %(name)s : %(levelname)s : %(message)s")
        self.handler.setFormatter(fmt)
        self.logger.addHandler(self.handler)
