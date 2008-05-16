from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.lib.shortcuts import render_response
from datetime import datetime

def year_group(request, year):
    logs = TumblelogItem.objects.filter(pub_date__year=year).order_by('-pub_date')
    date = datetime(int(year),1,1)
    return render_response(request, 'tumblelog/year_group.html', {'entries': logs, 'showing_date': date})

def month_group(request, year, month):
    logs = TumblelogItem.objects.filter(pub_date__year=year).filter(pub_date__month=month).order_by('-pub_date')
    date = datetime(int(year),int(month),1)
    return render_response(request, 'tumblelog/month_group.html', {'entries': logs, 'showing_date': date})

def day_group(request, year, month, day):
    logs = TumblelogItem.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).order_by('-pub_date')
    date = datetime(int(year),int(month),int(day))
    return render_response(request, 'tumblelog/day_group.html', {'entries': logs, 'showing_date': date})
    