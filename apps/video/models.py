from django.db import models
from tagging.fields import TagField
from rewinder.apps.places.models import Place
from rewinder.apps.quirp.models import Source, Person
from rewinder.apps.links.models import Link

RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'), 
)

class Video(models.Model):
    created_on          = models.DateTimeField(u'Creation Date', auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)   
    pub_date            = models.DateTimeField(u'Publication Date', auto_now=True)
    title               = models.CharField(max_length=255, unique_for_date='pub_date')                                    
    slug                = models.SlugField(max_length=255, prepopulate_from=('title',), help_text=u'Automatically built from video title.', unique=True)
    description         = models.TextField(blank=True, help_text=u'Optional.')
    running_time        = models.CharField(max_length=10, blank=True, help_text=u'Optional.')
    nsfw                = models.BooleanField(u'NSFW?', help_text=u'Is this video Not Suitable For Work?')
    source              = models.ForeignKey(Source, help_text=u'Youtube, CBC, CNN etc...')
    people              = models.ManyToManyField(Person, filter_interface=models.HORIZONTAL, null=True, blank=True, help_text=u'Optional.')
    places              = models.ManyToManyField(Place, filter_interface=models.HORIZONTAL, null=True, blank=True, help_text=u'Optional.')
    url                 = models.URLField(u'URL', blank=True, help_text=u'For example: http://youtube.com/watch?v=rTZ6oDgUzkU. Optional.', verify_exists=False)
    embed_code          = models.TextField(max_length=400, blank=True, help_text=u"Paste video embed code in here if you're grabbing it from Youtube or something. Optional.")
    path                = models.FileField(upload_to='video/%Y/%m/%d', blank=True)
    rating              = models.CharField(max_length=20, choices=RATING_CHOICES, blank=True, help_text=u'Totally arbitray and completely optional.')
    tags                = TagField()
    enable_comments     = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('video_detail', (), {
            'year': self.pub_date.year,
            'month': str(self.pub_date.month).zfill(2),
            'day': str(self.pub_date.day).zfill(2),
            'slug': self.slug,
        })
    
    class Admin:
        list_display    = ('title', 'url', 'source', 'enable_comments', 'running_time',)
        search_fields   = ['title', 'description', 'source', 'people', 'url', 'tags']
        date_hierarchy  = 'created_on'
