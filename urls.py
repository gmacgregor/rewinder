from django.conf.urls.defaults import *
from django.conf import settings
from rewinder.apps.tumblelog.models import TumblelogItem


tumblelog_dict = {
    'queryset': TumblelogItem.objects.all().order_by('-pub_date')
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', dict(tumblelog_dict, paginate_by=10), name="homepage"),
    url(r'^tumblelog/?page=(?P<page>[0-9]+)$', 'django.views.generic.list_detail.object_list', dict(tumblelog_dict), name="tumblelog_list"),
    url(r'^tumblelog/','django.views.generic.list_detail.object_list', dict(tumblelog_dict, paginate_by=10), name="tumblelog_home"),
    url(r'^tweets/', include('rewinder.apps.twitter.urls')),
)

urlpatterns += patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^comments/', include('django.contrib.comments.urls.comments')),
    (r'^links/', include('rewinder.apps.delicious.urls')),
    (r'^places/', include('rewinder.apps.geo.urls')),
    (r'^photos/', include('rewinder.apps.flickr.urls')),
    (r'^videos/', include('rewinder.apps.video.urls')),
    (r'^words/', include('rewinder.apps.blog.urls')),
    url(r'^tag/(?P<tag>[-\w]+)/$', 'tag', name='tag_detail'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/gmacgregor/dev/rewinder/site_media'}),
    )
