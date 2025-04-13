import io
import json
import logging
import shutil
from pprint import pprint
from tkinter import filedialog

from Modules.Constants import Constants
from Modules.Logger import Logger
import os.path


class ConfigLand:

  def __init__(self, useConfigFile=1):

    self.useConfigFile = useConfigFile
    self.fileName = Constants.resource_path("config.json")
    self.Config = {
      "dyflexis": {"username": "", "password": ""},
      "ics": {"url": ""},
      "google": {"calendarId": None,'credentials':None},
      "autoPopulateConfig": False,
    }

    self.defaultConfig = {
      "dyflexis": {"username": "", "password": ""},
      "ics": {"url": ""},
      "google": {"calendarId": None,'credentials':None},
      "autoPopulateConfig": False,
    }
    self.loadConfig()

  def getKey(self, key):
    if key in self.Config:
      print(type(self.Config[key]))
      return self.Config[key]
    else:
      return self.defaultConfig[key]

  def storeKey(self, key, value):
    self.Config[key] = value
    pprint(value)
    pprint(type(value))
    self.saveConfig()

  def saveConfig(self, localConfig=None):
    # alleen als we de config gebruiken save ik de waarden. anders draaien we in memory
    if (localConfig != None):
      self.Config = localConfig
    with open(self.fileName, 'w') as fp:
      fp.write(json.dumps(self.Config,indent=2))
      fp.close()

  def reset(self):
    self.saveConfig(self.defaultConfig)

  def loadConfig(self):
    if os.path.isfile(self.fileName):
      try:
        with open(self.fileName, 'r') as fp:
          superValue = fp.read()
          self.Config = json.loads(superValue)
          fp.close()
      except:
        Logger().log('config.json is niet json')
        self.saveConfig()
    else:
      self.saveConfig(self.defaultConfig)
      Logger().log('geen config.json gevonden, we maken dit aan')
    return self.Config

  def exportConfig(self):
    target_dir = filedialog.askdirectory(
      title="Locatie om naartoe te exporteren",
      initialdir=os.path.expanduser('~/Downloads'))
    shutil.copyfile(Constants.resource_path("config.json"), target_dir+"/dyflexisConfig.json")

  def importConfig(self):
    targetfile = filedialog.askopenfilename(title="locatie van uw config.json",filetypes=[('Json bestand', 'json')])
    if targetfile is not None:
      with open(targetfile, 'r') as fp:
        content = json.loads(fp.read())
        fp.close()
        self.saveConfig(content)
