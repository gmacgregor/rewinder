from django.conf.urls.defaults import *
from rewinder.apps.tumblelog.models import TumblelogItem


tumblelog_dict = {
    'queryset': TumblelogItem.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', dict(tumblelog_dict, paginate_by=10), name="homepage"),
)

urlpatterns += patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^comments/', include('django.contrib.comments.urls.comments')),
    (r'^words/', include('rewinder.apps.blog.urls')),
    (r'^places/', include('rewinder.apps.places.urls')),
    (r'^videos/', include('rewinder.apps.video.urls')),
    (r'^photos/', include('rewinder.apps.photos.urls')),
    (r'^quirps/', include('rewinder.apps.quirp.urls')),
    (r'^links/', include('rewinder.apps.links.urls')),
    url(r'^tag/(?P<tag>[-\w]+)/$', 'tag', name='tag_detail'),
)
