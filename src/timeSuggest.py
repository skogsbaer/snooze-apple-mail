import time
from datetime import datetime, timedelta

def findDay(base, pred):
    if pred(base):
        return base
    return findDay(base + timedelta(days=1), pred)

def dow(dt):
    x = dt.isoweekday()
    if x == 1:
        return "Mon"
    if x == 2:
        return "Tue"
    if x == 3:
        return "Wed"
    if x == 4:
        return "Thu"
    if x == 5:
        return "Fri"
    if x == 6:
        return "Sat"
    if x == 7:
        return "Sun"

def suggestTime(t):
    dt = datetime.fromtimestamp(t)
    today9 = dt.replace(hour=9, minute=0)
    today20 = dt.replace(hour=20, minute=0)
    oneDay = timedelta(days=1)
    tomorrow = today9 + oneDay
    nextWeek = findDay(tomorrow, lambda x: x.isoweekday() == 1)
    weekEnd = findDay(today9, lambda x: x.isoweekday() == 6)
    if dt.isoweekday() in [6,7]:
        weekEnd = findDay(nextWeek, lambda x: x.isoweekday() == 6)
    candidates =      [(f"Later         ({dow(today20)} 20:00)", today20),
                       (f"Tomorrow      ({dow(tomorrow)} 09:00)", tomorrow)]
    if weekEnd < nextWeek:
        candidates += [(f"Weekend       ({dow(weekEnd)} 09:00)", weekEnd),
                       (f"Next week     ({dow(nextWeek)} 09:00)", nextWeek)]
    else:
        candidates += [(f"Next week     ({dow(nextWeek)} 09:00)", nextWeek),
                       (f"Next weekend  ({dow(weekEnd)} 09:00)", weekEnd)]
    res = []
    for cand in candidates:
        if cand[1] == today20:
            if dt.hour < 19:
                res.append(cand)
            continue
        found = False
        for _, x in res:
            if cand[1] <= x:
                found = True
        if not found:
            res.append(cand)
    return [(x[0], x[1].timestamp()) for x in res]
