import re

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
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
  #todo dit ook naar een config wegschrijven
  MAX_NAME_LENGTH = 71

  def __init__(self, config, width, height):
    self.config = config
    self.width = width
    self.height = height
    Logger.getLogger(__name__).info('initializing Dyflexis')

  def __str__(self):
    return 'Dyflexis'

  def openChrome(self):
    Logger.getLogger(__name__).info('opening chrome')
    if self.driver == None:
      options = Options()
      options.add_argument("start-maximized")
      self.driver = webdriver.Chrome(options=options)

  def login(self, _progressbarCallback=None):
    Logger.getLogger(__name__).info('starting loggin procedure')

    config = self.config.Config
    self.driver.get(Constants.getDyflexisRoutes("login"))
    WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "username")))

    # wait for page load
    if (config["dyflexis"]["username"] == ""):
      Logger.getLogger(__name__).error('username not set',exc_info=True)
      raise BadLoginException('no username')
    # gebruikersnaam invullen
    self.driver.find_element(by=By.ID, value="username").send_keys(config["dyflexis"]["username"])

    if (config["dyflexis"]["password"] == ""):
      Logger.getLogger(__name__).error('password not set', exc_info=True)
      raise BadLoginException('no password')
    # wachtwoord invullen
    self.driver.find_element(by=By.ID, value="password").send_keys(config["dyflexis"]["password"])
    # knop indrukken en inloggen
    self.driver.find_element(by=By.ID, value="do-login").click()

    try:
      WebDriverWait(self.driver, 6).until(ec.invisibility_of_element_located((By.ID, "username")))
    except TimeoutException as e:
      # de inlog ging niet goed bij dyflexis
      Logger.getLogger(__name__).error('login niet succesvol, ww of username niet goed', exc_info=True)
      raise BadLoginException("De login bij dyflexis was niet succesvol")

    if self.driver.current_url == Constants.getDyflexisRoutes("login"):
      # inlog mis gegaan, fout geven
      Logger.getLogger(__name__).info('logging niet succesvol...')
      return False
    if self.driver.current_url == Constants.getDyflexisRoutes("homepage"):
      Logger.getLogger(__name__).info('logging succesvol')
      return True

  def run(self, _progressbarCallback=None, periods=None):
    if periods is None:
      periods = []

    try:
      self.openChrome()
      self.login()
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
      #word hier niet gelogd omdat het omhoog doorgegooit word
      raise e

    Logger.getLogger(__name__).info('chrome weer sluiten')
    self.driver.quit()
    self.driver = None
    return eventData

  def getRooster(self, _progressbarCallback=None, period=None, baseData=None):
    """
    rooster uitlezen en opslaan als bruikbare data
    :param _progressbarCallback:
    :param period: als None pakken we deze maand
    :param baseData: eventData om te updaten
    :return: eventData
    """
    if baseData is None:
      baseData = {}
    Logger.getLogger(__name__).info('get rooster')
    startProgress = 1
    endProgress = 100

    if _progressbarCallback:
      _progressbarCallback(startProgress,period)

    route = Constants.getDyflexisRoutes('rooster')
    if period is not None:
      route = route + '?periode=' + period
    else:
      period = arrow.get(tzinfo=self.tz).format('YYYY-MM')

    self.driver.get(route)
    WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "main-bar-inner")))
    calendar = self.driver.find_element(by=By.CLASS_NAME, value='calender')

    Logger.getLogger(__name__).info('de maand {} word uitgelezen'.format(period))

    if len(baseData) != 0:
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
      Logger.getLogger(__name__).info('\t\tWeek word uitgelezen')
      columns = row.find_elements(by=By.TAG_NAME, value='td')
      for column in columns:
        Logger.getLogger(__name__).info('\t\t\tKolom word uitgelezen met info:{}\t'.format(column.text[0:2]))

        # als de datum in het verleden ligt lezen we hem niet uit
        startOfMonth = arrow.get(period, tzinfo=self.tz).replace(day=1, hour=0, minute=0, second=0)
        endOfMonth = arrow.get(period, tzinfo=self.tz).shift(months=1, minutes=-1)
        eventDate = arrow.get(column.get_attribute('title'), tzinfo=self.tz)

        if startOfMonth > eventDate or endOfMonth < eventDate:
          Logger.getLogger(__name__).warning('\t\t\t\t skipped: verkeerde periode. periode:{}, eventData: {}'.format(period,eventDate))
          continue

        if not (arrow.get(column.get_attribute('title'), tzinfo=self.tz) >
                arrow.now().replace(hour=0, minute=0).shift(days=-1)):
          Logger.getLogger(__name__).warning('\t\t\t\t skipped: voor vandaag')
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

        # todo, scan ass list for shift en genereer hier al
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
              if len(tuplet) != 0:
                if tuplet[0][1].upper() in event.text.upper():
                  # click event to open info
                  event.click()
                  WebDriverWait(self.driver, 20).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, "div.c-rooster2.a-info")))

                  popup = self.driver.find_element(by=By.CSS_SELECTOR, value="div.c-rooster2.a-info")
                  description = popup.find_elements(by=By.TAG_NAME, value='div')[2].text
                  self.driver.find_element(by=By.CLASS_NAME, value='close-flux').click()
                  WebDriverWait(self.driver, 20).until(
                    ec.invisibility_of_element_located((By.CSS_SELECTOR, "div.c-rooster2.a-info")))

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

    if _progressbarCallback:
      _progressbarCallback(endProgress,period)
    return returnArray

  def elementArrayToIcs(self, elementArray, _progressbarCallback=None):
    Logger.getLogger(__name__).info('elements to array')
    shift = []
    tz = Constants.timeZone

    for dates in elementArray['list']:

      startDate = arrow.get(dates['date'], tzinfo=tz)
      stopDate = arrow.get(dates['date'], tzinfo=tz)
      Logger.getLogger(__name__).info('start verwerking dag: {}'.format(dates['date']))
      if dates['text'] == "":
        continue
        #todo check for null??
      for assignments in dates['assignments']:
        name = None
        description = None
        ##hier is er geen info van het event, mogelijk doordat dit niet goed gegaan is
        if assignments['text'] == "" or assignments['tijd'] == '':
          continue
        ## start date and time ->"10:00 - 17:30"
        start_time = assignments['tijd'][0:5]
        start_hour = start_time[0:2]
        start_minute = start_time[3:5]
        Logger.getLogger(__name__).info('\twith date ' + start_time + " and times " + start_hour + " and sec " + start_minute)

        startDate = startDate.replace(hour=int(start_hour), minute=int(start_minute))
        print("\t" + startDate.format('YYYY-MM-DDTHH:mm:ss'))
        # stop date and time
        stop_time = assignments['tijd'][8:13]
        stop_hour = stop_time[0:2]
        stop_minute = stop_time[3:5]
        stopDate = stopDate.replace(hour=int(stop_hour), minute=int(stop_minute))
        # create name depending on what is in text

        for event in dates['events']:
          tempName,tempDescription = self.eventnameParser(event, assignments)
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

  def eventnameParser(self, event, assignment):
    Logger.getLogger(__name__).info('eventNameParser')
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
      if name is not None and len(name) > self.MAX_NAME_LENGTH:
        name = name[0:self.MAX_NAME_LENGTH] + "..."

    return name,description