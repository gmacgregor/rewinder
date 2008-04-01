from django.conf.urls.defaults import *

home_dict = {
    'template': 'home.html' 
}

urlpatterns = patterns('',
    #homepage
    #(r'^$', 'django.views.generic.simple.direct_to_template', home_dict),
    (r'^$', 'rewinder.apps.blog.views.blog_home'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^comments/', include('django.contrib.comments.urls.comments')),
    (r'^blog/', include('rewinder.apps.blog.urls')),
    (r'^places/', include('rewinder.apps.places.urls')),
    (r'^videos/', include('rewinder.apps.video.urls')),
    (r'^photos/', include('rewinder.apps.photos.urls')),
    (r'^quirps/', include('rewinder.apps.quirp.urls')),
    (r'^links/', include('rewinder.apps.links.urls')),
    url(r'^tag/(?P<tag>[-\w]+)/$', 'tag', name='tag_detail'),
)
