from django.db import models
from tagging.fields import TagField
from rewinder.apps.links.models import Link


SOURCE_CHOICES = (
    (1, 'organization'),
    (2, 'publication'),
    (3, 'newspaper'),
    (4, 'website'),
    (5, 'television show'),
    (6, 'movie'),
    (7, 'radio'),
    (8, 'person'),
    (9, 'event'),
)

RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'), 
)

class Source(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    name                = models.CharField(max_length=255)
    slug                = models.SlugField(max_length=255, prepopulate_from=('name',), help_text=u'Automatically built from name', unique=True)
    description         = models.CharField(max_length=255, blank=True)
    url                 = models.URLField(u'URL', blank=True, help_text=u'Optional', verify_exists=False)
    type                = models.CharField(max_length=10, choices=SOURCE_CHOICES, radio_admin=True, default=4)
    tags                = TagField()
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        list_display    = ('name', 'description', 'url',)
        search_fields   = ['name', 'description', 'url', 'tags']


class Quirp(models.Model):
    created_on          = models.DateTimeField(u'Creation Date', auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField(u'Publication Date', auto_now=True)
    title               = models.CharField(max_length=255)
    slug                = models.SlugField(max_length=255, prepopulate_from=('title',), help_text=u'Automatically built from title', unique=True)
    source              = models.ForeignKey(Source, null=True, blank=True, help_text=u'Optional')
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


class Person(models.Model):
    """
    Just a first and last name + (optional) brief bio and website
    should suffice.
    
    Could eventually use a PersonType class - occupation, source etc...
    
    """
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    firstname           = models.CharField(u'First name', max_length=20)
    lastname            = models.CharField(u'Last name', max_length=30)
    bio                 = models.TextField(u'Who is this person?', help_text=u'How do you know them? Do you know them at all? What do they do? How are the involved?', blank=True)
    url                 = models.URLField(u'URL', blank=True, help_text=u'Optopnal')
    
    class Meta:
        verbose_name_plural = 'people'
    
    class Admin:
        pass