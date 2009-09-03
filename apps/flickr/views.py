from rewinder.apps.flickr.models import Photo, FavoriteList
from rewinder.lib.stateful_paginator import DiggPaginator
from rewinder.lib.shortcuts import render_response

def list(request):
    items = Photo.sixminutes.all()
    page = request.GET.get('page', 1)
    paginator = DiggPaginator(items, 10, page=page, body=7, tail=2, padding=3) 
    return render_response(request, 'flickr/photo_list.html', {'page': page, 'paginator': paginator})

def faves(request):
    faves = FavoriteList.objects.get(owner='sixminutes').photos.all()
    return render_response(request, 'flickr/photo_faves.html', {'photos': faves})
