import unittest
from unittest.mock import patch

from Modules.dataClasses import PeriodList, Period


class period_tester(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def testPeriodList(self):
    periodList = PeriodList();
    periodList.addPeriod(Period('2025-01'))
    self.assertEqual(1,len(periodList.getPeriods()))
    self.assertEqual("2025-01",periodList.getPeriods()[0].period)

  def testPeriodGenerate(self):
    periodList = PeriodList()
    with self.assertRaises(Exception) as e:
      periodList.generatePeriods('2025-04', '2025-01')
    with self.assertRaises(Exception) as e:
      periodList.generatePeriods('2026-01', '2025-01')
    with self.assertRaises(Exception) as e:
      periodList.generatePeriods('2030-05', '2025-01')
    with self.assertRaises(Exception) as e:
      periodList.generatePeriods('34', '2025-01')
    with self.assertRaises(Exception) as e:
      periodList.generatePeriods('2025-1', '2024-01')

    periodList.generatePeriods('2024-01', '2025-01')
    self.assertEqual(13, len(periodList.getPeriods()))
    periodList.clearPeriods()
    self.assertEqual(0,len(periodList.getPeriods()))
    periodList.generatePeriods('2024-01', '2025-06')
    self.assertEqual(18, len(periodList.getPeriods()))

  def testPeriodHandler(self):
    periodList = PeriodList()
    with patch.object(periodList, 'callHandler') as mock:
      periodList.generatePeriods('2024-01', '2025-06')
      mock.assert_called()
    with patch.object(periodList, 'callHandler') as mock:
      periodList.clearPeriods()
      mock.assert_called()
    with patch.object(periodList, 'callHandler') as mock:
      periodList.addPeriod(Period('2025-01'))
      mock.assert_called()
    with patch.object(periodList, 'callHandler') as mock:
      periodList.removePeriod(periodList.getPeriods()[0])
      mock.assert_called()

  def testPeriodListFunction(self):
    periodList = PeriodList(6)
    self.assertEqual(6,len(periodList.getPeriods()))

