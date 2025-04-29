import unittest

from Modules.Dyflexis import Dyflexis


class DyflexisTest(unittest.TestCase):
  def setup(self):
    self.dyflexis = Dyflexis(3, 3)

  def test_event_name_parser(self):
    self.setup()

    events = [
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
    # eerste twee testen op de tuplet code
    # de derde is voor extra
    # de vierde test ik wat er gebeurt als een waarde van de tuplet in de naam zit
    expectedResults = ["AH Simon Keizer - Ruimte",
                       "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n14:30: Aankomst techniek\n20:00: Aanvang\n21:30: Einde\n\nAantal techniek: 3\nAantal verkochte tickets: 214"]

    assignments = {
      "id": "assignment://21094",
      "tijd": "13:00 - 23:00",
      "text": "Zaandam > 60 Technische Dienst > Grote zaal"
    }
    response = self.dyflexis.eventnameParser(events, assignments)
    self.assertEqual(response[0], expectedResults[0])
    self.assertEqual(response[1], expectedResults[1])

  def test_two_events_same_shift(self):
    self.setup()

    events = [
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
        "text": "AH Simon Keizer - Ruimte",
        "description": "tweede bevestigt"
      },
      {
        "id": "event://1724",
        "text": "ZTR dinner met AH in de naam want die moet ik niet zien ",
        "description": ""
      }
    ]
    # eerste twee testen op de tuplet code
    # de derde is voor extra
    # de vierde test ik wat er gebeurt als een waarde van de tuplet in de naam zit
    expectedResults = ["AH Simon Keizer - Ruimte",
                       Dyflexis.DESCRIPTION_PREFIX + "\n" + events[2]['description'] + "\n" + events[1]['description']]

    assignments = {
      "id": "assignment://21094",
      "tijd": "13:00 - 23:00",
      "text": "Zaandam > 60 Technische Dienst > Grote zaal"
    }
    response = self.dyflexis.eventnameParser(events, assignments)
    self.assertEqual(response[0], expectedResults[0])
    self.assertEqual(response[1], expectedResults[1])

  def test_case_wrong(self):
      self.setup()

      events = [
        {
          "description": "",
          "id": "event://1865",
          "text": "GEANNULEERD - Kz Laat me leven - Theater Rast"
        },
        {
          "description": "",
          "id": "event://1866",
          "text": "AH Rob & Emiel - Best of..."
        },
        {
          "description": "",
          "id": "event://1867",
          "text": "ZTR Diner in ZaanTheaterrestaurant"
        }
      ]
      # eerste twee testen op de tuplet code
      # de derde is voor extra
      # de vierde test ik wat er gebeurt als een waarde van de tuplet in de naam zit
      expectedResults = ["AH Rob & Emiel - Best of...",
                         Dyflexis.DESCRIPTION_PREFIX + "\n" + events[1]['description']]

      assignments = {
        "id": "assignment://21635",
        "text": "Zaandam > 60 Technische Dienst > Grote zaal",
        "tijd": "13:00 - 23:00"
      }
      response = self.dyflexis.eventnameParser(events, assignments)
      self.assertEqual(response[0], expectedResults[0])
      self.assertEqual(response[1], expectedResults[1])


if __name__ == '__main__':
  unittest.main()
