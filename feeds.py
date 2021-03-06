from django.contrib.syndication.feeds import Feed
from rewinder.apps.blog.models import Article
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.flickr.models import Photo
from rewinder.apps.video.models import Video
from rewinder.apps.twitter.models import Tweet
from rewinder.apps.generic.models import Quote
from rewinder.apps.tumblelog.models import TumblelogItem

class LatestArticles(Feed):
    title = "rewinder.ca: Latest blog posts"
    link = "/blog/"
    description = "Latest blog posts from rewinder.ca"
    
    def items(self):
        return Article.published_articles.all()[:10]

class LatestLinks(Feed):
    title = "rewinder.ca: Latest links"
    link = "/links/"
    description = "Latest links at rewinder.ca"
    
    def items(self):
        return Bookmark.objects.order_by('-saved_date')[:10]

class LatestPhotos(Feed):
    title = "rewinder.ca: Latest photos"
    link = "/photos/"
    description = "Latest photos from rewinder.ca"
    
    def items(self):
        return Photo.sixminutes.order_by('-taken_date')[:10]

class LatestVideos(Feed):
    title = "rewinder.ca: Latest videos"
    link = "/videos/"
    description = "Latest videos from rewinder.ca"
    
    def items(self):
        return Video.objects.order_by('-pub_date')[:10]

class LatestTweets(Feed):
    title = "rewinder.ca: Latest twitter tweets"
    link = "/tweets/"
    description = "Latest twitter tweets"
    
    def items(self):
        return Tweet.objects.order_by('-pub_time')[:10]

class LatestQuotes(Feed):
    title = "rewinder.ca: Latest quotes"
    link = "/quotes/"
    description = "Latest quotes"
    
    def items(self):
        return Quote.objects.order_by('-pub_date')[:10]

class LatestTumblelog(Feed):
    title = "rewinder.ca: Latest online activity"
    link = "/tumblelog/"
    description = "My latest online activity"
    
    def items(self):
        return TumblelogItem.objects.order_by('-pub_date')[:10]
    
    def item_link(self, item):
        obj = item.get_content_object()
        return obj.get_absolute_url()