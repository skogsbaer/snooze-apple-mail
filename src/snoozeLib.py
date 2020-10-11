
import sys
sys.path.insert(0, '/Users/swehr/devel/libPyshell/src/')

from shell import *
import json
import pathlib
import snoozeDb
import time
import timeSuggest
import inputDateTime

thisDir = pathlib.Path(__file__).parent.absolute()
scriptPath = os.path.join(thisDir, 'mail.js')

def abort(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)

def runScript(cmd, args=[], noResult=False):
    if type(args) == str:
        args = [args]
    if noResult:
        captureStdout=False
        stderrToStdout=False
    else:
        captureStdout=splitLines
        stderrToStdout=True
    lines = run(
        ['osascript', scriptPath, cmd] + args,
        captureStdout=captureStdout, stderrToStdout=stderrToStdout
    ).stdout
    jsons = []
    for l in lines:
        if l.startswith('JSON: '):
            l = l[len('JSON: '):]
            jsons.append(json.loads(l))
    if len(jsons) == 1:
        return jsons[0]
    elif len(jsons) == 0:
        if noResult:
            return None
        else:
            abort("No JSON output found for mail.js command " + cmd + ": " + str(lines))
    else:
        abort("Too many JSON outputs found for mail.js command " + cmd + ": " + str(lines))

def getSelectedMsgs():
    return runScript('selected-messages-json')

def moveMailsToSnoozed(msgIds):
    runScript('snooze-messages', msgIds, noResult=True)

def getSnoozedMsgIdsFromMail():
    return runScript('snoozed-ids-json')

def unsnoozeEmail(msgId):
    runScript('unsnooze-message', msgId, noResult=True)

def askForSnoozeDate(infoLines):
    now = time.time()
    suggestions = timeSuggest.suggestTime(now)
    return inputDateTime.enterDateTime(infoLines, suggestions)

def snoozeMails(db):
    msgs = getSelectedMsgs()
    if len(msgs) == 0:
        abort("No messages selected in Mail.app")
    infoLines = []
    n = 2
    if len(msgs) == n + 1:
        n += 1
    for i in range(n):
        if i < len(msgs):
            m = msgs[i]
            infoLines.append(m['subject'] + ' (' + m['from'] + ')')
    delta = len(msgs) - len(infoLines)
    if delta > 0:
        infoLines.append(f'({delta} more messages)')
    wakeUp = askForSnoozeDate(infoLines)
    msgIds = []
    # We first add the mails to our DB. If the move in Mail.app then fails for some reasons,
    # we only have some superfluous mails in the DB. If we did it the other way round, then
    # we would have snoozed emails in Mail.app without an record in the DB.
    for m in msgs:
        entry = snoozeDb.SnoozeDbEntry.fromJsonString(m, wakeUp)
        print(f"Snoozing email {repr(entry.subject)} ({entry.sender}) until {formatTime(wakeUp)}")
        db.addOrUpdateEntry(entry)
        msgIds.append(entry.msgId)
    moveMailsToSnoozed(msgIds)

def tryUnsnooze(db, force):
    t = time.time()
    if force:
        t = sys.float_info.max
    entries = db.getEntries(t)
    if len(entries) == 0:
        print("No emails found that should be unsnoozed.")
    # We first unsnooze the mail in Mail.app, then delete it from the DB. This way, an error
    # would leave at most superfluous entries in the DB. We do not want emails in the Snooze
    # folder without reference in the DB.
    for e in entries:
        print(f"Unsnoozing {repr(e.subject)} ({e.sender})")
        unsnoozeEmail(e.msgId)
        db.deleteEntry(e.msgId)

def formatTime(f):
    local = time.localtime(f)
    return time.strftime("%Y-%m-%d %H:%M", local)

def displaySnoozeDb(db):
    allEntries = db.getEntries()
    allEntries.reverse() # most recent last
    if len(allEntries) == 0:
        print('No snoozed emails')
    for e in allEntries:
        timeStr = formatTime(e.wakeUp)
        print(f"[{timeStr}] {e.sender}: {e.subject}")
