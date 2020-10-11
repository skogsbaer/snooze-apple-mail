ObjC.import("stdlib");

const accountName = "Hs-Offenburg";
const snoozeMailboxName = "Snooze";
const inboxName = "INBOX";

function getArgs() {
    const primArgs = $.NSProcessInfo.processInfo.arguments    // NSArray
    const argv = []
    const argc = primArgs.count
    for (let i = 2; i < argc; i++) {
        argv.push(ObjC.unwrap(primArgs.objectAtIndex(i)))
    }
    return argv;
}

function abort(msg) {
    console.log("ERROR: " + msg);
    $.exit(1);
}

function getByName(elems, name, what) {
    for (let x of elems) {
        if (x.name() === name) {
            return x;
        }
    }
    abort(what + " " + name + " not found");
}

function arraySameElems(arr1, arr2) {
    for (let x of arr1) {
        if (arr2.indexOf(x) < 0) {
            return false;
        }
    }
    for (let x of arr2) {
        if (arr1.indexOf(x) < 0) {
            return false;
        }
    }
    return true;
}

function uniqueMessageIds(arr) {
    const res = [];
    arr.forEach(x => {
        if (res.indexOf(x) < 0) {
            res.push(x);
        }
    });
    return res;
}

function formatRecipient(r) {
    let s = "";
    const n = r.name();
    if (n) {
        s += n + " <";
    }
    s += r.address();
    if (n) {
        s += ">";
    }
    return s;
}

function printSelectedMessages(mail) {
    const selectedMessages = mail.selection();
    const handled = {};
    const res = [];
    selectedMessages.forEach(msg => {
        const msgId = msg.messageId();
        if (!handled[msgId]) {
            handled[msgId] = true;
            const subject = msg.subject();
            const sender = msg.sender();
            const recipients = msg.recipients().map(r => formatRecipient(r));
            res.push({msgId: msgId, from: sender, to: recipients, subject: subject});
        };
    });
    console.log("JSON: " + JSON.stringify(res));
}

function snoozeMessages(mail, cmdLineMsgIds) {
    const selectedMessages = mail.selection();
    const msgIds = uniqueMessageIds(selectedMessages.map(msg => {
        return msg.messageId();
    }));
    if (!arraySameElems(msgIds, cmdLineMsgIds)) {
        abort("Selection changed, ids of selected messages: " + JSON.stringify(msgIds) +
              ", ids on the cmdline: " + JSON.stringify(cmdLineMsgIds));
    }
    const account = getByName(mail.accounts(), accountName, "Account");
    const mailbox = getByName(account.mailboxes(), snoozeMailboxName, "Mailbox");
    selectedMessages.forEach(msg => {
        mail.move(msg, {to: mailbox});
    });
}

function unsnoozeMessage(mail, msgId) {
    const account = getByName(mail.accounts(), accountName, "Account");
    const mailbox = getByName(account.mailboxes(), snoozeMailboxName, "Mailbox");
    const inbox = getByName(account.mailboxes(), inboxName, "Mailbox");
    const moved = {};
    mailbox.messages().forEach(msg => {
        if (msgId == msg.messageId() && !moved[msgId]) {
            msg.readStatus = false;
            mail.move(msg, {to: inbox});
            moved[msgId] = true;
        }
    });
    const numMoved = Object.keys(moved).length;
    if (numMoved === 1) {
        console.log("Unsoozed 1 message");
    } else if (numMoved > 0) {
        console.log("Unsoozed " + numMoved + " messages");
    } else {
        console.log("No message found in mailbox " + snoozeMailboxName + " with message id " + msgId);
    }
}

function displaySnoozedMessages(mail) {
    const account = getByName(mail.accounts(), accountName, "Account");
    const mailbox = getByName(account.mailboxes(), snoozeMailboxName, "Mailbox");
    const messages = mailbox.messages();
    console.log(messages.length + " snoozed messages");
    messages.forEach((msg, idx) => {
        if (msg.deletedStatus()) {
            return;
        }
        const msgId = msg.messageId();
        let s = msgId;
        const subject = msg.subject();
        s += "\n" + subject;
        const sender = msg.sender();
        s += "\nFrom: " + sender;
        const recipients = msg.recipients();
        recipients.forEach(r => {
            s += "\nTo: ";
            s += formatRecipient(r);
        });
        if (idx < messages.length - 1) {
            console.log("\n");
        }
    });
}

function printSnoozedMessageIds(mail) {
    const account = getByName(mail.accounts(), accountName, "Account");
    const mailbox = getByName(account.mailboxes(), snoozeMailboxName, "Mailbox");
    const messages = mailbox.messages();
    const msgIds = uniqueMessageIds(messages.map(msg => msg.messageId()));
    console.log("JSON: " + JSON.stringify(msgIds));
}

function usage() {
    abort("USAGE: osascript mail.js COMMAND [ARGS]\n\n" +
          "Commands:\n" +
          "selected-messages-json: Print the message ids of the currently selected emails as JSON.\n" +
          "snooze-messages id1 .. idn: Snooze the currently selected emails, \n" +
          "   which must have the given message ids\n" +
          "unsnooze-message id: Unsnooze the message with the id given.\n" +
          "display-snoozed: Display snoozed emails.\n" +
          "snoozed-ids-json: Print the message ids of all snoozed emails as JSON."
         );
}

function command(args) {
    if (args.length == 0) {
        usage();
    }
    const cmd = args[0];
    const mail = Application('Mail');
    if (cmd === "selected-messages-json") {
        printSelectedMessages(mail);
    } else if (cmd === "snooze-messages") {
        if (args.length === 1) {
            usage();
        }
        snoozeMessages(mail, args.slice(1));
    } else if (cmd === "unsnooze-message") {
        if (args.length !== 2) {
            usage();
        }
        unsnoozeMessage(mail, args[1]);
    } else if (cmd === "display-snoozed") {
        if (args.length !== 1) {
            usage();
        }
        displaySnoozedMessages(mail);
    } else if (cmd === "snoozed-ids-json") {
        if (args.length !== 1) {
            usage();
        }
        printSnoozedMessageIds(mail);
    } else {
        abort("Unknown command: " + cmd);
    }
}

command(getArgs());
