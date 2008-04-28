from django.conf.urls.defaults import *
from django.conf import settings
from rewinder.apps.tumblelog.models import TumblelogItem

tumblelog_dict = {
    'queryset': TumblelogItem.objects.all().order_by('-pub_date')
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', dict(tumblelog_dict, paginate_by=10), name="homepage"),
)

urlpatterns += patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    #(r'^comments/', include('django.contrib.comments.urls.comments')),
    (r'^remarks/', include('threadedcomments.urls')),
    (r'^links/', include('rewinder.apps.delicious.urls')),
    (r'^places/', include('rewinder.apps.geo.urls')),
    (r'^photos/', include('rewinder.apps.flickr.urls')),
    url(r'^tumblelog/?page=(?P<page>[0-9]+)$', 'django.views.generic.list_detail.object_list', dict(tumblelog_dict), name="tumblelog_list"),
    url(r'^tumblelog/','django.views.generic.list_detail.object_list', dict(tumblelog_dict, paginate_by=10), name="tumblelog_home"),
    (r'^tweets/', include('rewinder.apps.twitter.urls')),
    (r'^videos/', include('rewinder.apps.video.urls')),
    (r'^words/', include('rewinder.apps.blog.urls')),
    url(r'^tags/(?P<tag>[-\w]+)/$', 'rewinder.apps.blog.views.tag_detail', name='tag_detail'),
    url(r'^tags/$', 'rewinder.apps.blog.views.all_tags', name='tags_list'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/gmacgregor/dev/rewinder/site_media'}),
    )
