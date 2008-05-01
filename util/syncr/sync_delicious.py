from django.conf import settings
from rewinder.util.syncr.delicious import DeliciousSyncr

def run():
    d = DeliciousSyncr(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD)
    # sync today's bookmarks
    #d.syncBookmarks
    d.syncRecent()
    #d.syncAll()
