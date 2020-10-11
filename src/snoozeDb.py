from typing import *
import json
import sqlite3
import os
from contextlib import closing
import sys

DEFAULT_DB_FILE = os.path.join(os.environ.get('HOME'), '.snooze-apple-mail.db')

def initDb(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages
            (msgId TEXT NOT NULL PRIMARY KEY,
             subject TEXT NOT NULL,
             sender TEXT NOT NULL,
             recipients TEXT NOT NULL,
             wakeUp FLOAT NOT NULL)
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS wakeUp_idx ON messages (wakeUp);
        """
    )

class SnoozeDb:
    def __init__(self, fileName=DEFAULT_DB_FILE):
        self.conn = sqlite3.connect(fileName)
        initDb(self.conn)

    def getEntries(self, time=sys.float_info.max):
        entries = []
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
                """
                SELECT msgId, subject, sender, recipients, wakeUp
                FROM messages
                WHERE wakeUp <= ?
                ORDER BY wakeUp ASC
                """,
                (float(time),)
            )
            rawEntries = cursor.fetchall()
            for (msgId, subject, sender, recipients, wakeUp) in rawEntries:
                entries.append(
                    SnoozeDbEntry(msgId, subject, sender, json.loads(recipients), wakeUp)
                )
        return entries

    def addOrUpdateEntry(self, entry):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
                """
                REPLACE INTO messages(msgId, subject, sender, recipients, wakeUp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (entry.msgId,
                 entry.subject,
                 entry.sender,
                 json.dumps(entry.recipients),
                 entry.wakeUp)
            )
            self.conn.commit()

    def close(self):
        self.conn.close()

    def deleteEntry(self, msgId):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
                """
                DELETE FROM messages WHERE msgId=?
                """,
                (msgId,)
            )
            self.conn.commit()


class SnoozeDbEntry:

    def fromJsonString(j, wakeUp):
        return SnoozeDbEntry(
            j["msgId"],
            j["subject"],
            j["from"],
            j["to"],
            wakeUp
        )

    def __init__(
            self,
            msgId: str,
            subject: str,
            sender: str,
            recipients: List[str],
            wakeUp: Optional[float]
    ):
        self.msgId = msgId
        self.subject = subject
        self.sender = sender
        self.recipients = recipients
        self.wakeUp = wakeUp

    def __repr__(self):
        return "SnoozeDbEntry(" + repr(self.__dict__) + ")"

    def __eq__(self, other):
        if type(other) is not SnoozeDbEntry:
            return false
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__dict__)
