from django.conf.urls.defaults import *
from rewinder.apps.tumblelog.models import TumblelogItem

log_dict = {
    'queryset': TumblelogItem.objects.all(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('',
    url(r'^$', 'rewinder.views.list', {'app': 'tumblelog', 'model': TumblelogItem}, name="tumblelog_home"),
)

#urlpatterns += patterns('django.views.generic.date_based',
#    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'archive_day', dict(log_dict, month_format='%m'), name='tumblelog_archive_day'),
#    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(log_dict, month_format='%m'), name='tumblelog_archive_month'),
#    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(log_dict, make_object_list=True), name='tumblelog_archive_year'),
#)

urlpatterns += patterns('rewinder.apps.tumblelog.views',
    url(r'^(?P<year>\d{4})/$', 'items_by_year')
)