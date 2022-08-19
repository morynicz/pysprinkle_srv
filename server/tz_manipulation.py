from datetime import datetime
from dateutil import tz

utc = tz.tzutc()
local = tz.tzlocal()


def utc_to_local(timestamp):
    return convert_tz(timestamp, utc, local)


def local_to_utc(timestamp):
    return convert_tz(timestamp, local, utc)


def convert_tz(timestamp, from_zone, to_zone):
    # utc = datetime.utcnow()
    # input_dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
    input_dt = datetime.fromisoformat(timestamp)
    print("run")

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    input_dt = input_dt.replace(tzinfo=from_zone)

    # Convert time zone
    return input_dt.astimezone(to_zone)
