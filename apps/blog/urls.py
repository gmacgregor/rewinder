from django.conf.urls.defaults import *
from rewinder.apps.blog.models import Article, Category

article_dict = {
    'queryset': Article.published_articles.all(),
    'date_field': 'pub_date',
}

category_dict = {
    'queryset': Category.objects.all(),
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^categories/all/$', 'object_list', dict(category_dict), name='blog_category_list'),
    url(r'^categories/(?P<slug>[-\w]+)/$', 'object_detail', dict(category_dict, template_object_name='category'), name='blog_category_detail'),
)
urlpatterns += patterns('django.views.generic.date_based',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(article_dict, month_format='%m'), name='blog_entry_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(article_dict, month_format='%m'), name='blog_month_archive'),
    url(r'^(?P<year>\d{4})/$', 'archive_year', dict(article_dict, make_object_list=True), name='blog_year_archive'),
    url(r'^$', 'archive_index', dict(article_dict, num_latest=5), name='blog_index'),
)