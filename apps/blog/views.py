from django.shortcuts import render_to_response
from tagging.models import Tag, TaggedItem

from rewinder.apps.blog.models import Article
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.video.models import Video
from rewinder.apps.flickr.models import Photo

def all_tags(request):
    all_tags = Tag.objects.all()
    count = all_tags.count()
    #tags = {}
    #for tag in all_tags:
    #    tags[tag] = tag.items.count()
    #items = tags.items()
    #items = [(v, k) for (k, v) in items]
    #items.sort()
    #items.reverse()
    return render_to_response('tag_list.html', {'tags': all_tags, 'count': count})
    
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