from django.conf.urls.defaults import *
from rewinder.apps.video.models import Video

video_dict = {
    'queryset': Video.objects.all().order_by('-pub_date'),
    'date_field': 'pub_date',
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', dict(queryset=Video.objects.all().order_by('-pub_date'), paginate_by=10), name='video_list'),
)

urlpatterns += patterns('django.views.generic.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(video_dict, month_format='%m'), name="video_detail"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(video_dict, month_format='%m'), name="video_month_detail"),
    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(video_dict, make_object_list=True), name="video_year_detail"),
)