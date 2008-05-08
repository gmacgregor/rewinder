from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.lib.shortcuts import render_response

def items_by_year(request, year):
    logs = TumblelogItem.objects.filter(pub_date__year=year)
    entries = {
        1: {'name': 'Jan', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        2: {'name': 'Feb', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        3: {'name': 'Mar', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        4: {'name': 'Apr', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        5: {'name': 'May', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        6: {'name': 'Jun', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        7: {'name': 'Jul', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        8: {'name': 'Aug', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        9: {'name': 'Sep', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        10: {'name': 'Oct', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        11: {'name': 'Nov', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
        12: {'name': 'Dec', 'links': None, 'tweets':None, 'videos':None, 'photos':None, 'content':False},
    }
    for m in entries:
        entries[m]['links'] = logs.filter(content_type__name="bookmark").filter(pub_date__month=m)
        entries[m]['tweets'] = logs.filter(content_type__name="tweet").filter(pub_date__month=m)
        entries[m]['videos'] = logs.filter(content_type__name="video").filter(pub_date__month=m)
        entries[m]['photos'] = logs.filter(content_type__name="photo").filter(pub_date__month=m)
    #count = logs.count()
    #links = logs.filter(content_type__name="bookmark")
    #tweets = logs.filter(content_type__name="tweet")
    #videos = logs.filter(content_type__name="video")
    #photos = logs.filter(content_type__name="photo")
    #monthly_links = process_entries(links)
    #monthly_tweets = process_entries(tweets)
    #monthly_videos = process_entries(videos)
    #monthly_photos = process_entries(photos)
    #entries = {'year': year, 'count': count, 'links': {'count': links.count(), 'items': monthly_links}, 'tweets': tweets, 'videos': videos, 'photos': photos}
    #months = process_entries(logs)
    return render_response(request, 'tumblelog/year.html', {'entries': entries})