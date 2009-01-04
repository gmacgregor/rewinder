from django.conf import settings
from rewinder.syncr.app.delicious import DeliciousSyncr

def run():
    d = DeliciousSyncr(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD)
    # sync today's bookmarks
    #d.syncRecent()
    d.syncAll()
