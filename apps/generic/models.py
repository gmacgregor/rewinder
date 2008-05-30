from django.db import models
from django.conf import settings
from tagging.fields import TagField
from template_utils.markup import formatter
from typogrify.templatetags.typogrify import typogrify
from comment_utils.moderation import CommentModerator, moderator

from django.dispatch import dispatcher
from django.db.models import signals
from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.lib.signals import create_tumblelog_item, kill_tumblelog_item

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
    #author              = models.ForeignKey('Person', null=True, blank=True)
    #source              = models.ForeignKey(Source)
    url                 = models.URLField(u'URL', blank=True, help_text=u'Optional.', verify_exists=False)
    text                = models.TextField(help_text=u'Use Markdown syntax for HTML formatting.')
    slug                = models.SlugField(null=True)
    html_text           = models.TextField(blank=True, editable=False)
    rating              = models.CharField(max_length=20, choices=settings.RATING_CHOICES, blank=True, help_text=u'Optional')
    credit              = models.CharField(max_length=255, null=True, blank=True)
    tags                = TagField()
    enable_comments     = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s' % self.text
    
    @models.permalink
    def get_absolute_url(self):
        return ('quote_detail', (), {
            'year': self.pub_date.year,
            'month': str(self.pub_date.month).zfill(2),
            'day': str(self.pub_date.day).zfill(2),
            'slug': self.slug,
        })
    
    def save(self):
        self._process_markup()
        super(Quote, self).save()
    
    def _process_markup(self):
        self.html_text =  typogrify(formatter(self.text))
    
    class Admin:
        list_display    = ('text', 'url', 'enable_comments')
        search_fields   = ['text', 'credit']


class QuoteModerator(CommentModerator):
    akismet = settings.COMMENTS_AKISMET
    auto_moderate_field = 'pub_date'
    moderate_after = settings.COMMENTS_MODERATE_AFTER
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
        
dispatcher.connect(create_tumblelog_item, sender=Quote, signal=signals.post_save)
dispatcher.connect(kill_tumblelog_item, sender=Quote, signal=signals.post_delete)