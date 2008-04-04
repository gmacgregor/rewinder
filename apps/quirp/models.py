from django.db import models
from tagging.fields import TagField
from rewinder.apps.links.models import Link

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
        verbose_name_plural = 'Source Categories'
    
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
        return self.name
    
    class Admin:
        list_display    = ('title', 'description', 'url',)
        search_fields   = ['title', 'description', 'url', 'tags']


class Quirp(models.Model):
    created_on          = models.DateTimeField(u'Creation Date', auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField(u'Publication Date', auto_now=True)
    title               = models.CharField(max_length=255)
    slug                = models.SlugField(max_length=255, prepopulate_from=('title',), help_text=u'Automatically built from title', unique=True)
    source              = models.ForeignKey(Source, null=True, blank=True, help_text=u'Optional, but desired')
    description         = models.TextField(blank=True, help_text=u'Optional')
    url                 = models.URLField(u'URL', blank=True, help_text=u'Optional')
    rating              = models.CharField(max_length=20, choices=RATING_CHOICES, blank=True, help_text=u'Optional')
    tags                = TagField()
    enable_comments     = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('quirp_detail', (), {'slug': self.slug})
        
    class Admin:
        list_display    = ('title', 'enable_comments', 'source',)
        list_filter     = ['created_on']
        search_fields   = ['title', 'description', 'url', 'tags']
        date_hierarchy  = 'created_on'


class Quote(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField('Publication Date')
    author              = models.ForeignKey('Person', null=True, blank=True)
    source              = models.ForeignKey(Source)
    text                = models.TextField()
    rating              = models.CharField(max_length=20, choices=RATING_CHOICES, blank=True, help_text=u'Optional')
    
    def __unicode__(self):
        return u'%s' % self.text
    
    class Admin:
        pass


class Person(models.Model):
    """
    Just a first and last name + (optional) brief bio and website
    should suffice.
    
    Could eventually use a PersonType class - occupation, source etc...
    
    """
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    name                = models.CharField(max_length=255)
    slug                = models.SlugField(max_length=255, prepopulate_from=('name',), help_text=u'Automatically built from name', unique=True)
    bio                 = models.TextField(u'Biography', blank=True)
    url                 = models.URLField(u'URL', blank=True, help_text=u'Optopnal')
    
    class Meta:
        verbose_name_plural = 'people'
    
    class Admin:
        pass