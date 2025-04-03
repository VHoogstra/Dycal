import json
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

  def toFile(self, location, variable):
    with open(Constants.resource_path(location), 'w+') as fp:
      fp.write(json.dumps(variable))
