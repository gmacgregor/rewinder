from django.db import models
from tagging.fields import TagField
from template_utils.markup import formatter

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


class Quote(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField('Publication Date')
    author              = models.ForeignKey('Person', null=True, blank=True)
    source              = models.ForeignKey(Source)
    url                 = models.URLField(u'URL', blank=True, help_text=u'Optional.', verify_exists=False)
    text                = models.TextField()
    html_text           = models.TextField(blank=True)
    rating              = models.CharField(max_length=20, choices=RATING_CHOICES, blank=True, help_text=u'Optional')
    tags                = TagField()
    
    def __unicode__(self):
        return u'%s' % self.text
    
    def save(self):
        self.html_text = formatter(self.text)
            
    class Admin:
        list_display    = ('title', 'authour', 'source', 'url')
        search_fields   = ['title', 'description', 'url', 'tags']


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