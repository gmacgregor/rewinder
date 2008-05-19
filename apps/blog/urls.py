from django.conf.urls.defaults import *
from rewinder.apps.blog.models import Article, Category

article_dict = {
    'queryset': Article.published_articles.all(),
    'date_field': 'pub_date',
}

category_dict = {
    'queryset': Category.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', 'rewinder.views.list', {'app': 'blog', 'model': Article}, name='blog_home'),
)

urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^categories/all/$', 'object_list', dict(category_dict), name='blog_category_list'),
    url(r'^categories/(?P<slug>[-\w]+)/$', 'object_detail', dict(category_dict, template_object_name='category'), name='blog_category_detail'),
)

urlpatterns += patterns('django.views.generic.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(article_dict, month_format='%m'), name='article_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'archive_day', dict(article_dict, month_format='%m'), name='article_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(article_dict, month_format='%m'), name='article_archive_month'),
    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(article_dict, make_object_list=True), name='article_archive_year'),
)