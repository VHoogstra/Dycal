import json
import os
import time
import urllib


class Constants():
  version = "v0.1.2-Alpha"
  appname = "Dycal"

  primary_color = "#03969c"
  background_color_primary = '#393534'
  background_color_secondary = "#4a4747"

  dyflexisMessage = "test "
  logPrefix = "logs/"
  logFileName = "log_" + time.strftime("%Y-%m-%d", time.gmtime()) + '.txt'
  dyflexisJsonFilename = 'latestCalendarData.json'
  googleJsonFile = 'latestGoogleMergeData.json'
  userStorageLocation = "dycal"
  githubVersionLink = "https://dycal.vincentvandetechniek.nl/githubtagversion"
  timeZone = "Europe/Amsterdam"
  Dyflexis = {
    "routes": {
      "login": "https://app.planning.nu/{organisation}/login",
      "rooster": "https://app.planning.nu/{organisation}/{location}/rooster2/index2",
      "homepage": "https://app.planning.nu/{organisation}/{location}/"
    }
  }
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
    return gitVersions['data']['name']
