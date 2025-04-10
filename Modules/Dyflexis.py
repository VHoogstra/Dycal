import re
from pprint import pprint

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import arrow

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from Exceptions.BadLoginException import BadLoginException
from Modules.Constants import Constants
from Modules.Logger import Logger


class Dyflexis:
  tz = "Europe/Amsterdam"
  DESCRIPTION_PREFIX = "=== CODE GENERATED BELOW ==="
  driver = None
  ## locatie zoektermen (shift zoektekst, event zoektekst)
  #todo deze lijst in de config wegzetten
  LOCATION_NAMES = [("Kleine Zaal", 'kz'), ("Grote Zaal", "ah"),('Foyer','foyr')]
  MAX_NAME_LENGTH = 71

  def __init__(self, config, width, height):
    self.config = config
    self.width = width
    self.height = height

  def __str__(self):
    return 'Dyflexis'

  def openChrome(self):
    if self.driver == None:
      options = Options()
      options.add_argument("start-maximized")
      self.driver = webdriver.Chrome(options=options)

  def login(self, _progressbarCallback=None):
    startProgress = 0
    endProgress = 5
    # progressbar 0 through 10
    config = self.config.Config
    self.driver.get(Constants.getDyflexisRoutes("login"))
    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "username")))

    # wait for page load
    if (config["dyflexis"]["username"] == ""):
      raise BadLoginException('no username')
    # gebruikersnaam invullen
    self.driver.find_element(by=By.ID, value="username").send_keys(config["dyflexis"]["username"])

    if (config["dyflexis"]["password"] == ""):
      raise BadLoginException('no password')
    # wachtwoord invullen
    self.driver.find_element(by=By.ID, value="password").send_keys(config["dyflexis"]["password"])
    # knop indrukken en inloggen
    self.driver.find_element(by=By.ID, value="do-login").click()

    try:
      WebDriverWait(self.driver, 6).until(EC.invisibility_of_element_located((By.ID, "username")))
    except TimeoutException as e:
      # de inlog ging niet goed bij dyflexis
      raise BadLoginException("De login bij dyflexis was niet succesvol")

    if self.driver.current_url == Constants.getDyflexisRoutes("login"):
      # inlog mis gegaan, fout geven
      print('er is iets mis gegaan bij het inloggen, zie het scherm')
      return False
    if self.driver.current_url == Constants.getDyflexisRoutes("homepage"):
      print('login succesvol')
      return True

  def run(self, _progressbarCallback=None, periods=[]):
    try:
      self.openChrome()
      logger = Logger()
      # progressbar 0 through 5
      self.login()
      # progressbar 5 through 50
      data = {}
      for period in periods:
        data = self.getRooster(
          _progressbarCallback,
          period=period,
          baseData=data
        )
      # progressbar 75 through 100
      eventData = self.elementArrayToIcs(data, _progressbarCallback)
    except Exception as e:
      self.driver.quit()
      self.driver = None
      raise e

    logger.toFile(location=Constants.logPrefix+ Constants.dyflexisJsonFilename, variable=eventData)
    self.driver.quit()
    self.driver = None
    return eventData

  def getRooster(self, _progressbarCallback=None, period=None, baseData={}):

    config = self.config.Config
    startProgress = 1
    endProgress = 100

    if _progressbarCallback:
      _progressbarCallback(startProgress,period)

    route = Constants.getDyflexisRoutes('rooster')
    if period != None:
      route = route + '?periode=' + period
    else:
      period = arrow.get(tzinfo=self.tz).format('YYYY-MM')

    self.driver.get(route)
    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "main-bar-inner")))
    calendar = self.driver.find_element(by=By.CLASS_NAME, value='calender')

    print('de maand word uitgelezen')

    if (len(baseData) != 0):
      returnArray = baseData
    else:
      returnArray = {
        "assignments": 0,
        "agenda": 0,
        "events": 0,
        "list": []
      }

    body = calendar.find_element(by=By.TAG_NAME, value='tbody')
    rows = body.find_elements(by=By.TAG_NAME, value='tr')

    # het aantal weken gedeelt door het aantal dagen wat we scannen
    progressRowCount = ((endProgress - startProgress) / len(rows))/7

    for row in rows:
      print('regel word uitgelezen')
      columns = row.find_elements(by=By.TAG_NAME, value='td')
      for column in columns:
        print('\tkolom word uitgelezen\t' + column.text[0:2])

        # als de datum in het verleden ligt lezen we hem niet uit
        startOfMonth = arrow.get(period, tzinfo=self.tz).replace(day=1, hour=0, minute=0, second=0)
        endOfMonth = arrow.get(period, tzinfo=self.tz).shift(months=1, minutes=-1)
        eventDate = arrow.get(column.get_attribute('title'), tzinfo=self.tz)

        if startOfMonth > eventDate or endOfMonth < eventDate:
          print('\t\t skipped: wrong month')
          continue

        if not (arrow.get(column.get_attribute('title'), tzinfo=self.tz) >
                arrow.now().replace(hour=0, minute=0).shift(days=-1)):
          print('\t\t skipped: before today')
          continue

        ################ find assignments, aka diensten ################
        assignments = column.find_elements(by=By.CLASS_NAME, value='ass')
        assList = []
        if len(assignments) != 0:
          for assignment in assignments:
            assignmentInnerDiv = assignment.find_element(by=By.TAG_NAME, value='div')
            tijd = assignment.find_element(by=By.TAG_NAME, value='b')

            assList.append({
              "id": assignment.get_attribute('uo'),
              "tijd": tijd.text,
              "text": assignmentInnerDiv.text
            })

        # todo, scan ass list for shift
        ################ find events aka shows in the day ################
        events = column.find_elements(by=By.CLASS_NAME, value='evt')
        eventList = []
        if len(events) != 0:
          for event in events:
            # check if an assignment has this event
            # alleen als het event een assignment heeft klikken we er op, anders is de omschrijving niet boeiend
            description = ""
            for assignement in assList:
              tuplet = [item for item in self.LOCATION_NAMES if
                        item[0].upper() in assignement['text'].upper()]
              if (len(tuplet) != 0):
                if (tuplet[0][1].upper() in event.text.upper()):
                  # click event to open info
                  event.click()
                  WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.c-rooster2.a-info")))

                  popup = self.driver.find_element(by=By.CSS_SELECTOR, value="div.c-rooster2.a-info")
                  description = popup.find_elements(by=By.TAG_NAME, value='div')[2].text
                  self.driver.find_element(by=By.CLASS_NAME, value='close-flux').click()
                  WebDriverWait(self.driver, 20).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.c-rooster2.a-info")))

            eventList.append({
              "id": event.get_attribute('uo'),
              "text": event.text,
              'description': description
            })

        ################ find agenda aka gewerkte uren ################
        agendas = column.find_elements(by=By.CLASS_NAME, value='agen')
        aggList = []
        if len(agendas) != 0:
          for agenda in agendas:
            aggList.append({"id": agenda.get_attribute('uo'), "text": agenda.text})

        returnArray['list'].append(
          {
            "date": column.get_attribute('title'),
            "text": column.text,
            "events": eventList,
            'assignments': assList,
            'agenda': aggList,
          })
        returnArray['events'] = returnArray['events'] + len(eventList)
        returnArray['assignments'] = returnArray['assignments'] + len(assList)
        returnArray['agenda'] = returnArray['agenda'] + len(aggList)

        ##progress for column
        if _progressbarCallback:
          # gedeeld door 7 omdat er 7 dagen in de week zijn
          startProgress = startProgress + (progressRowCount)
          _progressbarCallback(startProgress,period)
      # progress for row
      # if _progressbarCallback:
      #   startProgress = startProgress + progressRowCount
      #   _progressbarCallback(startProgress,period)

    print('done')
    if _progressbarCallback:
      _progressbarCallback(endProgress,period)

    return returnArray

  def elementArrayToIcs(self, elementArray, _progressbarCallback=None):
    # 75 ->100
    startProgress = 75
    endProgress = 100



    print('elementArrayToIcs')
    shift = []
    tz = "Europe/Amsterdam"
    progressRowCount = (endProgress - startProgress) / len(elementArray['list'])

    for dates in elementArray['list']:

      startDate = arrow.get(dates['date'], tzinfo=tz)
      stopDate = arrow.get(dates['date'], tzinfo=tz)
      print(dates['date'])
      if (dates['text'] == ""):
        continue
      for assignments in dates['assignments']:
        name = None
        description = None
        if assignments['text'] == "" or assignments['tijd'] == '':
          continue
        ## start date and time
        start_time = assignments['tijd'][0:5]
        print('\twith date ' + start_time + " and times " + start_time[0:2] + " and sec " + start_time[3:5])

        startDate = startDate.replace(hour=int(start_time[0:2]), minute=int(start_time[3:5]))
        print("\t" + startDate.format('YYYY-MM-DDTHH:mm:ss'))
        # stop date and time
        stop_time = assignments['tijd'][8:13]
        stopDate = stopDate.replace(hour=int(stop_time[0:2]), minute=int(stop_time[3:5]))
        # create name depending on what is in text
        print(" \t" + assignments['text'])

        for event in dates['events']:
          tempName,tempDescription = self.eventNameParser(event,assignments)
          if tempName is not tempDescription is not None:
            name = tempName
            description = tempDescription

        if name is None or description is None:
          ##bij td is de preset Zaandam > 60 Technische Dienst > Grote zaal
          search = [match.start() for match in re.finditer('>', assignments['text'])]
          # get the index from the > and add 1 to it so its not showing
          indexIs = search[len(search) - 1] + 1
          name = assignments['text'][indexIs:].lstrip()
          description = self.DESCRIPTION_PREFIX

        shift.append({
          'date': startDate.format('YYYY-MM-DD'),
          "start_date": startDate.format('YYYY-MM-DDTHH:mm:ssZZ'),  # 20250321T090000Z
          "end_date": stopDate.format('YYYY-MM-DDTHH:mm:ssZZ'),  # 20250321T170000Z
          'title': name,
          'description': description,
          'id': assignments['id']
        })


    elementArray["shift"] = shift
    return elementArray

  def eventNameParser(self,event,assignment):
    # ik moet aan de hand van ass beslissen of ik een naam maak of niet
    description = None
    name =None
    if "GEANNULEERD".upper() in event['text'].upper():
      return name,description
    # look in location names for the shift name
    tuplet = [item for item in self.LOCATION_NAMES if
              item[1].upper() in event['text'][0:5].upper()]
    ### look in the event for the event search
    if len(tuplet) != 0 and tuplet[0][0].upper() in assignment['text'].upper():
      # pak de 2e waarde van de tuplet uit location names
      name = event['text']
      description = self.DESCRIPTION_PREFIX + "\n" + event['description']
      if (name !=None and len(name) > self.MAX_NAME_LENGTH):
        name = name[0:self.MAX_NAME_LENGTH] + "..."

    return name,description