from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.lib.stateful_paginator import DiggPaginator
from rewinder.lib.shortcuts import render_response

def list(request):
    items = TumblelogItem.objects.all()
    page = request.GET.get('page', 1)
    paginator = DiggPaginator(items, 15, page=page, body=7, tail=2, padding=3) 
    return render_response(request, 'tumblelog/tumblelogitem_list.html', {'page': page, 'paginator': paginator})
