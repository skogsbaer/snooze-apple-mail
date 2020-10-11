
import sys
sys.path.insert(0, '/Users/swehr/devel/libPyshell/src/')

from shell import *
import json

scriptPath = '/Users/swehr/devel/snooze-apple-mail/mail.js'

def abort(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)

def runScript(cmd, args=[], noResult=False):
    if type(args) == str:
        args = [args]
    lines = run(
        ['osascript', scriptPath, cmd] + args,
        captureStdout=splitLines, stderrToStdout=True
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

def getSelectedMsgIds():
    return runScript('selected-ids-json')

def moveMailsToSnooze(msgIds):
    runScript('snooze-messages', msgIds, noResult=True)

def getSnoozedMsgIdsFromMail():
    return runScript('snoozed-ids-json')

def unsnoozeEmail(msgId):
    runScript('unsnooze-message', msgId, noResult=True)

def snoozeMails():
    msgIds = getSelectedMsgIds()
    if len(msgIds) == 0:
        abort("No messages selected")
    # FIXME: ask for date, store in DB as pending
    moveMailsToSnooze(msgIds)
    # FIXME: set mails in DB as no longer pending

def tryUnsnooze():
    msgIdsInMail = getSnoozedMsgIdsFromMail()
    print(str(msgIdsInMail))
    # get from DB, do sanity check
    # find out which mails must be unsnoozed
    # do unsnooze them
    for msgId in msgIdsInMail:
        unsnoozeEmail(msgId)

def displaySnoozeDb():
    print('implement me')
