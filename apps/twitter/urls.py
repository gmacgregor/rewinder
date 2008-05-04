from django.conf.urls.defaults import *
from rewinder.apps.twitter.models import Tweet

tweet_dict = {
    'queryset': Tweet.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', 'rewinder.views.list', {'app': 'twitter', 'model': Tweet, 'ordering': '-pub_time'}, name="tweet_home"),
)

urlpatterns += patterns('django.views.generic.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<object_id>\d+)/$', 'object_detail', dict(tweet_dict, date_field='pub_time', month_format='%m'), name='tweet_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'archive_day', dict(tweet_dict, date_field='pub_time', month_format='%m'), name='tweet_day_archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(tweet_dict, date_field='pub_time', month_format='%m'), name='tweet_month_archive'),
    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(tweet_dict, date_field='pub_time', make_object_list=True), name='tweet_year_archive'),
)
