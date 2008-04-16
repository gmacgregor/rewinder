from django.core.management import setup_environ
import rewinder.settings
setup_environ(rewinder.settings)

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
