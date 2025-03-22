import requests
import arrow
from ics import Calendar, Event


# https://icspy.readthedocs.io/en/stable/index.html
class ICS:
    calendar = None

    def connectToICS(self, url=None, file=None):
        content = None
        if (url is not None):
            content = requests.get(url).text

        if (file is not None):
            with open(file, 'r') as fp:
                content = fp.read()

        if content == None:
            return;

        self.calendar = Calendar(content)
        print("calendar connectToICS event lengths " + str(len(self.calendar.events)))
        # c.events # lijst met evenementen in de dingus, kan ik met een map/foreach op filteren? indexen?
        # eventondate = self.isEventOnDate('2025-03-23')

    def createNewEvent(self,dyflexysEvent):
        #ik map nu hier alle info... ergens heb ik het hele dag object nog nodig om te bepalen welke data ik in de url plaats....
        name = ''
        description = ''
        if "Kleine Zaal" in dyflexysEvent.text:
            name = "KZ"
        elif "Grote Zaal" in dyflexysEvent.text:
            name = "AH"
            #TODO HIER MOET DE SHOW NAAM NOG ACHTER
        else:
            name = dyflexysEvent.text[33:]

        #todo dyflexis tekst willen we eigenlijk ook in de omschrijving hebben
        ##todo wat als je meer items per dag hebt, dat ook verwerken? hoe?
        event = Event()
        event.name = "ZT: "+name
        event.description = description +"\n\n\n "+event.id

    def isEventOnDate(self, date):
        eventOnDate = self.calendar.timeline.on(arrow.get(date))

        for event in eventOnDate:
            # print(event)
            print(event.name)
            if "id" in event.description:
                print( 'id is in description ')
        print(eventondate.__sizeof__())

    def generateToICS(self):
        with open('my.ics', 'w') as fp:
            fp.writelines(self.calendar.serialize_iter())
