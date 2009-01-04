from django.conf.urls.defaults import *
from rewinder.apps.tumblelog.models import TumblelogItem

log_dict = {
    'queryset': TumblelogItem.objects.all(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('',
    url(r'^$', 'rewinder.views.list', {'app': 'tumblelog', 'model': TumblelogItem}, name="tumblelog_home"),
)

urlpatterns += patterns('rewinder.apps.tumblelog.views',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'day_group', name='tumblelog_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'month_group', name='tumblelog_archive_month'),
    url(r'^(?P<year>\d{4})/$', 'year_group', name='tumblelog_archive_year')
)