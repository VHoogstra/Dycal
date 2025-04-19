import unittest
from pprint import pprint

from Modules.dataClasses import ExportReturnObject
from Modules.Google import Google


class GoogleTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_sort_removal(self):
    returnObject = ExportReturnObject()
    googleEvent = {
      "description": "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199\nassignment://21237",
      "end": {
        "dateTime": "2025-04-16T23:00:00+02:00",
        "timeZone": "Europe/Amsterdam"
      },
      "id": "oaf039tr0b25bo78ismpftl3cs",
      "start": {
        "dateTime": "2025-04-16T13:00:00+02:00",
        "timeZone": "Europe/Amsterdam"
      },
      "summary": "Kz Circus Treurdier - Wendy Pan",
      "updated": "2025-04-16T10:34:48.424Z"
    },
    googleEvent2 = {
      "description": "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199\nassignment://21237",
      "end": {
        "dateTime": "2025-04-16T23:00:00+02:00",
        "timeZone": "Europe/Amsterdam"
      },
      "id": "oaf039tr0b25bo78ismpftl3cs",
      "start": {
        "dateTime": "2025-04-16T13:00:00+02:00",
        "timeZone": "Europe/Amsterdam"
      },
      "summary": "Kz Circus Treurdier - Wendy Pan",
      "updated": "2025-04-16T10:34:48.424Z"
    },
    googleEvents = [googleEvent,googleEvent2]
    returnObject.updateCalendarItem.append(googleEvent)
    returnObject.newCalendarItem.append(googleEvent2)

    periods = ["2025-04", "2025-05", ]

    googleClass = Google()
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(0, len(returnSortRemoval.removeCalendarItem))

  def test_sort_removal_no_exportreturnobject_but_calendar_event(self):
    """
    er is geen evenement vanuit dyflexis maar wel een evenement in de agenda door ons aangemaakt, moet verwijderd
    :return:
    """
    returnObject = ExportReturnObject()
    googleEvents = [
      {
        "description": "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199\nassignment://21237",
        "end": {
          "dateTime": "2025-04-16T23:00:00+02:00",
          "timeZone": "Europe/Amsterdam"
        },
        "id": "oaf039tr0b25bo78ismpftl3cs",
        "start": {
          "dateTime": "2025-04-16T13:00:00+02:00",
          "timeZone": "Europe/Amsterdam"
        },
        "summary": "Kz Circus Treurdier - Wendy Pan",
        "updated": "2025-04-16T10:34:48.424Z"
      }
    ]
    periods = ["2025-04", "2025-05", ]

    googleClass = Google()
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(1, len(returnSortRemoval.removeCalendarItem))
    self.assertEqual('Kz Circus Treurdier - Wendy Pan', returnSortRemoval.removeCalendarItem[0]['summary'])

  def test_sort_removal_not_in_period(self):
    """
    er is geen evenement vanuit dyflexis maar wel een evenement in de agenda door ons aangemaakt maar buiten de huidige periode
    :return:
    """
    returnObject = ExportReturnObject()
    googleEvents = [
      {
        "description": "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199\nassignment://21237",
        "end": {
          "dateTime": "2025-04-16T23:00:00+02:00",
          "timeZone": "Europe/Amsterdam"
        },
        "id": "oaf039tr0b25bo78ismpftl3cs",
        "start": {
          "dateTime": "2025-04-16T13:00:00+02:00",
          "timeZone": "Europe/Amsterdam"
        },
        "summary": "Kz Circus Treurdier - Wendy Pan",
        "updated": "2025-04-16T10:34:48.424Z"
      }
    ]
    periods = ["2025-02"]

    googleClass = Google()
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(0, len(returnSortRemoval.removeCalendarItem))

  def test_sort_removal_in_period(self):
    """
    er is geen evenement vanuit dyflexis maar wel een evenement in de agenda door ons aangemaakt en binnen de huidige periode
    :return:
    """
    returnObject = ExportReturnObject()
    googleEvents = [
      {
        "description": "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199\nassignment://21237",
        "end": {
          "dateTime": "2025-04-16T23:00:00+02:00",
          "timeZone": "Europe/Amsterdam"
        },
        "id": "oaf039tr0b25bo78ismpftl3cs",
        "start": {
          "dateTime": "2025-04-16T13:00:00+02:00",
          "timeZone": "Europe/Amsterdam"
        },
        "summary": "Kz Circus Treurdier - Wendy Pan",
        "updated": "2025-04-16T10:34:48.424Z"
      }
    ]
    periods = ["2025-04"]

    googleClass = Google()
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(1, len(returnSortRemoval.removeCalendarItem))

  def test_sort_removal_personal_event(self):
    """
    een event uit een persoonlijke agenda
    :return:
    """
    returnObject = ExportReturnObject()
    googleEvents = [
      {
        "description": "een eigen omschrijving",
        "end": {
          "dateTime": "2025-04-16T23:00:00+02:00",
          "timeZone": "Europe/Amsterdam"
        },
        "id": "oaf039tr0b25bo78ismpftl3cs",
        "start": {
          "dateTime": "2025-04-16T13:00:00+02:00",
          "timeZone": "Europe/Amsterdam"
        },
        "summary": "een eigen titel",
        "updated": "2025-04-16T10:34:48.424Z"
      }
    ]
    periods = ["2025-04"]

    googleClass = Google()
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(0, len(returnSortRemoval.removeCalendarItem))
