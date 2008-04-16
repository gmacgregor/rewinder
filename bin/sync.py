from django.core.management import setup_environ
import sys
sys.path.append('/home/gmacgregor/webapps/django/')
from rewinder import settings
setup_environ(settings)

from rewinder.util.syncr import sync_delicious
from rewinder.util.syncr import sync_flickr
from rewinder.util.syncr import sync_twitter
print "syncing delicious...."
sync_delicious.run()
print "done <delicious>"
print "syncing flickr...."
sync_flickr.run()
print "done <flickr>"
print "syncing twitter..."
sync_twitter.run()
print "done <twitter>"
