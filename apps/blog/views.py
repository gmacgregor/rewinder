from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.conf.urls.defaults import *
from rewinder.apps.blog.models import Article

#from django.contrib.auth.models import User

#blog/
def blog_home(request):
	return render_to_response('home.html')
#blog/archive/
def archive_view(request):
	return HttpResponse('This is archive_view')

#blog/2007
def year_view(request, year):
	return HttpResponse('This is year_view')

#blog/2007/09	
def month_view(request, year, month):
	return HttpResponse('This is month_view')

#blog/2007/09/29		
def day_view(request, year, month, day):
	#articles = Article.objects.dates('pub_date', 'year')
	return HttpResponse('This is day_view')

#blog/2007/09/29/article-slug	
def detail_view(request, year, month, day, slug):
	u = User.objects.get(username='test')
	article = get_object_or_404(Article, slug=slug)
	Article.make_new_article(article)
	return HttpResponse('it is done again agan')	