"""
START DJANGO PHOTO MODEL
Requires django-tagging (http://code.google.com/p/django-tagging/)
"""
from django.db import models
from tagging.fields import TagField

FLICKR_LICENSES = (
    ('0', 'All Rights Reserved'),
    ('1', 'Attribution-NonCommercial-ShareAlike License'),
    ('2', 'Attribution-NonCommercial License'),
    ('3', 'Attribution-NonCommercial-NoDerivs License'),
    ('4', 'Attribution License'),
    ('5', 'Attribution-ShareAlike License'),
    ('6', 'Attribution-NoDerivs License'),
)

class Set(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    set_id = models.IntegerField()
    primary = models.CharField(max_length=512)
    secret = models.CharField(max_length=512)
    server = models.IntegerField()
    farm = models.IntegerField()
    photos = models.IntegerField()
    
    class Admin:
        list_display = ('title', 'description', 'set_id')
        search_fields = ['title', 'description']
        
    def __unicode__(self):
        return '%s' % self.title
        
class Pool(models.Model):
    title = models.CharField(max_length=512)
    pool_id = models.CharField(max_length=100)
    
    class Admin:
        list_display = ('title', 'pool_id')
        search_fields = ['title', 'description']
        
    def __str__(self):
        return '%s' % (self.title)

class Photo(models.Model):
    photo_id = models.IntegerField()
    secret = models.CharField(max_length=512)
    server = models.IntegerField()
    is_favorite = models.BooleanField()
    farm = models.IntegerField()
    original_secret = models.CharField(max_length=512)
    views = models.IntegerField()
    original_format = models.CharField(max_length=512)
    license = models.CharField(max_length=10, choices=FLICKR_LICENSES)
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    is_public = models.BooleanField()
    is_friend = models.BooleanField()
    is_family = models.BooleanField()
    date_taken = models.DateTimeField()
    date_uploaded = models.DateTimeField()
    last_updated = models.DateTimeField()
    comments = models.IntegerField()
    photo_page = models.URLField()
    tags = TagField(blank=True)
    sets = models.ManyToManyField(Set, blank=True)
    pools = models.ManyToManyField(Pool, blank=True)
    latitude = models.CharField(max_length=512, blank=True)
    longitude = models.CharField(max_length=512, blank=True)
    accuracy = models.IntegerField(blank=True, null=True)
    locality = models.CharField(max_length=512, blank=True)
    county = models.CharField(max_length=512, blank=True)
    region = models.CharField(max_length=512, blank=True)
    country = models.CharField(max_length=512, blank=True)
    geo_is_public = models.BooleanField()
    geo_is_contact = models.BooleanField()
    geo_is_friend = models.BooleanField()
    geo_is_family = models.BooleanField()
    exif_make = models.CharField(max_length=512, blank=True)
    exif_model = models.CharField(max_length=512, blank=True)
    exif_orientation = models.CharField(max_length=512, blank=True)
    exif_exposure = models.CharField(max_length=512, blank=True)
    exif_software = models.CharField(max_length=512, blank=True)
    exif_aperture = models.CharField(max_length=512, blank=True)
    exif_exposure_program = models.CharField(max_length=512, blank=True)
    exif_iso = models.CharField(max_length=512, blank=True)
    exif_metering_mode = models.CharField(max_length=512, blank=True)
    exif_flash = models.CharField(max_length=512, blank=True)
    exif_focal_length = models.CharField(max_length=512, blank=True)
    exif_color_space = models.CharField(max_length=512, blank=True)
    
    class Admin:
        list_display = ('title', 'is_public', 'is_family', 'is_friend', 'date_taken', 'last_updated')
        list_filter = ('date_taken', 'last_updated', 'is_public', 'is_family', 'is_friend')
        search_fields = ['title', 'description']
    
    def __unicode__(self):
        return '%s' % (self.title)

