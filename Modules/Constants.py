import os
import shutil
import sys
import time


class Constants():
  version = "v0.1.0-beta"
  appname = "Dycal"

  zaantheaterColor = "#7a4689"
  dyflexisMessage = "test "
  logPrefix = "logs/"
  logFileName = "log_" + time.strftime("%Y-%m-%d", time.gmtime()) + '.txt'
  dyflexisJsonFilename = 'latestCalendarData.json'
  googleJsonFile = 'latestGoogleMergeData.json'
  githubVersionLink = "https://api.github.com/repos/VHoogstra/dyflexis-calendar-ics/releases"
  timeZone = "Europe/Amsterdam"
  Dyflexis = {
    "routes": {
      "login": "https://app.planning.nu/{organisation}/login",
      "rooster": "https://app.planning.nu/{organisation}/{location}/rooster2/index2",
      "homepage": "https://app.planning.nu/{organisation}/{location}/"
    }
  }
  # todo zaandam ook kiesbaar maken
  OrganisationName = 'zaantheater'
  LocationName = 'zaandam'
  DESCRIPTION_PREFIX = "=== CODE GENERATED BELOW ==="

  @staticmethod
  def getGoogleCalName():
    return Constants.appname +": "+Constants.OrganisationName

  @staticmethod
  def getDyflexisRoutes(key):
    return (Constants.Dyflexis['routes'][key]
            .replace('{organisation}', Constants.OrganisationName)
            .replace('{location}', Constants.LocationName))

  @staticmethod
  def resource_path(relative):
    """
    :param relative:
    :return:
    """
    #todo test if this works on windows
    base_path = os.path.expanduser('~/dycol')
    response = os.path.isdir(base_path)
    if not response:
      os.makedirs(base_path)

    # try:
    #   # PyInstaller creates a temp folder and stores path in _MEIPASS
    #   base_path = sys._MEIPASS
    # except Exception:
    #   base_path = os.path.abspath(".")
    return os.path.join(base_path, relative)

  @staticmethod
  def cleanLogFolder():
    source_dir = Constants.resource_path(Constants.logPrefix)
    if os.path.isdir(source_dir):
      file_names = os.listdir(source_dir)

      for file_name in file_names:
        if Constants.logFileName in file_name or Constants.dyflexisJsonFilename in file_name or Constants.googleJsonFile in file_name:
          continue
        os.remove(source_dir + file_name)
    else:
      os.mkdir(source_dir)