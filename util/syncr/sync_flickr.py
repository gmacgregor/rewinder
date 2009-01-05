from django.conf import settings
from rewinder.syncr.app.flickr import FlickrSyncr

def run():
    f = FlickrSyncr(settings.FLICKR_KEY, settings.FLICKR_SECRET)
    f.syncRecentPhotos('sixminutes', days=2000)

def favs():
    f = FlickrSyncr(api_key, api_secret)
    f.syncPublicFavorites('sixminutes')