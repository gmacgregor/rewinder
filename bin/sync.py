import datetime
import sys
sys.path.append('/home/gmacgregor/webapps/django/')

from django.core.management import setup_environ
from rewinder import settings
setup_environ(settings)

from rewinder.util.syncr import sync_delicious
from rewinder.util.syncr import sync_flickr
from rewinder.util.syncr import sync_twitter
print "syncing delicious.... <%s>" % datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
sync_delicious.run()
print "done <delicious: %s>" % datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
print "syncing flickr.... <%s>" % datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
sync_flickr.run()
print "done <flickr: %s>" % datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
print "syncing twitter... <%s>" % datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
sync_twitter.run()
print "done <twitter: %s>" % datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
