from django.core.management import setup_environ
import rewinder.settings
setup_environ(settings)

from rewinder.util.syncr import sync_delicious
from rewinder.util.syncr import sync_flickr
from rewinder.util.syncr import sync_twitter
sync_delicious.run()
sync_flickr.run()
sync_twitter.run()
