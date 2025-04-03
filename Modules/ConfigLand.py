import io
import json

from Modules.Constants import Constants
from Modules.Logger import Logger
import os.path

class ConfigLand:

    def __init__(self, useConfigFile = 1):
        self.useConfigFile = useConfigFile
        self.fileName = Constants.resource_path("config.json")
        self.Config = {
            "dyflexis": {"username": "", "password": ""},
            "ics": {"url": ""},
            "routes": {
                "loginUrl": "https://app.planning.nu/zaantheater/login",
                "roosterUrl": "https://app.planning.nu/zaantheater/zaandam/rooster2/index2",
                "homepageAfterLogin": "https://app.planning.nu/zaantheater/zaandam/"
            }
        }

    def saveConfig(self, localConfig=None):
        # alleen als we de config gebruiken save ik de waarden. anders draaien we in memory
        if self.useConfigFile == False:
            return True
        if (localConfig != None):
            self.Config = localConfig
        with open(self.fileName, 'w') as fp:
            fp.write(json.dumps(self.Config))
            fp.close()

    def loadConfig(self):
        # alleen als we de config gebruiken return ik de waarden. anders draaien we in memory
        if self.useConfigFile == False:
            return True
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
            self.saveConfig()
            Logger().log('geen config.json gevonden, we maken dit aan')
        return self.Config
