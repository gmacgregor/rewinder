from tagging.models import Tag, TaggedItem
from rewinder.lib.stateful_paginator import DiggPaginator
from rewinder.lib.shortcuts import render_response
from rewinder.apps.blog.models import Article
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.video.models import Video
from rewinder.apps.flickr.models import Photo
from rewinder.apps.twitter.models import Tweet


def list(request, app, model, ordering='-pub_date'):
    ctx = None
    items = model.objects.all().order_by('%s' % ordering)
    if model.__name__.lower() == "tumblelogitem":
        links = Bookmark.objects.count()
        photos = Photo.sixminutes.all().count()
        videos = Video.objects.count()
        tweets = Tweet.objects.count()
        ctx = {'total': items.count(), 'links': links, 'photos': photos, 'videos': videos, 'tweets': tweets}
    page = request.GET.get('page', 1)
    paginator = DiggPaginator(items, 10, page=page, body=7, tail=2, padding=3)
    template_name = '%s/%s_list.html' % (app.lower(), model.__name__.lower())
    return render_response(request, template_name, {'page': page, 'paginator': paginator, 'extra': ctx})

def all_tags(request):
    return render_response(request, 'tag/tag_list.html')

def tag_detail(request, tag):
    articles = TaggedItem.objects.get_by_model(Article, tag)
    links = TaggedItem.objects.get_by_model(Bookmark, tag)
    videos = TaggedItem.objects.get_by_model(Video, tag)
    photos = TaggedItem.objects.get_by_model(Photo, tag)
    count = articles.count() + links.count() + videos.count() + photos.count() 
    tag_dict = {
        'tag': tag,
        'total': count,
        'articles': articles,
        'links': links,
        'videos': videos,
        'photos': photos,
    }
    return render_response(request, 'tag/tag_detail.html', tag_dict)