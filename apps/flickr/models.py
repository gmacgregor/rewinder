from django.conf import settings
from django.db import models
from tagging.fields import TagField
from django.dispatch import dispatcher
from django.db.models import signals
from threadedcomments.moderation import CommentModerator, moderator

from rewinder.lib.signals import create_tumblelog_item, kill_tumblelog_item
from rewinder.lib.models import BigIntegerField


FLICKR_LICENSES = (
    ('0', 'All Rights Reserved'),
    ('1', 'Attribution-NonCommercial-ShareAlike License'),
    ('2', 'Attribution-NonCommercial License'),
    ('3', 'Attribution-NonCommercial-NoDerivs License'),
    ('4', 'Attribution License'),
    ('5', 'Attribution-ShareAlike License'),
    ('6', 'Attribution-NoDerivs License'),
)

class MyPhotosManager(models.Manager):
    def get_query_set(self):
        qs = super(MyPhotosManager, self).get_query_set()
        return qs.filter(owner="sixminutes").order_by('-taken_date')

class Photo(models.Model):
    #flickr_id           = models.PositiveIntegerField()
    flickr_id           = BigIntegerField()
    owner               = models.CharField(max_length=50)
    owner_nsid          = models.CharField(max_length=50)
    title               = models.CharField(max_length=200)
    slug                = models.SlugField()
    #description         = models.CharField(max_length=250, blank=True)
    description         = models.TextField(blank=True)
    taken_date          = models.DateTimeField()
    photopage_url       = models.URLField()
    square_url          = models.URLField()
    small_url           = models.URLField()
    medium_url          = models.URLField()
    thumbnail_url       = models.URLField()
    tags                = TagField()
    enable_comments     = models.BooleanField(default=settings.COMMENTS_ENABLE)
    license             = models.CharField(max_length=50, choices=FLICKR_LICENSES)
    geo_latitude        = models.CharField(max_length=50, blank=True)
    geo_longitude       = models.CharField(max_length=50, blank=True)
    geo_accuracy        = models.CharField(max_length=50, blank=True)
    exif_make           = models.CharField(max_length=50, blank=True)
    exif_model          = models.CharField(max_length=50, blank=True)
    exif_orientation    = models.CharField(max_length=50, blank=True)
    exif_exposure       = models.CharField(max_length=50, blank=True)
    exif_software       = models.CharField(max_length=250, blank=True)
    exif_aperture       = models.CharField(max_length=50, blank=True)
    exif_iso            = models.CharField(max_length=50, blank=True)
    exif_metering_mode  = models.CharField(max_length=50, blank=True)
    exif_flash          = models.CharField(max_length=50, blank=True)
    exif_focal_length   = models.CharField(max_length=50, blank=True)
    exif_color_space    = models.CharField(max_length=50, blank=True)
    
    #managers
    objects             = models.Manager()
    sixminutes          = MyPhotosManager()
    
    def __unicode__(self):
        return u'%s' % self.title
    
    @models.permalink
    def get_absolute_url(self):
       return ('photo_detail', (), {
            'year': self.taken_date.year,
            'month': str(self.taken_date.month).zfill(2),
            'day': str(self.taken_date.day).zfill(2),
            'object_id': self.id,
        })
    
    def _next_previous_helper(self, direction):
            return getattr(self, 'get_%s_by_taken_date' % direction)(owner__exact='sixminutes')
    
    @property
    def get_next(self):
        return self._next_previous_helper('next')
    
    @property
    def get_previous(self):
        return self._next_previous_helper('previous')
    
    def save(self):
        """
        Assign photo.slug to a slugified version of the photo title.
        If the title is empty, slugify to "untitled-photo.id"
        
        If this photo doesn't belong to me, DO NOT save associated tags
        
        """
        if not self.id:
            from django.template.defaultfilters import slugify
            if not self.title:
                self.title = "Untitled"
                self.slug = "untitled-%s" % self.flickr_id
            else:
                self.slug = slugify(self.title)
            if self.owner != "sixminutes":
                self.tags = ''
        super(Photo, self).save()
    
    class Meta:
        ordering = ('-taken_date',)
        get_latest_by = 'taken_date'
    
    class Admin:
        list_display = ('taken_date', 'title', 'flickr_id', 'owner')
        search_fields = ['title', 'description']
        date_hierarchy = 'taken_date'


class FavoriteList(models.Model):
    owner = models.CharField(max_length=50)
    sync_date = models.DateTimeField()
    photos = models.ManyToManyField('Photo')
    
    def numPhotos(self):
        return len(self.photo_list.objects.all())
    
    def __unicode__(self):
        return u"%s's favorite photos" % self.owner
    
    class Admin:
        list_display = ('owner', 'sync_date', 'numPhotos')


class PhotoSet(models.Model):
    flickr_id           = models.CharField(max_length=50)
    owner               = models.CharField(max_length=50)
    title               = models.CharField(max_length=200)
    description         = models.CharField(max_length=250)
    photos              = models.ManyToManyField('Photo')
    
    def numPhotos(self):
        return len(self.photos.objects.all())
    
    def __unicode__(self):
        return u"%s photo set by %s" % (self.title, self.owner)
    
    class Admin:
        list_display = ('flickr_id', 'owner', 'title')

class PhotoModerator(CommentModerator):
    akismet = settings.COMMENTS_AKISMET
    auto_moderate_field = 'taken_date'
    moderate_after = settings.COMMENTS_MODERATE_AFTER
    email_notification = settings.COMMENTS_EMAIL
    enable_field = settings.COMMENTS_ENABLE_FIELD
moderator.register(Photo, PhotoModerator)
        
dispatcher.connect(create_tumblelog_item, sender=Photo, signal=signals.post_save)
dispatcher.connect(kill_tumblelog_item, sender=Photo, signal=signals.post_delete)