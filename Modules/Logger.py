import json
import logging
import os
import time

from Modules.Constants import Constants


class Logger:
  logPrefix = None
  logFileName = None

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
      format="%(asctime)s - %(name)s - %(levelname)s -\t %(message)s",
      datefmt="%H:%M:%S",
      handlers=[
        logging.StreamHandler()
      ]
    )
    logger = logging.getLogger(className)
    base_path = os.path.expanduser('~/' + Constants.userStorageLocation)
    if  os.path.isdir(base_path):
      if not os.path.isdir(base_path+"/logs"):
        os.mkdir(base_path+"/logs")
      fileLogger = logging.FileHandler(Constants.resource_path("logs/console_" + Constants.logFileName))
      logger.addHandler(fileLogger)

    return logger
