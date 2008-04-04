from rewinder.apps.tumblelog.models import TumblelogItem
from django.shortcuts import render_to_response


def home(request):
    logs = TumblelogItem.objects.all()
    return render_to_response('tumblelog/home.html', {'logs': logs})
