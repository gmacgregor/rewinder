from django.contrib.sitemaps import Sitemap
from rewinder.apps.blog.models import Article
from rewinder.apps.flickr.models import Photo
from rewinder.apps.video.models import Video
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.twitter.models import Tweet
from rewinder.apps.tumblelog.models import TumblelogItem

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 1.0
    
    def items(self):
        return Article.published_articles.all()
    
    def lastmod(self, obj):
        return obj.pub_date

class TumblelogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7
    
    def items(self):
        return TumblelogItem.objects.order_by('-pub_date')
    
    def lastmod(self, obj):
        item = obj.get_content_object()
        return item.pub_date
    
    def location(self, obj):
        item = obj.get_content_object()
        return item.get_absolute_url()
    
class VideoSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    
    def items(self):
        return Video.objects.all()
    
    def lastmod(self, obj):
        return obj.pub_date

class LinkSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7
    
    def items(self):
        return Bookmark.objects.all()
    
    def lastmod(self, obj):
        return obj.saved_date

class PhotoSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    
    def items(self):
        return Photo.sixminutes.all()
    
    def lastmod(self, obj):
        return obj.taken_date

class TweetSitemap(Sitemap):
    changefreq = "never"
    priority = 0.4
    
    def items(self):
        return Tweet.objects.all()
    
    def lastmod(self, obj):
        return obj.pub_time

        