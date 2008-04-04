from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import dispatcher
from django.db.models import signals

from rewinder.apps.geo.models import Place
from rewinder.apps.video.models import Video
from rewinder.apps.youtube.models import Video as YoutubeVideo
from rewinder.apps.quirp.models import Quirp, Source, Person
from rewinder.apps.delicious.models import Bookmark
from rewinder.apps.tumblelog.models import TumblelogItem

from rewinder.lib.signals import create_article_tumblelog_item

from tagging.fields import TagField

from template_utils.markup import formatter


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
            self.description_html = formatter(self.description)
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
    geography           = models.ForeignKey(Place)
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
    
    #related models
    people              = models.ManyToManyField(Person, filter_interface=models.HORIZONTAL, null=True, blank=True)
    sources             = models.ManyToManyField(Source, filter_interface=models.HORIZONTAL, null=True, blank=True)
    
    #images
    lead_image          = models.ImageField(upload_to='img/articles/lead/%Y%m%d/', blank=True)
    lead_caption        = models.CharField(max_length=255, blank=True)
    sidebar_image       = models.ImageField(upload_to='img/articles/sidebar/%Y%m%d/', blank=True)
    sidebar_caption     = models.CharField(max_length=255, blank=True)
    inline_image        = models.ImageField(upload_to='img/articles/inline/%Y%m%d/', blank=True)
    inline_caption      = models.CharField(max_length=255, blank=True)
    
    #media
    #this should, at some point, include a photo gallery
    articles            = models.ManyToManyField('self', filter_interface=models.HORIZONTAL, null=True, blank=True)
    quirps              = models.ManyToManyField(Quirp, filter_interface=models.HORIZONTAL, null=True, blank=True)
    links               = models.ManyToManyField(Bookmark, filter_interface=models.HORIZONTAL, null=True, blank=True)
    videos              = models.ManyToManyField(Video, filter_interface=models.HORIZONTAL, null=True, blank=True)
    youtube_videos      = models.ManyToManyField(YoutubeVideo, filter_interface=models.HORIZONTAL, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.headline
    
    def save(self):
        '''
        A few things happening here:
            Format teaser, summary, body and pull_quote properly
            
            If this is article has a PUBLISHED_STATUS, make sure it's added to the tumblelog,
            otherwise, try to remove it from the tumblelog (status possibly changed 
            from PUBLISHED_STATUS to DRAFT_STATUS)
        '''
        if self.teaser:
            self.html_teaser = formatter(self.teaser)
        if self.summary:
            self.html_summary = formatter(self.summary)
        if self.body:
            self.html_body = formatter(self.body)
        if self.pull_quote:
            self.html_pull_quote = formatter(self.pull_quote)
        super(Article, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog_entry_detail', (), {
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
            ('Publication details', {'fields': ('pub_date', 'headline', 'slug',)}),
            ('Author', {'fields': ('author',)}),
            ('Article Activity', {'fields': ('status', 'enable_comments',)}),
            ('Brief', {'fields': ('summary', 'teaser', 'pull_quote',), 'classes': 'collapse'}),
            ('Categorization', {'fields': ('categories', 'tags', 'featured',)}),
            ('Entry', {'fields': ('body',)}),
            ('Related Material', {'fields': ('articles', 'links', 'youtube_videos', 'videos', 'quirps',), 'classes': 'collapse'}),
            ('Images and Photos', {'fields': ('lead_image', 'lead_caption', 'sidebar_image', 'sidebar_caption', 'inline_image', 'inline_caption',), 'classes': 'collapse'}),
            ('Metadata: Relevant People, Places and Sources', {'fields': ('places', 'people', 'sources',), 'classes': 'collapse'}),
        )
        
        list_display    = ('headline', 'pub_date', 'last_modified', 'status', 'enable_comments', 'author')
        list_filter     = ['pub_date', 'author', 'status', 'categories', 'featured']
        search_fields   = ['headline', 'summary', 'body']
        date_hierarchy  = 'pub_date'

dispatcher.connect(create_article_tumblelog_item, sender=Article, signal=signals.post_save)