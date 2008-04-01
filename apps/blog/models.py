from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from tagging.models import Tag
from tagging.fields import TagField
from rewinder.apps.places.models import Place
from rewinder.apps.video.models import Video
from rewinder.apps.quirp.models import Quirp, Source, Person
from rewinder.apps.links.models import Link
from markdown import markdown

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

class EmbargoedArticlesManager(models.Manager):
    def get_query_set(self):
        qs = super(EmbargoedArticlesManager, self).get_query_set()
        return qs.filter(status__exact=EMBARGO_STATUS).order_by('-pub_date').select_related()

class Category(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    title               = models.CharField(u'Title', max_length=200,)
    slug                = models.SlugField(max_length=255, prepopulate_from=('title',), help_text=u'Automatically built from category title.', unique=True)
    
    def __unicode__(self):
        return '%s' % self.title
    
    class Admin:
        pass

class Article(models.Model):
    '''
    A blog article model. Entries that used HTML must be marked up via Python Markdown.
    '''
    PUBLICATION_CHOICES = (
        (PUBLISHED_STATUS, 'Live on site'),
        (DRAFT_STATUS, 'Draft'),
        (EMBARGO_STATUS, 'Embargo'),
    )
    
    #publication details
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField('Publication Date')
    author              = models.ForeignKey(User)
    status              = models.IntegerField(max_length=1, choices=PUBLICATION_CHOICES, radio_admin=True, default=1)
    category            = models.ForeignKey(Category)
    
    #managers
    objects             = models.Manager()
    published_articles  = PublishedArticlesManager()
    draft_articles      = DraftArticlesManager()
    embargoed_articles  = EmbargoedArticlesManager()
    
    #copy
    headline            = models.CharField(max_length=255, unique_for_date='pub_date')
    slug                = models.SlugField(max_length=255, prepopulate_from=('headline',), help_text='Automatically built from article headline.', unique=True) 
    teaser              = models.TextField(blank=True)
    summary             = models.TextField(blank=True)
    body                = models.TextField(blank=True, help_text=u'Use Markdown syntax for HTML formatting.')
    html_body           = models.TextField(blank=True, null=True)
    pull_quote          = models.TextField(blank=True)
    
    #related models
    places              = models.ManyToManyField(Place, filter_interface=models.HORIZONTAL, null=True, blank=True)
    people              = models.ManyToManyField(Person, filter_interface=models.HORIZONTAL, null=True, blank=True)
    sources             = models.ManyToManyField(Source, filter_interface=models.HORIZONTAL, null=True, blank=True)
    
    #images
    lead_image          = models.ImageField(upload_to='img/articles/lead/%Y/%m/%d/', blank=True)
    lead_caption        = models.CharField(max_length=255, blank=True)
    sidebar_image       = models.ImageField(upload_to='img/articles/sidebar/%Y/%m/%d/', blank=True)
    sidebar_caption     = models.CharField(max_length=255, blank=True)
    inline_image        = models.ImageField(upload_to='img/articles/inline/%Y/%m/%d/', blank=True)
    inline_caption      = models.CharField(max_length=255, blank=True)
    
    #media
    #this should, at some point, include a photo gallery
    articles            = models.ManyToManyField('self', filter_interface=models.HORIZONTAL, null=True, blank=True)
    quirps              = models.ManyToManyField(Quirp, filter_interface=models.HORIZONTAL, null=True, blank=True)
    links               = models.ManyToManyField(Link, filter_interface=models.HORIZONTAL, null=True, blank=True)
    videos              = models.ManyToManyField(Video, filter_interface=models.HORIZONTAL, null=True, blank=True)
    tags                = TagField()
    enable_comments     = models.BooleanField(default=True)
    
    def __unicode__(self):
        return '%s' % self.headline
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)
    
    def save(self):
        self.html_body = markdown(self.body)
        super(Article, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog_entry_detail', (), {
            'year': self.pub_date.year,
            'month': str(self.pub_date.month).zfill(2),
            'day': str(self.pub_date.day).zfill(2),
            'slug': self.slug,
        })
    
    class Admin:
        fields = (
            ('Publication details', {'fields': ('pub_date', 'headline', 'slug', 'category')}),
            ('Author', {'fields': ('author',)}),
            ('Brief', {'fields': ('summary', 'teaser', 'pull_quote',), 'classes': 'collapse'}),
            ('Entry', {'fields': ('body', 'tags',)}),
            ('Related Articles, Links, Videos, Quirps', {'fields': ('articles', 'links', 'videos', 'quirps',), 'classes': 'collapse'}),
            ('Images and Photos', {'fields': ('lead_image', 'lead_caption', 'sidebar_image', 'sidebar_caption', 'inline_image', 'inline_caption',), 'classes': 'collapse'}),
            ('Metadata: Relevant People, Places and Sources', {'fields': ('places', 'people', 'sources',), 'classes': 'collapse'}),
            ('Article Activity', {'fields': ('status', 'enable_comments',)}),
        )
        
        list_display    = ('headline', 'pub_date', 'author', 'status', 'enable_comments',)
        list_filter     = ['pub_date', 'author', 'status']
        search_fields   = ['headline', 'author', 'summary', 'tags']
        date_hierarchy  = 'pub_date'
