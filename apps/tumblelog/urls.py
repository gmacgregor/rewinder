from django.conf.urls.defaults import *
from rewinder.apps.tumblelog.models import TumblelogItem

tumblelog_dict = {
    'queryset': TumblelogItem.objects.all().order_by('-pub_date')
}

urlpatterns = patterns('',
    url(r'^tumblelog/?page=(?P<page>[0-9]+)$', 'django.views.generic.list_detail.object_list', dict(tumblelog_dict), name="tumblelog_list"),
    url(r'^tumblelog/','django.views.generic.list_detail.object_list', dict(tumblelog_dict, paginate_by=10), name="tumblelog_home"),
)