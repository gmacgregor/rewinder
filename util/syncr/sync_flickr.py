from flickr import FlickrSyncr

api_key = 'c5b82d5a4ae7101366113790d947da9e'
api_secret = '072822dd97710515'

f = FlickrSyncr(api_key, api_secret)
f.syncAllPublic('sixminutes')