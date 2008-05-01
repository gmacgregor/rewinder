from rewinder.apps.video.models import Video
from rewinder.lib.stateful_paginator import DiggPaginator
from rewinder.lib.shortcuts import render_response

def list(request):
    items = Video.objects.all().order_by('-pub_date')
    page = request.GET.get('page', 1)
    paginator = DiggPaginator(items, 10, page=page, body=7, tail=2, padding=3) 
    return render_response(request, 'video/video_list.html', {'page': page, 'paginator': paginator})

