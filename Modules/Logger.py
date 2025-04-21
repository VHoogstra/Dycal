import json
import logging
import os
import time
import collections

from Modules.Constants import Constants


class Logger:
    logPrefix = None
    logFileName = None
    _logger = None
    _tail = None

    def __init__(self):
        self.logPrefix = Constants.logPrefix
        self.logFileName = Constants.logFileName
        path = Constants.resource_path(self.logPrefix)
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def toFile(location, variable, isJson=False):
        with open(Constants.resource_path(location), 'w') as fp:
            if isJson:
                fp.write(variable)
            else:
                fp.write(json.dumps(variable, indent=4))

    @staticmethod
    def getLogger(className):

        logging.root.handlers = []
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt="%H:%M:%S",
            handlers=[
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(className)

        base_path = os.path.expanduser('~/' + Constants.userStorageLocation)
        if os.path.isdir(base_path):
            if not os.path.isdir(base_path + "/logs"):
                os.mkdir(base_path + "/logs")
            test=Constants.resource_path("logs/console_" + Constants.logFileName)
            fileLogger = logging.FileHandler(Constants.resource_path("logs/console_" + Constants.logFileName))
            logger.addHandler(fileLogger)

        tail = TailLogger.getLogger(200)
        log_handler = tail.log_handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt="%H:%M:%S")

        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        Logger._tail = tail
        Logger._logger = logger
        return Logger._logger


class TailLogger(object):
    _self = None
    _handler = []
    @staticmethod
    def getLogger( maxlen):
        if TailLogger._self is None:
            TailLogger._self = TailLogger(maxlen)
        return TailLogger._self

    def __init__(self, maxlen):
        self._log_queue = []
        self._log_handler = TailLogHandler(self._log_queue,self.runHandler)

    def update(self):
        return self.contents
    def contents(self):
        return '\n'.join(self._log_queue)

    @property
    def log_handler(self):
        return self._log_handler
    @staticmethod
    def addHandler(func):
        TailLogger._handler.append(func)

    @staticmethod
    def runHandler():
        for func in TailLogger._handler:
            func()

class TailLogHandler(logging.Handler):

    def __init__(self, log_queue,callback):
        logging.Handler.__init__(self)
        self.log_queue = log_queue
        self.callback = callback

    def emit(self, record):
        self.log_queue.append(self.format(record))
        self.callback()
