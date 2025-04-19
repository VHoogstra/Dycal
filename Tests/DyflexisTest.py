import unittest

from Modules.Dyflexis import Dyflexis


class DyflexisTest(unittest.TestCase):
    def setup(self):
        self.dyflexis = Dyflexis({},3,3)

    def testEventNameParser(self):
        self.setup()

        events=[
                {
                  "id": "event://1725",
                  "text": "Kz ISH Dance Collective - Home",
                  "description": ""
                },
                {
                  "id": "event://1726",
                  "text": "AH Simon Keizer - Ruimte",
                  "description": "Status: Bevestigd\n\n14:30: Aankomst techniek\n20:00: Aanvang\n21:30: Einde\n\nAantal techniek: 3\nAantal verkochte tickets: 214"
                },
                {
                  "id": "event://1724",
                  "text": "ZTR Diner in ZaanTheaterrestaurant",
                  "description": ""
                },
                {
                  "id": "event://1724",
                  "text": "ZTR dinner met AH in de naam want die moet ik niet zien ",
                  "description": ""
                }
              ]
        #eerste twee testen op de tuplet code
        #de derde is voor extra
        #de vierde test ik wat er gebeurt als een waarde van de tuplet in de naam zit
        expectedResults=[
            (None,None),
            ("AH Simon Keizer - Ruimte","=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n14:30: Aankomst techniek\n20:00: Aanvang\n21:30: Einde\n\nAantal techniek: 3\nAantal verkochte tickets: 214"),
            (None,None),
            (None,None)
        ]
        assignments={
                  "id": "assignment://21094",
                  "tijd": "13:00 - 23:00",
                  "text": "Zaandam > 60 Technische Dienst > Grote zaal"
                }
        output =[]
        for event in events:
           output.append(self.dyflexis.eventnameParser(event, assignments))
        for index,expectedResult in enumerate(expectedResults):
            self.assertEqual(output[index], expectedResult)  # add assertion here


if __name__ == '__main__':
    unittest.main()
