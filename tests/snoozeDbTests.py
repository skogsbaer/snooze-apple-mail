import tempfile
import unittest
from snoozeDb import *

class TestSnoozeDb(unittest.TestCase):
    def test_basic(self):
        e1 = SnoozeDbEntry("msg-id-1", "subject-1", "sender-1", ["r-11", "r-12"], 25.0)
        e2 = SnoozeDbEntry("msg-id-2", "subject-2", "sender-2", ["r-21"], 20.0)
        with tempfile.TemporaryDirectory() as tmp:
            dbFile = os.path.join(tmp, "test.db")
            db = SnoozeDb(dbFile)
            db.addOrUpdateEntry(e1)
            db.addOrUpdateEntry(e2)
            self.assertEqual([e2, e1], db.getEntries())
            e3 = SnoozeDbEntry("msg-id-1", "subject-1", "sender-3", ["r-11", "r-12"], 15.0)
            db.addOrUpdateEntry(e3)
            self.assertEqual([e3, e2], db.getEntries())
            self.assertEqual([e3], db.getEntries(17))
            self.assertEqual([], db.getEntries(14))
            db.close()
            db = SnoozeDb(dbFile)
            self.assertEqual([e3, e2], db.getEntries())
            db.deleteEntry('msg-id-1')
            self.assertEqual([e2], db.getEntries())
            db.close()
            db = SnoozeDb(dbFile)
            self.assertEqual([e2], db.getEntries())
