from datetime import datetime
from zoneinfo import ZoneInfo

def clock(zone='Asia/Kolkata', twelve=False):
    return datetime.now(ZoneInfo(zone)).strftime('%I:%M:%S %p' if twelve else '%H:%M:%S')

def duration(seconds):
    h, r = divmod(max(0, int(seconds)), 3600)
    m, s = divmod(r, 60)
    return f'{h:02}:{m:02}:{s:02}'
