from django.conf.urls.defaults import *
from rewinder.apps.generic.models import Quote

quote_dict = {
    'queryset': Quote.objects.all(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('',
    url(r'^$', 'rewinder.views.list', {'app': 'generic', 'model': Quote}, name='quote_home'),
)

urlpatterns += patterns('django.views.generic.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(quote_dict, month_format='%m'), name='quote_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'archive_day', dict(quote_dict, month_format='%m'), name='quote_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(quote_dict, month_format='%m'), name='quote_archive_month'),
    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(quote_dict, make_object_list=True), name='quote_archive_year'),
)