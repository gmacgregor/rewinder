from tagging.models import Tag, TaggedItem
from rewinder.lib.stateful_paginator import DiggPaginator
from rewinder.lib.shortcuts import render_response
from rewinder.apps.blog.models import Article
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.video.models import Video
from rewinder.apps.flickr.models import Photo

def list(request, app, model, ordering='-pub_date', extra_context=None):
    """
    I love you, Django!
    """
    items = model.objects.all().order_by('%s' % ordering)
    page = request.GET.get('page', 1)
    paginator = DiggPaginator(items, 10, page=page, body=7, tail=2, padding=3)
    template_name = '%s/%s_list.html' % (app.lower(), model.__name__.lower())
    return render_response(request, template_name, {'page': page, 'paginator': paginator, 'extra_context': extra_context})

def all_tags(request):
    all_tags = Tag.objects.all()
    count = all_tags.count()
    tags = {}
    for tag in all_tags:
        tags[tag] = tag.items.count()
    items = tags.items()
    items = [(v, k) for (k, v) in items]
    items.sort()
    items.reverse()
    items = items[:100]
    top_count = items[0][0]
    return render_response(request, 'tag/tag_list.html', {'tags': items, 'total_count': count, 'top_count': top_count})

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
    return render_response(request, 'tag/tag_detail.html', tag_dict)