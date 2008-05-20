from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import dispatcher
from django.db.models import signals
from django.contrib.sitemaps import ping_google
from tagging.fields import TagField
from template_utils.markup import formatter
from typogrify.templatetags.typogrify import typogrify
from threadedcomments.moderation import CommentModerator, moderator

from rewinder.apps.geo.models import Place
from rewinder.apps.video.models import Video
from rewinder.apps.generic.models import Quote, Source, Person
from rewinder.apps.delicious.models import Bookmark
#from rewinder.apps.tumblelog.models import TumblelogItem
#from rewinder.lib.signals import create_tumblelog_item, kill_tumblelog_item

import os

PUBLISHED_STATUS = 1
DRAFT_STATUS = 2
EMBARGO_STATUS = 3

class PublishedArticlesManager(models.Manager):
    def get_query_set(self):
        qs = super(PublishedArticlesManager, self).get_query_set()
        return qs.filter(status__exact=PUBLISHED_STATUS).order_by('-pub_date').select_related()


class DraftArticlesManager(models.Manager):
    def get_query_set(self):
        qs = super(DraftArticlesManager, self).get_query_set()
        return qs.filter(status__exact=DRAFT_STATUS).order_by('-pub_date').select_related()


class Category(models.Model):
    title               = models.CharField(u'Title', max_length=200,)
    slug                = models.SlugField(max_length=200, prepopulate_from=('title',), help_text=u'Automatically built from category title.', unique=True)
    description         = models.TextField(help_text=u'A short description of the category. Use Markdown syntax for HTML formatting. Optional.', blank=True)
    description_html    = models.TextField(blank=True, null=True, editable=False)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def save(self):
        if self.description:
            self.description_html =  typogrify(formatter(self.description))
        super(Category, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog_category_detail', (), {'slug': self.slug})
     
    def _get_live_entries(self):
        '''
        Returns Articles in this Category with status of "published".
        Access this through the property ``live_entry_set``.
        '''
        from rewinder.apps.blog.models import Article
        return self.entry_set.filter(status__exact=Article.PUBLISHED_STATUS)
    
    live_entry_set = property(_get_live_entries)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']
    
    class Admin:
        pass


class Article(models.Model):
    PUBLICATION_CHOICES = (
        (PUBLISHED_STATUS, 'Live on site'),
        (DRAFT_STATUS, 'Draft'),
    )
    
    #publication details
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField('Publication Date')
    author              = models.ForeignKey(User)
    status              = models.IntegerField(max_length=1, choices=PUBLICATION_CHOICES, radio_admin=True, default=1)
    geography           = models.ForeignKey(Place, null=True, blank=True)
    categories          = models.ManyToManyField(Category, filter_interface=models.HORIZONTAL, null=True, blank=True)
    featured            = models.BooleanField('Featured article?', default=False)
    tags                = TagField()
    enable_comments     = models.BooleanField(default=True)
    
    #managers
    objects             = models.Manager()
    published_articles  = PublishedArticlesManager()
    draft_articles      = DraftArticlesManager()
    
    #copy
    headline            = models.CharField(max_length=255, unique_for_date='pub_date')
    slug                = models.SlugField(max_length=255, prepopulate_from=('headline',), help_text='Automatically built from article headline.', unique=True) 
    teaser              = models.TextField(blank=True, help_text=u'Use Markdown syntax for HTML formatting.')
    html_teaser         = models.TextField(blank=True, null=True)
    summary             = models.TextField(blank=True, help_text=u'Use Markdown syntax for HTML formatting.')
    html_summary        = models.TextField(blank=True, null=True)
    body                = models.TextField(blank=True, help_text=u'Use Markdown syntax for HTML formatting.')
    html_body           = models.TextField(blank=True, null=True)
    pull_quote          = models.TextField(blank=True, help_text=u'Use Markdown syntax for HTML formatting.')
    html_pull_quote     = models.TextField(blank=True, null=True)
    
    #media -- this should, at some point, include a photo gallery
    articles            = models.ManyToManyField('self', filter_interface=models.HORIZONTAL, null=True, blank=True)
    links               = models.ManyToManyField(Bookmark, filter_interface=models.HORIZONTAL, null=True, blank=True)
    videos              = models.ManyToManyField(Video, filter_interface=models.HORIZONTAL, null=True, blank=True)
    quotes              = models.ManyToManyField(Quote, filter_interface=models.HORIZONTAL, null=True, blank=True)
    
    #related models
    people              = models.ManyToManyField(Person, filter_interface=models.HORIZONTAL, null=True, blank=True)
    sources             = models.ManyToManyField(Source, filter_interface=models.HORIZONTAL, null=True, blank=True)
    
    #images
    #lead_image          = models.ImageField(upload_to='img/articles/lead/%Y%m%d/', blank=True)
    lead_image          = models.ImageField(upload_to='img/articles/lead/%Y%m%d/', blank=True)
    remove_lead         = models.BooleanField(u'Remove lead image?')
    lead_caption        = models.CharField(max_length=255, blank=True, help_text=u'Use Markdown syntax for HTML formatting.')
    html_lead_caption   = models.CharField(max_length=255, blank=True)
    sidebar_image       = models.ImageField(upload_to='img/articles/sidebar/%Y%m%d/', blank=True)
    remove_sidebar      = models.BooleanField(u'Remove sidebar image?')
    sidebar_caption     = models.CharField(max_length=255, blank=True, help_text=u'Use Markdown syntax for HTML formatting.')
    html_sidebar_caption= models.CharField(max_length=255, blank=True)
    inline_image        = models.ImageField(upload_to='img/articles/inline/%Y%m%d/', blank=True)
    remove_inline       = models.BooleanField(u'Remove inline image?')
    inline_caption      = models.CharField(max_length=255, blank=True, help_text=u'Use Markdown syntax for HTML formatting.')
    html_inline_caption = models.CharField(max_length=255, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.headline
    
    def save(self):
        self = self._process_markup()
        self = self._process_images()
        super(Article, self).save()
    
    def delete(self):
        images = [self.get_lead_image_filename(), self.get_sidebar_image_filename(), self.get_inline_image_filename()]
        for i in images:
            try:
                os.remove(i)
            except OSError:
                pass
        super(Article, self).delete()
    
    def _next_previous_helper(self, direction):
        return getattr(self, 'get_%s_by_pub_date_date' % direction)
    
    @property
    def get_next(self):
        return self._next_previous_helper('next')
        
    @property
    def get_previous(self):
        return self._next_previous_helper('previous')
    
    def _process_markup(self):
        self.html_teaser =  typogrify(formatter(self.teaser))
        self.html_summary =  typogrify(formatter(self.summary))
        self.html_body =  typogrify(formatter(self.body))
        self.html_pull_quote =  typogrify(formatter(self.pull_quote))
        self.html_lead_caption =  typogrify(formatter(self.lead_caption))
        self.html_sidebar_caption =  typogrify(formatter(self.sidebar_caption))
        self.html_inline_caption =  typogrify(formatter(self.inline_caption))
        return self
    
    def _process_images(self):
        if self.remove_lead:
            try:
                os.remove(self.get_lead_image_filename())
            except OSError:
                # most likely that image doesn't exist
                pass
            self.lead_image, self.lead_caption, self.html_lead_caption = '', '', ''
        if self.remove_sidebar:
            try:
                os.remove(self.get_sidebar_image_filename())
            except OSError:
                pass
            self.sidebar_image, self.sidebar_caption, self.html_sidebar_caption = '', '', ''
        if self.remove_inline:
            try:
                os.remove(self.get_inline_image_filename())
            except OSError:
                pass
            self.inline_image, self.inline_caption, self.html_inline_caption = '', '', ''
        self.remove_lead, self.remove_sidebar, self.remove_inline = False, False, False
        return self
    
    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', (), {
            'year': self.pub_date.year,
            'month': str(self.pub_date.month).zfill(2),
            'day': str(self.pub_date.day).zfill(2),
            'slug': self.slug,
        })
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']
    
    class Admin:
        date_hierarchy = 'pub_date'
        fields = (
            ('Publication details', {'fields': ('pub_date', 'headline', 'slug', 'geography')}),
            ('Author', {'fields': ('author',)}),
            ('Article Activity', {'fields': ('status', 'enable_comments',)}),
            ('Categorization', {'fields': ('categories', 'tags', 'featured',)}),
            ('Brief', {'fields': ('summary', 'teaser', 'pull_quote',)}),
            ('Entry', {'fields': ('body',)}),
            ('Related Material', {'fields': ('articles', 'links', 'videos', 'quotes',), 'classes': 'collapse'}),
            ('Images', {'fields': ('lead_image', 'remove_lead', 'lead_caption', 'sidebar_image', 'remove_sidebar', 'sidebar_caption', 'inline_image', 'remove_inline', 'inline_caption',), 'classes': 'collapse'}),
            ('Relevant People, Sources', {'fields': ('people', 'sources',), 'classes': 'collapse'}),
        )
        
        list_display    = ('headline', 'pub_date', 'last_modified', 'status', 'enable_comments', 'author')
        list_filter     = ['pub_date', 'author', 'status', 'categories', 'featured']
        search_fields   = ['headline', 'summary', 'body']
        date_hierarchy  = 'pub_date'


class ArticleModerator(CommentModerator):
    akismet = settings.COMMENTS_AKISMET
    auto_moderate_field = 'pub_date'
    moderate_after = settings.COMMENTS_MODERATE_AFTER
    email_notification = settings.COMMENTS_EMAIL
    enable_field = settings.COMMENTS_ENABLE_FIELD
moderator.register(Article, ArticleModerator)


#dispatcher.connect(create_tumblelog_item, sender=Article, signal=signals.post_save)
#dispatcher.connect(kill_tumblelog_item, sender=Article, signal=signals.post_delete)
