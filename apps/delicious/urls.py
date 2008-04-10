from django.conf.urls.defaults import *
from rewinder.apps.delicious.models import Bookmark

bookmark_dict = {
    'queryset': Bookmark.objects.all(),
    'date_field': 'saved_date',
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', dict(queryset=Bookmark.objects.all(), paginate_by=10), name='link_list'),
)

urlpatterns += patterns('django.views.generic.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<object_id>\d+)/$', 'object_detail', dict(bookmark_dict, month_format='%m'), name='link_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'archive_day', dict(bookmark_dict, month_format='%m'), name='link_day_archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(bookmark_dict, month_format='%m'), name='link_month_archive'),
    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(bookmark_dict, make_object_list=True), name='link_year_archive'),
)