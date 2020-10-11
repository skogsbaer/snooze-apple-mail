#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import npyscreen
import time
import warnings
import utils

class Done(Exception):
    def __init__(self, value):
        self.value = value

class QuickSelect(npyscreen.MultiLineAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def actionHighlighted(self, act_on_this, key_press):
        raise Done(act_on_this)

COLUMNS = 80

class MyActionForm(npyscreen.ActionForm):
    OK_BUTTON_BR_OFFSET = (2, COLUMNS - 15)
    CANCEL_BUTTON_BR_OFFSET = (2, COLUMNS - 4)
    OK_BUTTON_TEXT          = "Cancel"
    CANCEL_BUTTON_TEXT      = "Ok"
    # We swap to meaning of the two buttons because we cannot swap
    # them physically.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ok = True
        self.move_ok_button()
    def on_ok(self):
        self.ok = False
    def on_cancel(self):
        self.ok = True

class SnoozeSelectApp(npyscreen.NPSApp):
    def __init__(self, introLines, suggestions):
        self.introLines = introLines
        self.suggestions = suggestions

    def main(self):
        lines = max(16, len(self.suggestions) + 7 + len(self.introLines) + 1)
        form = MyActionForm(name="Snooze Email", lines=lines, columns=80)
        self.form = form
        for l in self.introLines:
            maxCols = 70
            suffix = ''
            if len(l) > maxCols:
                suffix = '...'
            l = l[:maxCols] + suffix
            form.add(npyscreen.FixedText, value=l, editable=False)
        form.add(npyscreen.FixedText, value="", editable=False)
        ms = form.add(QuickSelect,
                      name="Snooze",
                      value=[],
                      values=self.suggestions,
                      scroll_exit=True,
                      height=len(self.suggestions) + 1)
        date = form.add(npyscreen.TitleDateCombo, value=0, name="Date: ")
        time  = form.add(npyscreen.TitleText, value="09:00", name="Time:",)
        self.date = date
        self.time = time
        form.edit()

def enterDateTime(infoLines, suggestions, errorMsg=None):
    myInfoLines = infoLines
    if errorMsg:
        myInfoLines = infoLines + ["", errorMsg]
    app = SnoozeSelectApp(myInfoLines, [s[0] for s in suggestions])
    value = None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            app.run(fork=False)
    except Done as e:
        for k, v in suggestions:
            if k == e.value:
                value = v
    ok = app.form.ok
    if not ok:
        return None
    if value is not None:
        return value
    dtStr = str(app.date.value) + " " + str(app.time.value)
    dt = utils.parseAsLocalTime(dtStr, fail=False)
    if dt is not None:
        return dt
    else:
        errMsg = "Error: Could not parse time " + str(app.time.value)
        if not app.date.value:
            errMsg = "Error: No date selected"
        app = None
        return enterDateTime(infoLines, suggestions, errMsg)

if __name__ == "__main__":
    suggestions = [("Later         (Sa 20:00)", "1"),
                   ("Tomorrow      (So 09:00)", "2"),
                   ("Next week     (Mo 09:00)", "3"),
                   ("Next weekend  (Sa 09:00)", "4")]
    res = enterDateTime(['Test 2 (Stefan Wehr <mail@stefanwehr.de>)'], suggestions)
    print(res)
