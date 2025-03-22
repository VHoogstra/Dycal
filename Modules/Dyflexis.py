from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class Dyflexis:

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config.Config

    def __str__(self):
        return 'Dyflexis'

    def login(self):
        self.driver.get(self.config["routes"]["loginUrl"])
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "username")))

        # wait for page load
        if (self.config["dyflexis"]["username"] == ""):
            self.config["dyflexis"]["username"] = input("Enter username:")
        # gebruikersnaam invullen
        self.driver.find_element(by=By.ID, value="username").send_keys(self.config["dyflexis"]["username"])
        time.sleep(1)

        if (self.config["dyflexis"]["password"] == ""):
            self.config["dyflexis"]["password"] = input("enter password:")
        # wachtwoord invullen
        self.driver.find_element(by=By.ID, value="password").send_keys(self.config["dyflexis"]["password"])

        # knop indrukken en inloggen
        time.sleep(1)
        self.driver.find_element(by=By.ID, value="do-login").click()

        time.sleep(3)

        if (self.driver.current_url == self.config["routes"]["loginUrl"]):
            # inlog mis gegaan, fout geven
            print('er is iets mis gegaan bij het inloggen, zie het scherm')
            password = input("waiting, press enter to cclose")
            return False
        if (self.driver.current_url == self.config["routes"]["homepageAfterLogin"]):
            print('login succesvol')
            return True

    def getRooster(self):
        self.driver.get(self.config["routes"]["roosterUrl"])
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "main-bar-inner")))
        calendar = self.driver.find_element(by=By.CLASS_NAME, value='calender')
        return calendar
        # calendarNextMonthButton = self.calendar.find_element(by=By.TAG_NAME, value='thead').find_elements(by=By.TAG_NAME,
        #                                                                                                  value='a')
        ## bovenstaand gebruiken om de 2 urls te vinden in de eerste th
        # print(calendarNextMonthButton[0].get_attribute('href'))
        # todo get rooster today en next month
        # print(calendarNextMonthButton[1].get_attribute('href'))
        # self.driver.get(calendarNextMonthButton[1].get_attribute('href'))

    def tableElementToArray(self, calendar):
        print('de maand word uitgelezen')
        returnArray = []
        assignmentsCounter = 0
        eventsCounter = 0
        agendaCounter = 0

        body = calendar.find_element(by=By.TAG_NAME, value='tbody')
        rows = body.find_elements(by=By.TAG_NAME, value='tr')

        for row in rows:
            print('regel word uitgelezen')
            columns = row.find_elements(by=By.TAG_NAME, value='td')
            for column in columns:
                print('\tkolom word uitgelezen')

                ## find events aka shows
                events = column.find_elements(by=By.CLASS_NAME, value='evt')
                eventList = []
                if len(events) != 0:
                    for event in events:
                        eventList.append({"id": event.get_attribute('uo'), "text": event.text})

                ## find assignments, aka diensten
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

                ## find agenda aka gewerkte uren
                agendas = column.find_elements(by=By.CLASS_NAME, value='agen')
                aggList = []
                if len(agendas) != 0:
                    for agenda in agendas:
                        aggList.append({"id": agenda.get_attribute('uo'), "text": agenda.text})

                returnArray.append(
                    {
                        "date": column.get_attribute('title'),
                        "text": column.text,
                        "events": eventList,
                        'assignments': assList,
                        'agenda': aggList,
                    })
                eventsCounter = eventsCounter + len(eventList)
                assignmentsCounter = assignmentsCounter + len(assList)
                agendaCounter = agendaCounter + len(aggList)

        print('done')
        return {
            "assignments": assignmentsCounter,
            "agenda": agendaCounter,
            "events": eventsCounter,
            "list": returnArray
        }
