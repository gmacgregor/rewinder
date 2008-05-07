from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.blog.models import Article
from rewinder.apps.twitter.models import Tweet
from rewinder.apps.flickr.models import Photo
from rewinder.apps.video.models import Video

from rewinder.views import list

def list_items(request):
    logs = TumblelogItem.objects.all().exclude(content_type__exact=15).count()
    #articles = Article.published_articles.all().count()
    links = Bookmark.objects.all().count()
    videos = Video.objects.all().count()
    photos = Photo.objects.all().filter(owner='sixminutes').count()
    tweets = Tweet.objects.all().count()
    ctx = {'logs': logs, 'links': links, 'photos': photos, 'tweets': tweets, 'videos': videos}
    return list(request, 'tumblelog', TumblelogItem, '-pub_date', ctx)