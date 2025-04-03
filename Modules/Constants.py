import os
import shutil
import sys
import time


class Constants():
  zaantheaterColor = "#7a4689"
  dyflexisMessage = "test "
  logPrefix = "logs/"
  logFileName = "log_" + time.strftime("%Y-%m-%d", time.gmtime()) + '.txt'
  dyflexisJsonFilename='latestCalendarData.json'

  def resource_path(relative):
    try:
      # PyInstaller creates a temp folder and stores path in _MEIPASS
      base_path = sys._MEIPASS
    except Exception:
      base_path = os.path.abspath(".")

    return os.path.join(base_path, relative)

  @staticmethod
  def cleanLogFolder():
    print("Cleaning Log Folder")
    source_dir = Constants.resource_path(Constants.logPrefix)
    file_names = os.listdir(source_dir)

    for file_name in file_names:
      if Constants.logFileName in file_name or Constants.dyflexisJsonFilename in file_name:
        continue
      os.remove(source_dir+file_name)
