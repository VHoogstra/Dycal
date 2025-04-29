import re

import arrow
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from Exceptions.BadLoginException import BadLoginException
from Modules.ConfigLand import ConfigLand
from Modules.Constants import Constants
from Modules.Logger import Logger
from Modules.dataClasses import EventDataObject, Period, EventDataList, EventDataShift, CustomTime


class Dyflexis:
  tz = "Europe/Amsterdam"
  DESCRIPTION_PREFIX = "=== CODE GENERATED BELOW ==="
  driver = None
  ## locatie zoektermen (shift zoektekst, event zoektekst)
  # todo deze lijst in de config wegzetten
  LOCATION_NAMES = [("Kleine Zaal", 'kz'), ("Grote Zaal", "ah"), ('Foyer', 'foyr')]
  # todo dit ook naar een config wegschrijven
  MAX_NAME_LENGTH = 71

  def __init__(self, width, height):
    self.config = ConfigLand.getConfigLand()
    self.width = width
    self.height = height
    tempConfig = self.config.getKey('dyflexis')
    self.username = tempConfig['username']
    self.password = tempConfig['password']
    self.location = tempConfig['location']
    self.organisation = tempConfig['organisation']

    Logger.getLogger(__name__).info('initializing Dyflexis')

  def __str__(self):
    return 'Dyflexis'

  def openChrome(self):
    Logger.getLogger(__name__).info('opening chrome')
    if self.driver == None:
      options = Options()
      options.add_argument("start-maximized")
      self.driver = webdriver.Chrome(options=options)

  def login(self):
    Logger.getLogger(__name__).info('starting loggin procedure')

    self.driver.get(Constants.getDyflexisRoutes("login", organisation=self.organisation, location=self.location))
    WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.ID, "username")))

    # wait for page load
    if (self.username == ""):
      Logger.getLogger(__name__).error('self.username not set', exc_info=True)
      raise BadLoginException('no self.username')
    # gebruikersnaam invullen
    self.driver.find_element(by=By.ID, value="username").send_keys(self.username)

    if (self.password == ""):
      Logger.getLogger(__name__).error('password not set', exc_info=True)
      raise BadLoginException('no password')
    # wachtwoord invullen
    self.driver.find_element(by=By.ID, value="password").send_keys(self.password)
    # knop indrukken en inloggen
    self.driver.find_element(by=By.ID, value="do-login").click()

    try:
      WebDriverWait(self.driver, 6).until(ec.invisibility_of_element_located((By.ID, "username")))
    except TimeoutException as e:
      # de inlog ging niet goed bij dyflexis
      Logger.getLogger(__name__).error('login niet succesvol, ww of username niet goed', exc_info=True)
      raise BadLoginException("De login bij dyflexis was niet succesvol")

    if self.driver.current_url == Constants.getDyflexisRoutes("login", organisation=self.organisation,
                                                              location=self.location):
      # inlog mis gegaan, fout geven
      Logger.getLogger(__name__).info('logging niet succesvol...')
      return False

    postLoginRoute = self.driver.current_url
    route = Constants.getDyflexisRoutes('homepage', organisation=self.organisation, location=self.location)
    if not postLoginRoute in route:
      value = [m.start() for m in re.finditer('/', postLoginRoute)]
      lastSlash = value[len(value) - 1]
      secondLastSlash = value[len(value) - 2]
      locationName = postLoginRoute[secondLastSlash + 1:lastSlash]
      raise Exception(
        'locatie komt niet overeen met de locatie na login bij dyflexis namelijk: "{}"'.format(locationName))
    return True

  def run(self, periods=None):
    if periods is None:
      periods = []
    try:
      self.openChrome()
      self.login()
      eventData = EventDataObject()
      for period in periods:
        data = self.getRooster(
          period=period,
          baseData=eventData
        )
      # progressbar 75 through 100
    except Exception as e:
      self.driver.quit()
      self.driver = None
      # word hier niet gelogd omdat het omhoog doorgegooit word
      raise e

    Logger.getLogger(__name__).info('chrome weer sluiten')
    self.driver.quit()
    self.driver = None
    return eventData

  def getRooster(self, period=None, baseData: EventDataObject = None):
    """
    rooster uitlezen en opslaan als bruikbare data
    :param period: als None pakken we deze maand
    :param baseData: eventData om te updaten
    :return: eventData
    """
    if baseData is None:
      baseData = EventDataObject()
    Logger.getLogger(__name__).info('get rooster')
    startProgress = 1
    endProgress = 100

    route = Constants.getDyflexisRoutes('rooster', organisation=self.organisation, location=self.location)
    if period is None:
      period = Period(arrow.get(tzinfo=self.tz).format('YYYY-MM'))
    route = route + '?periode=' + period.period

    period.updateProgressBar(startProgress)

    self.driver.get(route)
    WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "main-bar-inner")))
    calendar = self.driver.find_element(by=By.CLASS_NAME, value='calender')

    Logger.getLogger(__name__).info('de maand {} word uitgelezen'.format(period.period))

    baseData.periods.append(period.period)
    body = calendar.find_element(by=By.TAG_NAME, value='tbody')
    rows = body.find_elements(by=By.TAG_NAME, value='tr')

    # het aantal weken gedeelt door het aantal dagen wat we scannen
    progressRowCount = ((endProgress - startProgress) / len(rows)) / 7

    for row in rows:
      Logger.getLogger(__name__).info('\t\tWeek word uitgelezen')
      columns = row.find_elements(by=By.TAG_NAME, value='td')
      for column in columns:
        eventDataList = EventDataList()
        eventDataList.date = column.get_attribute('title')
        eventDataList.text = column.text

        Logger.getLogger(__name__).info('\t\t\tKolom word uitgelezen met info:{}\t'.format(column.text[0:2]))

        # als de datum in het verleden ligt lezen we hem niet uit
        if self.check_is_current_month(period, column.get_attribute('title')):
          Logger.getLogger(__name__).warning(
            '\t\t\t\t skipped: verkeerde periode. periode:{}, eventData: {}'.format(period.period,
                                                                                    column.get_attribute('title')))
          continue
        ################ find assignments, aka diensten ################
        # dit moet na events omdat we meteen de shifts genereren
        eventDataList = self.create_assignment_list(column.find_elements(by=By.CLASS_NAME, value='ass'),
                                                    eventDataList)

        ################ find events aka shows in the day ################
        eventDataList = self.create_events_list(column.find_elements(by=By.CLASS_NAME, value='evt'), eventDataList)

        ################ find agenda aka gewerkte uren ################
        eventDataList = self.create_agenda_list(column.find_elements(by=By.CLASS_NAME, value='agen'), eventDataList)

        if len(eventDataList.assignments) > 0:
          for assignment in eventDataList.assignments:
            eventDataShift = EventDataShift()
            eventDataShift.date = arrow.get(eventDataList.date, tzinfo=Constants.timeZone).format('YYYY-MM-DD')
            eventDataShift.id = assignment['id']

            date = arrow.get(eventDataList.date, tzinfo=Constants.timeZone)
            isBeforeToday = not date > arrow.now().replace(hour=0, minute=0).shift(days=-1)
            if isBeforeToday or assignment['text'] == "":
              continue

            startTime = CustomTime.stringToText(assignment['tijd'][0:5])
            startDate = arrow.get(eventDataList.date, tzinfo=Constants.timeZone).replace(hour=startTime.hour,
                                                                                         minute=startTime.minute).format(
              'YYYY-MM-DDTHH:mm:ss')
            eventDataShift.start_date = startDate
            stopTime = CustomTime.stringToText(assignment['tijd'][8:13])
            stopDateTime = arrow.get(eventDataList.date, tzinfo=Constants.timeZone).replace(hour=stopTime.hour,
                                                                                            minute=stopTime.minute).format(
              'YYYY-MM-DDTHH:mm:ss')
            name, description = self.eventnameParser(eventDataList.events, assignment)
            if name is None or description is None:
              ##bij td is de preset Zaandam > 60 Technische Dienst > Grote zaal
              search = [match.start() for match in re.finditer('>', assignment['text'])]
              # get the index from the > and add 1 to it so its not showing
              indexIs = search[len(search) - 1] + 1
              name = assignment['text'][indexIs:].lstrip()
              description = self.DESCRIPTION_PREFIX

            eventDataShift.end_date = stopDateTime
            eventDataShift.title = name
            eventDataShift.description = description
            baseData.shift.append(eventDataShift)

        baseData.list.append(eventDataList)

        baseData.events = baseData.events + len(eventDataList.events)
        baseData.assignments = baseData.assignments + len(eventDataList.assignments)
        baseData.agenda = baseData.agenda + len(eventDataList.agenda)

        startProgress = startProgress + (progressRowCount)
        period.updateProgressBar(startProgress)

    period.updateProgressBar(endProgress)
    return baseData

  def create_agenda_list(self, agendaDyflexis, eventDataList: EventDataList):
    if len(agendaDyflexis) != 0:
      for agenda in agendaDyflexis:
        eventDataList.agenda.append({"id": agenda.get_attribute('uo'), "text": agenda.text})
    return eventDataList

  def checkLocationNames(self,assignment,event):
    tuplet = [item for item in self.LOCATION_NAMES if
              item[1].upper() in event[0:len(item[1]) + 2].upper()]
    ### look in the event for the event search
    if len(tuplet) != 0 and tuplet[0][0].upper() in assignment.upper():
      return True
    return False


  def create_events_list(self, eventsDyflexis, eventDataList: EventDataList):
    if len(eventsDyflexis) != 0:
      for event in eventsDyflexis:
        # check if an assignment has this event
        # alleen als het event een assignment heeft klikken we er op, anders is de omschrijving niet boeiend
        description = ""
        for assignement in eventDataList.assignments:
          #check if ass matches search query, if yes, click the event. else move along
            if self.checkLocationNames(assignement['text'],event.text):
              # click event to open info
              event.click()
              WebDriverWait(self.driver, 20).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, "div.c-rooster2.a-info")))

              popup = self.driver.find_element(by=By.CSS_SELECTOR, value="div.c-rooster2.a-info")
              description = popup.find_elements(by=By.TAG_NAME, value='div')[2].text
              self.driver.find_element(by=By.CLASS_NAME, value='close-flux').click()
              WebDriverWait(self.driver, 20).until(
                ec.invisibility_of_element_located((By.CSS_SELECTOR, "div.c-rooster2.a-info")))
        eventDataList.events.append({
          "id": event.get_attribute('uo'),
          "text": event.text,
          'description': description
        })
    return eventDataList

  def check_is_current_month(self, period: Period, eventDate):
    start_of_month = arrow.get(period.period, tzinfo=self.tz).replace(day=1, hour=0, minute=0, second=0)
    end_of_month = arrow.get(period.period, tzinfo=self.tz).shift(months=1, minutes=-1)
    event_date = arrow.get(eventDate, tzinfo=self.tz)
    return start_of_month > event_date or end_of_month < event_date

  def create_assignment_list(self, assignmentsDyflexis, eventDataList: EventDataList):
    if len(assignmentsDyflexis) != 0:
      for assignment in assignmentsDyflexis:
        assignmentInnerDiv = assignment.find_element(by=By.TAG_NAME, value='div')
        tijd = assignment.find_element(by=By.TAG_NAME, value='b')

        eventDataList.assignments.append({
          "id": assignment.get_attribute('uo'),
          "tijd": tijd.text,
          "text": assignmentInnerDiv.text
        })
    return eventDataList

  def eventnameParser(self, events, assignment):
    description = None
    name = None

    for event in events:
      # look in location names for the shift name
      ### look in the event for the event search
      if self.checkLocationNames(assignment['text'],event['text']):
        # pak de 2e waarde van de tuplet uit location names
        name = event['text']

        if description is not None:
          description = event['description'] + "\n" + description
        else:
          description = event['description']
        if name is not None and len(name) > self.MAX_NAME_LENGTH:
          name = name[0:self.MAX_NAME_LENGTH] + "..."

    if description is not None:
      description = "\n"+self.DESCRIPTION_PREFIX + "\n" + description
    return name, description
