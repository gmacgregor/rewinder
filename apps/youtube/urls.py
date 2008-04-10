from django.conf.urls.defaults import *
from rewinder.apps.youtube.models import Video


video_dict = {
    'queryset': Video.objects.all(),
    'paginate_by': 50,
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', dict(video_dict), name='video_list'),
)

#urlpatterns += patterns('django.views.generic.date_based',
#    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(article_dict, month_format='%m', template_object_name='article'), name='blog_entry_detail'),
#    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(article_dict, month_format='%m'), name='blog_month_archive'),
#    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(article_dict, make_object_list=True), name='blog_year_archive'),
#    url(r'^$', 'archive_index', dict(article_dict, num_latest=5), name='blog_home'),
#)