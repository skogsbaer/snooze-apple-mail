import snoozeLib
import snoozeDb
import argparse

parser = argparse.ArgumentParser(description='Snooze selected mails in Mail.app')
parser.add_argument('--list', action='store_true', help='List contents of snooze DB')
args = parser.parse_args()

db = snoozeDb.SnoozeDb()

if args.list:
    snoozeLib.displaySnoozeDb(db)
else:
    snoozeLib.snoozeMails(db)
