from rewinder.apps.delicious.models import Bookmark
from rewinder.lib.stateful_paginator import DiggPaginator
from rewinder.lib.shortcuts import render_response

def list(request):
    items = Bookmark.objects.all().order_by('-saved_date')
    page = request.GET.get('page', 1)
    paginator = DiggPaginator(items, 10, page=page, body=7, tail=2, padding=3) 
    return render_response(request, 'delicious/bookmark_list.html', {'page': page, 'paginator': paginator})
