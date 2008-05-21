from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.lib.shortcuts import render_response
from datetime import datetime

def year_group(request, year):
    date = datetime.strptime(year, "%Y")
    year = date.year
    logs = TumblelogItem.objects.filter(pub_date__year=year).order_by('-pub_date')
    return render_response(request, 'tumblelog/year_group.html', {'entries': logs, 'showing_date': date})

def month_group(request, year, month):
    date = datetime.strptime("%s %s" % (year, month), "%Y %m")
    # this is lame... i must be doing something wrong
    month = date.month
    logs = TumblelogItem.objects.filter(pub_date__year=year, pub_date__month=month).order_by('-pub_date')
    return render_response(request, 'tumblelog/month_group.html', {'entries': logs, 'showing_date': date})

def day_group(request, year, month, day):
    date = datetime.strptime("%s %s %s" % (year, month, day), "%Y %m %d")
    month = date.month
    day = date.day
    logs = TumblelogItem.objects.filter(pub_date__year=year, pub_date__month=month, pub_date__day=day).order_by('-pub_date')
    return render_response(request, 'tumblelog/day_group.html', {'entries': logs, 'showing_date': date})


