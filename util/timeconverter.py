from django.conf import settings
from dateutil import tz
import pytz


def time_to_settings(time_field):
    zone = pytz.timezone(settings.TIME_ZONE)
    newtime = time_field.replace(tzinfo=tz.tzutc()).astimezone(zone)
    return newtime

def time_to_utc(time_field):
    new_time = time_field.replace(tzinfo=pytz.utc)
    return new_time