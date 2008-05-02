from django.conf.urls.defaults import *
from rewinder.apps.delicious.models import Bookmark

bookmark_dict = {
    'queryset': Bookmark.objects.all(),
    'date_field': 'saved_date',
    'month_format': '%m',
}

bookmark_archive_dict = {
    'queryset': Bookmark.objects.all(),
    'date_field': 'saved_date',   
}

urlpatterns = patterns('',
    url(r'^$', 'rewinder.views.list', {'app': 'delicious', 'model': Bookmark, 'ordering': '-saved_date'}, name='bookmark_home'),
)

urlpatterns += patterns('django.views.generic.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(bookmark_dict), name='bookmark_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'archive_day', dict(bookmark_dict), name='bookmark_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(bookmark_dict), name='bookmark_archive_month'),
    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(bookmark_archive_dict, make_object_list=True), name='bookmark_archive_year'),
)