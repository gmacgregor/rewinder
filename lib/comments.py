import datetime
import sys
sys.path.append('/home/gmacgregor/webapps/django/')

from django.conf import settings
from django.core.management import setup_environ
from rewinder import settings

setup_environ(settings)

from rewinder.apps.tumblelog.models import TumblelogItem


def close():
    today = datetime.datetime.today()
    close_date = today - datetime.timedelta(days=settings.COMMENTS_CLOSE_AFTER)
    print "closing comments %s days old (published before %s)" % (settings.COMMENTS_CLOSE_AFTER, close_date)
    objs = TumblelogItem.objects.all()
    for o in objs:
        if o.pub_date < close_date:
            mod = o.get_content_object()
            mod.enable_comments = False
            mod.save()
    print "done"

def enable():
    objs = TumblelogItem.objects.all()
    for o in objs:
        mod = o.get_content_object()
        mod.enable_comments = True
        mod.save()

if __name__ == "main":
    close()
