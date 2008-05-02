from rewinder.lib.stateful_paginator import DiggPaginator
from rewinder.lib.shortcuts import render_response

def list(request, app, model, ordering='-pub_date'):
    """
    I love you, Django!
    """
    items = model.objects.all().order_by('%s' % ordering)
    page = request.GET.get('page', 1)
    paginator = DiggPaginator(items, 15, page=page, body=7, tail=2, padding=3)
    template_name = '%s/%s_list.html' % (app.lower(), model.__name__.lower())
    return render_response(request, template_name, {'page': page, 'paginator': paginator})