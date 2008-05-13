from django.conf import settings
import pytz


def time_to_settings(time_field):
    tz = pytz.timezone(settings.TIME_ZONE)
    new_time = time_field.replace(tzinfo=tz)
    #new_time = time_field.replace(tzinfo=pytz.utc).astimezone(tz)
    return new_time

def time_to_utc(time_field):
    new_time = time_field.replace(tzinfo=pytz.utc)
    return new_time