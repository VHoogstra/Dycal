import json
import shutil
from pprint import pprint
from tkinter import filedialog
from typing import Any

from Modules.Constants import Constants
from Modules.Logger import Logger
import os.path


class ConfigObject:
  dyflexis = None
  ics = None
  google = None
  autoPopulateConfig = None
  debug = None

  def __init__(self):
    self.__version__ = Constants.version
    self.dyflexis = {"username": "", "password": "","location":"","organisation":""}
    self.ics = {"url": ""}
    self.google = {"calendarId": None, 'credentials': None}
    #todo autopopulate config een checkbox geven in gui
    #encryption op config save en decription
    #config naar user folder verhuizen
    self.autoPopulateConfig = True
    self.debug = {}

  def __getattr__(self, name: str) -> Any:
    return self.__dict__[name]

  def __setattr__(self, name, value):
    # na elke set slaan we op naar de config, zo is die altijd up to date
    self.__dict__[name] = value

  def save(self):
    # alleen als we de config gebruiken save ik de waarden. anders draaien we in memory
    with open(Constants.resource_path("config.json"), 'w') as fp:
      fp.write(self.toJson())
      fp.close()
    return self

  @staticmethod
  def loadFromFile():
    if os.path.isfile(Constants.resource_path("config.json")):
      try:
        with open(Constants.resource_path("config.json"), 'r') as fp:
          superValue = fp.read()
          configObject = ConfigObject.fromJson(superValue)
          fp.close()
          configObject.__version__ = Constants.version
          return configObject

      except:
        Logger.getLogger(__name__).info('config.json is niet json, overschrijf')
        return ConfigObject().save()
    else:
      return ConfigObject().save()

  def toJson(self):
    return json.dumps(
      self,
      default=lambda o: o.__dict__,
      sort_keys=True,
      indent=2)

  @staticmethod
  def fromJson(jsonText):
    """
    load a configuration from json text
    :param jsonText:
    :return:
    """
    config = json.loads(jsonText)
    configObject = ConfigObject()
    # we zetten de keys van de json in onze classe, alles wat niet ingevuld word blijft zo standaard
    for key in config:
      configObject.__setattr__(key, config[key])
    configObject.__version__ = Constants.version
    configObject.save()
    return configObject

class ConfigLand:
  __config: ConfigObject

  def __init__(self):

    self.__config = ConfigObject.loadFromFile()
    self.__updateHandlers = []
    self.__loadHandlers = []

  def addUpdateHandler(self, handler):
    self.__updateHandlers.append(handler)
  def addLoadHandler(self, handler):
    self.__loadHandlers.append(handler)

  def handleUpdateHandlers(self):
    Logger.getLogger(__name__).info('handeling handlers')
    for handler in self.__updateHandlers:
      if handler is not None:
        handler()

  def handleLoadHandlers(self):
      Logger.getLogger(__name__).info('handeling handlers')
      for handler in self.__loadHandlers:
        if handler is not None:
          handler()

  def getKey(self, key):
    return self.__config.__getattr__(key)

  def setKey(self, key, value):
    self.__config.__setattr__(key,value)
    self.__config.save()

  def reset(self):
    self.__config = ConfigObject().save()

  def exportConfig(self):
    self.handleUpdateHandlers()

    target_dir = filedialog.askdirectory(
      title="Locatie om naartoe te exporteren",
      initialdir=os.path.expanduser('~/Downloads'))
    self.__config.save()
    shutil.copyfile(Constants.resource_path("config.json"), target_dir + "/dyflexisConfig.json")

  def importConfig(self):
    targetfile = filedialog.askopenfilename(title="locatie van uw config.json", filetypes=[('Json bestand', 'json')])
    if targetfile is not None and targetfile != "":
      with open(targetfile, 'r') as fp:
        content = fp.read()
        fp.close()
        self.__config = ConfigObject.fromJson(content)
    self.handleLoadHandlers()



