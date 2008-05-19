from django.conf.urls.defaults import *
from django.conf import settings
from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.apps.video.models import Video
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.twitter.models import Tweet
from rewinder.feeds import LatestArticles, LatestLinks, LatestPhotos, LatestVideos

feeds = {
    'blog': LatestArticles,
    'links': LatestLinks,
    'photos': LatestPhotos,
    'videos': LatestVideos,
}

urlpatterns = patterns('',
    #url(r'^$', 'django.views.generic.list_detail.object_list', dict(tumblelog_dict, paginate_by=10), name="homepage"),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}, name="homepage")
)

urlpatterns += patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^remarks/', include('threadedcomments.urls')),
    url(r'^links/?page=(?P<page>[0-9]+)$', 'rewinder.views.list', {'app': 'delicious', 'model': Bookmark, 'ordering': '-saved_date'}, name="bookmark_list"),
    (r'^links/', include('rewinder.apps.delicious.urls')),
    (r'^places/', include('rewinder.apps.geo.urls')),
    url(r'^photos/?page=(?P<page>[0-9]+)$', 'rewinder.apps.flickr.views.list', name="photo_list"),
    (r'^photos/', include('rewinder.apps.flickr.urls')),
    url(r'^activity/?page=(?P<page>[0-9]+)$', 'rewinder.views.list', {'app': 'tumblelog', 'model': TumblelogItem}, name="tumblelog_list"),
    (r'^activity/', include('rewinder.apps.tumblelog.urls')),
    url(r'^tweets/?page=(?P<page>[0-9]+)$', 'rewinder.views.list', {'app': 'twitter', 'model': Tweet, 'ordering': '-pub_time'}, name="tweet_list"),
    (r'^tweets/', include('rewinder.apps.twitter.urls')),
    url(r'^videos/?page=(?P<page>[0-9]+)$', 'rewinder.views.list', {'app': 'video', 'model': Video}, name="video_list"),
    (r'^videos/', include('rewinder.apps.video.urls')),
    (r'^blog/', include('rewinder.apps.blog.urls')),
    url(r'^tags/(?P<tag>[-\w]+)/$', 'rewinder.views.tag_detail', name='tag_detail'),
    url(r'^tags/$', 'rewinder.views.all_tags', name='tags_list'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/gmacgregor/dev/rewinder/site_media'}),
    )
