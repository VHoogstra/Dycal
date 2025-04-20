import os
import shutil
import sys
import time
import tkinter
from tkinter import messagebox


class Constants():
  version = "v0.1.0-beta"
  appname = "Dycal"

  zaantheaterColor = "#7a4689"
  dyflexisMessage = "test "
  logPrefix = "logs/"
  logFileName = "log_" + time.strftime("%Y-%m-%d", time.gmtime()) + '.txt'
  dyflexisJsonFilename = 'latestCalendarData.json'
  googleJsonFile = 'latestGoogleMergeData.json'
  userStorageLocation = "dycal"
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
  DESCRIPTION_PREFIX = "=== CODE GENERATED BELOW ==="

  @staticmethod
  def getGoogleCalName():
    return Constants.appname + ": " + Constants.OrganisationName

  @staticmethod
  def getDyflexisRoutes(key,organisation=None,location=None):
    if organisation is None or location is None:
      raise Exception('een Organisatie en Locatie is verplicht!')
    return (Constants.Dyflexis['routes'][key]
            .replace('{organisation}', organisation)
            .replace('{location}', location))

  @staticmethod
  def resource_path(relative):
    """
    :param relative:
    :return:
    """
    # todo test if this works on windows
    base_path = os.path.expanduser('~/'+Constants.userStorageLocation)
    return os.path.join(base_path, relative)


