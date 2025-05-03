import unittest

import arrow

from Modules.Constants import Constants
from Modules.Google import Google
from Modules.dataClasses import ExportReturnObject, EventDataShift


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
    googleEvents = [googleEvent, googleEvent2]
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
    today = arrow.get(tzinfo=Constants.timeZone)
    start = today.replace(hour=13, minute=00).format("YYYY-MM-DDTHH:mm:ssZ")
    stop = today.replace(hour=23, minute=00).format("YYYY-MM-DDTHH:mm:ssZ")
    period = today.format("YYYY-MM")
    returnObject = ExportReturnObject()
    googleEvents = [
      {
        "description": "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199\nassignment://21237",
        "end": {
          "dateTime": stop,
          "timeZone": "Europe/Amsterdam"
        },
        "id": "oaf039tr0b25bo78ismpftl3cs",
        "start": {
          "dateTime": start,
          "timeZone": "Europe/Amsterdam"
        },
        "summary": "Kz Circus Treurdier - Wendy Pan",
        "updated": "2025-04-16T10:34:48.424Z"
      }
    ]
    periods = [period]

    googleClass = Google()
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(1, len(returnSortRemoval.removeCalendarItem))
    self.assertEqual('Kz Circus Treurdier - Wendy Pan', returnSortRemoval.removeCalendarItem[0]['summary'])

  def test_sort_removal_not_in_period(self):
    """
    er is geen evenement vanuit dyflexis maar wel een evenement in de agenda door ons aangemaakt maar buiten de huidige periode
    :return:
    """
    today = arrow.get(tzinfo=Constants.timeZone)
    start = today.replace(hour=13, minute=00)
    stop = today.replace(hour=23, minute=00)
    period = today.shift(months=-2).format("YYYY-MM")
    returnObject = ExportReturnObject()
    googleEvents = [
      {
        "description": "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199\nassignment://21237",
        "end": {
          "dateTime": stop.format("YYYY-MM-DDTHH:mm:ssZ"),
          "timeZone": "Europe/Amsterdam"
        },
        "id": "oaf039tr0b25bo78ismpftl3cs",
        "start": {
          "dateTime": start.format("YYYY-MM-DDTHH:mm:ssZ"),
          "timeZone": "Europe/Amsterdam"
        },
        "summary": "Kz Circus Treurdier - Wendy Pan",
        "updated": "2025-04-16T10:34:48.424Z"
      }
    ]
    periods = [period]

    googleClass = Google()
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(0, len(returnSortRemoval.removeCalendarItem))

  def test_sort_removal_in_period(self):
    """
    er is geen evenement vanuit dyflexis maar wel een evenement in de agenda door ons aangemaakt en binnen de huidige periode
    :return:
    """
    today = arrow.get(tzinfo=Constants.timeZone).shift(days=1)
    start = today.replace(hour=13, minute=00)
    stop = today.replace(hour=23, minute=00)
    period = today.format("YYYY-MM")
    returnObject = ExportReturnObject()
    googleEvents = [
      {
        "description": "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199\nassignment://21237",
        "end": {
          "dateTime": stop.format("YYYY-MM-DDTHH:mm:ssZ"),
          "timeZone": "Europe/Amsterdam"
        },
        "id": "oaf039tr0b25bo78ismpftl3cs",
        "start": {
          "dateTime": start.format("YYYY-MM-DDTHH:mm:ssZ"),
          "timeZone": "Europe/Amsterdam"
        },
        "summary": "Kz Circus Treurdier - Wendy Pan",
        "updated": "2025-04-16T10:34:48.424Z"
      }
    ]
    periods = [period]

    googleClass = Google()
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(1, len(returnSortRemoval.removeCalendarItem))

    returnObject = ExportReturnObject()
    googleEvents[0]['start']['dateTime'] = arrow.get(tzinfo=Constants.timeZone).shift(days=-1).format(
      "YYYY-MM-DDTHH:mm:ssZ")
    googleEvents[0]['end']['dateTime'] = arrow.get(tzinfo=Constants.timeZone).shift(days=-1).format(
      "YYYY-MM-DDTHH:mm:ssZ")
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(0, len(returnSortRemoval.removeCalendarItem), 'in past')

  def test_sort_removal_personal_event(self):
    """
    een event uit een persoonlijke agenda
    :return:
    """
    today = arrow.get(tzinfo=Constants.timeZone)
    start = today.replace(hour=13, minute=00).format("YYYY-MM-DDTHH:mm:ssZ")
    stop = today.replace(hour=23, minute=00).format("YYYY-MM-DDTHH:mm:ssZ")
    period = today.format("YYYY-MM")
    returnObject = ExportReturnObject()
    googleEvents = [
      {
        "description": "een eigen omschrijving",
        "end": {
          "dateTime": stop,
          "timeZone": "Europe/Amsterdam"
        },
        "id": "oaf039tr0b25bo78ismpftl3cs",
        "start": {
          "dateTime": start,
          "timeZone": "Europe/Amsterdam"
        },
        "summary": "een eigen titel",
        "updated": "2025-04-16T10:34:48.424Z"
      }
    ]
    periods = [period]

    googleClass = Google()
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(0, len(returnSortRemoval.removeCalendarItem))

    googleClass = Google()
    del (googleEvents[0]["description"])
    returnSortRemoval = googleClass.sortRemoval(returnObject, googleEvents, periods)
    self.assertEqual(0, len(returnSortRemoval.removeCalendarItem))

  def test_event_comparison(self):
    """
    test vergelijker google
    :return:
    """
    today = arrow.get(tzinfo=Constants.timeZone)
    start = today.replace(hour=13, minute=00).format("YYYY-MM-DDTHH:mm:ssZ")
    stop = today.replace(hour=23, minute=00).format("YYYY-MM-DDTHH:mm:ssZ")
    description = "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199\nassignment://21237"
    dyfldescription = "=== CODE GENERATED BELOW ===\nStatus: Bevestigd\n\n13:00: Aankomst techniek\n16:00: Aankomst gezelschap\n20:30: Aanvang\n22:25: Einde\n\nAantal techniek: 2\nAantal artiesten: 5\n\nAantal verkochte tickets: 199"
    googleEvent = {
      "description": "\n\n\n\n" + description,
      "end": {
        "dateTime": stop,
        "timeZone": "Europe/Amsterdam"
      },
      "id": "oaf039tr0b25bo78ismpftl3cs",
      "start": {
        "dateTime": start,
        "timeZone": "Europe/Amsterdam"
      },
      "summary": "Kz Circus Treurdier - Wendy Pan",
      "updated": "2025-04-16T10:34:48.424Z"
    }

    dyflexisEvent = EventDataShift()
    dyflexisEvent.title = googleEvent['summary']
    dyflexisEvent.date = googleEvent['start']['dateTime']
    dyflexisEvent.description = dyfldescription
    dyflexisEvent.end_date = googleEvent['end']['dateTime']
    dyflexisEvent.start_date = googleEvent['start']['dateTime']
    dyflexisEvent.id = "assignment://21237"

    googleClass = Google()

    ##all Right
    returnSortRemoval = googleClass.compare_google_event_to_dyflexis(dyflexisEvent, googleEvent)
    self.assertEqual(True, returnSortRemoval, 'all the same')

    ##all start different
    dyflexisEvent.start_date = "2025-04-16T10:34:48.424Z"
    returnSortRemoval = googleClass.compare_google_event_to_dyflexis(dyflexisEvent, googleEvent)
    self.assertEqual(False, returnSortRemoval, 'start different')
    dyflexisEvent.start_date = googleEvent['start']['dateTime']

    ##all end different
    dyflexisEvent.end_date = "2025-04-16T10:34:48.424Z"
    returnSortRemoval = googleClass.compare_google_event_to_dyflexis(dyflexisEvent, googleEvent)
    self.assertEqual(False, returnSortRemoval, 'end different')
    dyflexisEvent.end_date = googleEvent['end']['dateTime']

    ##all description different
    dyflexisEvent.description = "2025-04-16T10:34:48.424Z"
    returnSortRemoval = googleClass.compare_google_event_to_dyflexis(dyflexisEvent, googleEvent)
    self.assertEqual(False, returnSortRemoval, 'description different ')
    dyflexisEvent.description = dyfldescription

    ##all description different
    dyflexisEvent.description = "een eigen tekst voordat het gegenereerde begint" + dyfldescription
    returnSortRemoval = googleClass.compare_google_event_to_dyflexis(dyflexisEvent, googleEvent)
    self.assertEqual(False, returnSortRemoval, 'more text before description')
    dyflexisEvent.description = dyfldescription

    ##all title different
    dyflexisEvent.title = "2025-04-16T10:34:48.424Z"
    returnSortRemoval = googleClass.compare_google_event_to_dyflexis(dyflexisEvent, googleEvent)
    self.assertEqual(False, returnSortRemoval, 'title different')
    dyflexisEvent.title = googleEvent['summary']
