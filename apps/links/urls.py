from django.conf.urls.defaults import *
from syncr.delicious.models import Bookmark

bookmark_dict = {
    'queryset': Bookmark.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', dict(bookmark_dict, paginate_by=10), name='link_list'),
    url(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', dict(bookmark_dict), name='link_detail'),
)