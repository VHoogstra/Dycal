import json
import os
import time
import urllib


class Constants():
  version = "v0.1.1 - Alpha"
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
  encryptionKey = b'Ngi3Iv2_rVNRuMXYhKHy1oVJvUCwm-xq_rTd7GmosXY='
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
  def getDyflexisRoutes(key, organisation=None, location=None):
    if organisation is None or location is None:
      raise Exception('een Organisatie en Locatie is verplicht!')
    return (Constants.Dyflexis['routes'][key].replace('{organisation}', organisation).replace('{location}', location))

  @staticmethod
  def resource_path(relative):
    """
    :param relative:
    :return:
    """
    # todo test if this works on windows
    base_path = os.path.expanduser('~/' + Constants.userStorageLocation)
    return os.path.join(base_path, relative)

  @staticmethod
  def Exception_to_message(exception):
    Message = ""
    if hasattr(exception, 'message'):
      Message = Message + exception.message
    else:
      Message = Message + str(exception)
    return Message

  @staticmethod
  def githubVersion():
    link = Constants.githubVersionLink
    f = urllib.request.urlopen(link)
    gitVersions = json.loads(f.read())
    return gitVersions[0]['name']
