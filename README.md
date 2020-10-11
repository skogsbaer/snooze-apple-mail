# snooze-apple-mail

Gmai-like snooze functionality for Apple's Mail.app

## How it works

* Select one or several messages in Mail.app.
* Run the `snooze` command from the terminal. The terminal-UI will prompt
  you for a snooze date.
* Later, at the given snooze date, a cronjob will put the mail back into
  the inbox and mark it as unread.

## Configuration

You need to have a crontab like this, adjust the paths!

```
# min hour dom moy dow cmd
*   *    *   *   *   /Users/swehr/devel/snooze-apple-mail/try-unsnooze
```
