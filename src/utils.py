import time

def parseAsLocalTime(s, fmt='%Y-%m-%d %H:%M', fail=True):
    try:
        dt = time.strptime(s, fmt)
    except ValueError:
        if fail:
            raise
        else:
            return None
    return time.mktime(dt)
