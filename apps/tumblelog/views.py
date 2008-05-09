from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.lib.shortcuts import render_response

entries = {
    1: {'name': 'January', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '01'},
    2: {'name': 'February', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '02'},
    3: {'name': 'March', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '03'},
    4: {'name': 'April', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '04'},
    5: {'name': 'May', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '05'},
    6: {'name': 'June', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '06'},
    7: {'name': 'July', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '07'},
    8: {'name': 'August', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '08'},
    9: {'name': 'September', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '09'},
    10: {'name': 'October', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '10'},
    11: {'name': 'November', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '11'},
    12: {'name': 'December', 'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'month': '12'},
}

days = {
    1: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '01'},
    2: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '02'},
    3: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '03'},
    4: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '04'},
    5: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '05'},
    6: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '06'},
    7: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '07'},
    8: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '08'},
    9: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '09'},
    10: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '10'},
    11: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '11'},
    12: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '12'},
    13: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '13'},
    14: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '14'},
    15: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '15'},
    16: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '16'},
    17: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '17'},
    18: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '18'},
    19: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '19'},
    20: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '20'},
    21: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '21'},
    22: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '22'},
    23: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '23'},
    24: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '24'},
    25: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '25'},
    26: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '26'},
    27: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '27'},
    28: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '28'},
    29: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '29'},
    30: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '30'},
    31: {'links': None, 'tweets': None, 'videos': None, 'photos': None, 'content': '', 'day': '31'},
}

def has_content(entries):
    if len(entries['links']) > 0 or len(entries['tweets']) > 0 or len(entries['videos']) > 0 or len(entries['photos']) > 0:
        return True
    return False

def filter(entries, logs):
    for m in entries:
        entries[m]['content'] = None
        entries[m]['links'] = logs.filter(content_type__name="bookmark").filter(pub_date__month=int(m))
        entries[m]['tweets'] = logs.filter(content_type__name="tweet").filter(pub_date__month=int(m))
        entries[m]['videos'] = logs.filter(content_type__name="video").filter(pub_date__month=int(m))
        entries[m]['photos'] = logs.filter(content_type__name="photo").filter(pub_date__month=int(m))
        if has_content(entries[m]):
            entries[m]['content'] = 1
    return entries

def day_filter(entries, logs):
    for d in days:
        days[d]['content'] = None
        days[d]['links'] = logs.filter(content_type__name="bookmark").filter(pub_date__day=int(d))
        days[d]['tweets'] = logs.filter(content_type__name="tweet").filter(pub_date__day=int(d))
        days[d]['videos'] = logs.filter(content_type__name="video").filter(pub_date__day=int(d))
        days[d]['photos'] = logs.filter(content_type__name="photo").filter(pub_date__day=int(d))
        if has_content(days[d]):
            days[d]['content'] = 1
    return days

def items_by_year(request, year):
    logs = TumblelogItem.objects.filter(pub_date__year=year).order_by('pub_date')
    year_items = filter(entries, logs)
    return render_response(request, 'tumblelog/year.html', {'entries': year_items, 'year': year })

def items_by_month(request, year, month):
    month = int(month)
    logs = TumblelogItem.objects.filter(pub_date__year=year).filter(pub_date__month=month).order_by('pub_date')
    day_items = day_filter(days, logs)
    return render_response(request, 'tumblelog/month.html', {'entries': day_items, 'year': year, 'month': month, 'month_name': entries[month]['name']})

#def items_by_day(request, year, month, day):
#    month = int(month)
#    day = int(day)
#    logs = TumblelogItem.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).order_by('pub_date')
#    day_items = day_filter(entries, logs)
#    return render_response(request, 'tumblelog/day.html', {'entries': day_items, 'year': year, 'month': str(month).zfill(2), 'day': day})


def group(request, year):
    from itertools import groupby
    logs = TumblelogItem.objects.filter(pub_date__year=year).order_by('pub_date')
    return render_response(request, 'tumblelog/test.html', {'entries': logs})
    
    