import snoozeLib
import snoozeDb
import argparse

parser = argparse.ArgumentParser(description='Snooze selected mails in Mail.app')
parser.add_argument('--all', action='store_true', help='Unsnooze all messages')
args = parser.parse_args()

db = snoozeDb.SnoozeDb()

snoozeLib.tryUnsnooze(db, args.all)
