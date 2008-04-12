from django.db import models
from tagging.fields import TagField
from template_utils.markup import formatter
from rewinder.apps.blog.models import Article
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.flickr.models import Photo
from rewinder.apps.geo.models import Place
from rewinder.apps.twitter.models import Tweet
from rewinder.apps.video.models import Video


RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'), 
)


class SourceCategory(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    title               = models.CharField(max_length=255)
    slug                = models.SlugField(max_length=255, prepopulate_from=('title',), help_text=u'Automatically built from title', unique=True)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        verbose_name_plural = 'Types of sources'
    
    class Admin:
        pass


class Source(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    title               = models.CharField(max_length=255)
    slug                = models.SlugField(max_length=255, prepopulate_from=('title',), help_text=u'Automatically built from title', unique=True)
    description         = models.CharField(max_length=255, blank=True)
    url                 = models.URLField(u'URL', blank=True, help_text=u'Optional', verify_exists=False)
    category            = models.ForeignKey(SourceCategory)
    
    def __unicode__(self):
        return self.title
    
    class Admin:
        list_display    = ('title', 'description', 'url',)
        search_fields   = ['title', 'description', 'url', 'tags']


class Quote(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField('Publication Date')
    author              = models.ForeignKey('Person', null=True, blank=True)
    source              = models.ForeignKey(Source)
    url                 = models.URLField(u'URL', blank=True, help_text=u'Optional.', verify_exists=False)
    text                = models.TextField()
    html_text           = models.TextField(blank=True, editable=False)
    rating              = models.CharField(max_length=20, choices=RATING_CHOICES, blank=True, help_text=u'Optional')
    tags                = TagField()
    enable_comments     = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s' % self.text
    
    def save(self):
        self.html_text = formatter(self.text)
            
    class Admin:
        list_display    = ('text', 'author', 'source', 'url')
        search_fields   = ['text', 'description']


class Person(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    name                = models.CharField(max_length=255)
    slug                = models.SlugField(max_length=255, prepopulate_from=('name',), help_text=u'Automatically built from name', unique=True)
    bio                 = models.TextField(u'Biography', blank=True, help_text=u'Optional')
    url                 = models.URLField(u'URL', blank=True, help_text=u'Optional')
    
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name_plural = 'people'
    
    class Admin:
        pass


class Series(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    title               = models.CharField(max_length=255)
    slug                = models.SlugField(max_length=255, prepopulate_from=('title',), help_text=u'Automatically built from title', unique=True)
    articles            = models.ManyToManyField(Article, null=True, blank=True, filter_interface=models.HORIZONTAL)
    tweets              = models.ManyToManyField(Tweet, null=True, blank=True, filter_interface=models.HORIZONTAL)
    videos              = models.ManyToManyField(Video, null=True, blank=True, filter_interface=models.HORIZONTAL)
    photos              = models.ManyToManyField(Photo, null=True, blank=True, filter_interface=models.HORIZONTAL)
    bookmarks           = models.ManyToManyField(Bookmark, null=True, blank=True, filter_interface=models.HORIZONTAL)
    quotes              = models.ManyToManyField(Quote, null=True, blank=True, filter_interface=models.HORIZONTAL)
    people              = models.ManyToManyField(Person, null=True, blank=True, filter_interface=models.HORIZONTAL)
    places              = models.ManyToManyField(Place, null=True, blank=True, filter_interface=models.HORIZONTAL)
    enable_comments     - models.BooleanField(default=True)
    
    def __unicode__(self):
        retrun u'%s' % self.title
    
    class Meta:
        verbose_name_plural = 'series'
    
    class Admin:
        pass
