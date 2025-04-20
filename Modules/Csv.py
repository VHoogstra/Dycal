import csv
import re

from Modules.Logger import Logger
from Modules.dataClasses import EventDataList


class Csv():
  def __init__(self):
    pass

  def parseData(self, eventData: EventDataList):
    returnObject = []
    for day in eventData.list:
      date = day['date']
      for agenda in day['agenda']:
        data = returnCsvData(date=date)
        data.id = agenda['id']
        data.info = agenda['text']
        pattern = re.compile(r"\d\d:\d\d\stot\s\d\d:\d\d", re.IGNORECASE)
        searchObject =  pattern.search( agenda['text'])
        if searchObject is not None:
          data.startTime = searchObject.group()[0:5]
          data.stopTime = searchObject.group()[10:15]
        returnObject.append(data)

      for assignment in day['assignments']:
        data = returnCsvData(date=date)
        data.id = assignment['id']
        data.info = assignment['text']
        data.startTime = assignment['tijd'][0:5]
        data.stopTime = assignment['tijd'][8:13]
        returnObject.append(data)

      for event in day['events']:
        data = returnCsvData(date=date)
        data.id = event['id']
        data.name = event['text']
        data.info = event['description']
        # data.startTime = event['tijd'][0:5]
        # data.stopTime = event['tijd'][8:13]
        returnObject.append(data)
    Logger.getLogger(__name__).info('done with parse')
    return returnObject

  def exportToCsv(self,location=None,returnObject=None):
    if location is None or returnObject is None:
      raise Exception('No location or returnObject provided')
    with open(location, 'w', newline='') as f:
      writer = csv.writer(f,delimiter=";")
    #create header with names
      headerRow =[]
      for att in returnCsvData().__dict__:
        if "__" not in att:
          headerRow.append(att)
      writer.writerow(headerRow)

      for object in returnObject:
        newRow = []
        for column in headerRow:
          value =getattr(object,column)
          if value is not None:
            value = value.replace(';',':')
          newRow.append(value)
        writer.writerow(newRow)

    Logger.getLogger(__name__).info('done with export')




class returnCsvData:
  def __init__(self, name=None, info=None, date=None, startTime=None, stopTime=None, type=None,id=None):
    self.name = name
    self.info = info
    self.date = date
    self.startTime = startTime
    self.stopTime = stopTime
    self.type = type
    self.id = id
