import unittest

from streamlink.utils.times import hours_minutes_seconds


class TestUtilsTimes(unittest.TestCase):

    def test_hours_minutes_seconds(self):
        self.assertEqual(hours_minutes_seconds("00:01:30"), 90)
        self.assertEqual(hours_minutes_seconds("01:20:15"), 4815)
        self.assertEqual(hours_minutes_seconds("26:00:00"), 93600)

        self.assertEqual(hours_minutes_seconds("07"), 7)
        self.assertEqual(hours_minutes_seconds("444"), 444)
        self.assertEqual(hours_minutes_seconds("8888"), 8888)

        self.assertEqual(hours_minutes_seconds("01h"), 3600)
        self.assertEqual(hours_minutes_seconds("01h22m33s"), 4953)
        self.assertEqual(hours_minutes_seconds("01H22M37S"), 4957)
        self.assertEqual(hours_minutes_seconds("01h30s"), 3630)
        self.assertEqual(hours_minutes_seconds("1m33s"), 93)
        self.assertEqual(hours_minutes_seconds("55s"), 55)

        self.assertEqual(hours_minutes_seconds("-00:01:40"), 100)
        self.assertEqual(hours_minutes_seconds("-00h02m30s"), 150)

        with self.assertRaises(ValueError):
            hours_minutes_seconds("02:04")

        with self.assertRaises(ValueError):
            hours_minutes_seconds("FOO")

        with self.assertRaises(ValueError):
            hours_minutes_seconds("BAR")

        with self.assertRaises(ValueError):
            hours_minutes_seconds("11:ERR:00")
