from django.db import models
from django.conf import settings
from tagging.fields import TagField
from template_utils.markup import formatter
from comment_utils.moderation import CommentModerator, moderator


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
    rating              = models.CharField(max_length=20, choices=settings.RATING_CHOICES, blank=True, help_text=u'Optional')
    tags                = TagField()
    enable_comments     = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s' % self.text
    
    def save(self):
        self.html_text = formatter(self.text)
            
    class Admin:
        list_display    = ('text', 'author', 'source', 'url')
        search_fields   = ['text', 'description']


class QuoteModerator(CommentModerator):
    akismet = settings.COMMENTS_AKISMET
    auto_close_field = 'pub_date'
    close_after = settings.COMMENTS_CLOSE_AFTER
    email_notification = settings.COMMENTS_EMAIL
    enable_field = settings.COMMENTS_ENABLE_FIELD
moderator.register(Quote, QuoteModerator)


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
    image               = models.ImageField(upload_to='img/series/', blank=True)
    enable_comments     = models.BooleanField(default=True)
   
    def __unicode__(self):
        return u'%s' % self.title
   
    class Meta:
        verbose_name_plural = 'series'
    
    class Admin:
        pass