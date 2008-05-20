from django.conf import settings
from rewinder.apps.tumblelog.models import TumblelogItem
import datetime


def close():
    today = datetime.datetime.today()
    close_date = today - datetime.timedelta(days=settings.COMMENTS_CLOSE_AFTER)
    objs = TumblelogItem.objects.all()
    for o in objs:
        if o.pub_date < close_date:
            mod = o.get_content_object()
            mod.enable_comments = False
            mod.save()

def enable():
    objs = TumblelogItem.objects.all()
    for o in objs:
        mod = o.get_content_object()
        mod.enable_comments = True
        mode.save()
