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

  def __str__(self):
    return 'i log important information'

  def log(self, msg):
    with open(Constants.resource_path(self.logPrefix + self.logFileName), 'a+') as fp:
      fp.write("\n")
      fp.write(time.strftime("%Y-%m-%d %H:%M", time.gmtime()))
      fp.write("\t")
      fp.write(msg)
      fp.close()

  @staticmethod
  def toFile(location, variable):
    with open(Constants.resource_path(location), 'w+') as fp:
      fp.write(json.dumps(variable, indent=4))

  @staticmethod
  def getLogger(className):
    logging.root.handlers = []
    logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s - %(name)s - %(levelname)s -\t %(message)s",
      datefmt="%H:%M:%S",
      handlers=[
        logging.FileHandler(Constants.logPrefix + "console_" + Constants.logFileName),
        logging.StreamHandler()
      ]
    )
    return logging.getLogger(className)
