from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list
from tagging.models import Tag, TaggedItem

from rewinder.apps.blog.models import Article
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.video.models import Video
from rewinder.apps.flickr.models import Photo

def all_tags(request):
    tags = Tag.objects.all().exclude(name__icontains='for:')
    return render_to_response('tags_list.html', {'tags': tags})

def tag_detail(request, tag):
    articles = TaggedItem.objects.get_by_model(Article, tag)
    links = TaggedItem.objects.get_by_model(Bookmark, tag)
    videos = TaggedItem.objects.get_by_model(Video, tag)
    photos = TaggedItem.objects.get_by_model(Photo, tag)
    tag_dict = {
        'tag': tag,
        'articles': articles,
        'links': links,
        'videos': videos,
        'photos': photos,
    }
    return render_to_response('tag_detail.html', tag_dict)
    