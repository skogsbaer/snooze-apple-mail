import tempfile
import unittest
import timeSuggest
import time
import utils

class TestTimeSuggest(unittest.TestCase):

    def assertSuggestions(self, dateStr, expected):
        t = utils.parseAsLocalTime(dateStr)
        realExpected = [(e[0], utils.parseAsLocalTime(e[1])) for e in expected]
        given = timeSuggest.suggestTime(t)
        # print("\nexpected: " + str(realExpected))
        # print("given:    " + str(given))
        self.assertEqual(realExpected, given)

    def test_suggestions(self):
        self.assertSuggestions(
            "2020-10-11 10:07", # Sonntag
            [("Later         (Sun 20:00)", "2020-10-11 20:00"),
             ("Tomorrow      (Mon 09:00)", "2020-10-12 09:00"),
             ("Next weekend  (Sat 09:00)", "2020-10-17 09:00")]
        )
        self.assertSuggestions(
            "2020-10-10 10:07", # Samstag
            [("Later         (Sat 20:00)", "2020-10-10 20:00"),
             ("Tomorrow      (Sun 09:00)", "2020-10-11 09:00"),
             ("Next week     (Mon 09:00)", "2020-10-12 09:00"),
             ("Next weekend  (Sat 09:00)", "2020-10-17 09:00")]
        )
        self.assertSuggestions(
            "2020-10-09 17:00", # Freitag
            [("Later         (Fri 20:00)", "2020-10-09 20:00"),
             ("Tomorrow      (Sat 09:00)", "2020-10-10 09:00"),
             ("Next week     (Mon 09:00)", "2020-10-12 09:00")]
        )
        self.assertSuggestions(
            "2020-10-08 10:07", # Donnerstag
            [("Later         (Thu 20:00)", "2020-10-08 20:00"),
             ("Tomorrow      (Fri 09:00)", "2020-10-09 09:00"),
             ("Weekend       (Sat 09:00)", "2020-10-10 09:00"),
             ("Next week     (Mon 09:00)", "2020-10-12 09:00")]
        )
        self.assertSuggestions(
            "2020-10-07 10:07", # Mittwoch
            [("Later         (Wed 20:00)", "2020-10-07 20:00"),
             ("Tomorrow      (Thu 09:00)", "2020-10-08 09:00"),
             ("Weekend       (Sat 09:00)", "2020-10-10 09:00"),
             ("Next week     (Mon 09:00)", "2020-10-12 09:00")]
        )
        self.assertSuggestions(
            "2020-10-06 10:07", # Dienstag
            [("Later         (Tue 20:00)", "2020-10-06 20:00"),
             ("Tomorrow      (Wed 09:00)", "2020-10-07 09:00"),
             ("Weekend       (Sat 09:00)", "2020-10-10 09:00"),
             ("Next week     (Mon 09:00)", "2020-10-12 09:00")]
        )
        self.assertSuggestions(
            "2020-10-05 18:59", # Montag
            [("Later         (Mon 20:00)", "2020-10-05 20:00"),
             ("Tomorrow      (Tue 09:00)", "2020-10-06 09:00"),
             ("Weekend       (Sat 09:00)", "2020-10-10 09:00"),
             ("Next week     (Mon 09:00)", "2020-10-12 09:00")]
        )
        self.assertSuggestions(
            "2020-10-05 19:00", # Montag
            [("Tomorrow      (Tue 09:00)", "2020-10-06 09:00"),
             ("Weekend       (Sat 09:00)", "2020-10-10 09:00"),
             ("Next week     (Mon 09:00)", "2020-10-12 09:00")]
        )
