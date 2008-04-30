from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list
from django.template import RequestContext
from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.lib.stateful_paginator import DiggPaginator

def list(request):
    items = TumblelogItem.objects.all()
    page = request.GET.get('page', 1)
    paginator = DiggPaginator(items, 15, page=page, body=7, tail=2, padding=3) 
    return render_to_response('tumblelog/tumblelogitem_list.html',
        {'page': page, 'paginator': paginator},
        context_instance=RequestContext(request))
