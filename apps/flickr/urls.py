from django.conf.urls.defaults import *
from rewinder.apps.flickr.models import Photo

photo_dict = {
    'queryset': Photo.objects.all(),
    'date_field': 'taken_date',
}

urlpatterns = patterns('django.views.generic.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<object_id>\d+)/$', 'object_detail', dict(photo_dict, month_format='%m', template_object_name='photo'), name='photo_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(photo_dict, month_format='%m'), name='photo_month_archive'),
    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(photo_dict, make_object_list=True), name='photo_year_archive'),
    url(r'^$', 'archive_index', dict(photo_dict, num_latest=5), name='photo_home'),
)