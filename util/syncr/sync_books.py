from django.conf import settings
from rewinder.syncr.app.syncreadernaut import BookSyncr

def run():
    b = BookSyncr()
    b.readernautsyncr() #readernautsyncr calls settings.READERNAUT_USERNAME