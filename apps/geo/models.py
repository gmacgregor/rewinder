from django.db import models
from django.db.models import permalink
from django.core import validators
from tagging.fields import TagField

PROVINCE_CHOICES = (
    ('AB', 'Alberta'),
    ('BC', 'British Columbia'),
    ('MAN', 'Manitoba'),
    ('NB', 'New Brunswick'),
    ('NFLD', 'Newfoundland and Labrador'),
    ('NWT', 'Northwest Territories'),
    ('NS', 'Nova Scotia'),
    ('NUN', 'Nunavut'),
    ('ON', 'Ontario'),
    ('PEI', 'Prince Edward Island'),
    ('QUE', 'Quebec'),
    ('SASK', 'Saskatchewan'),
    ('YUK', 'Yukon'),    
)


class PlaceType(models.Model):
    """
    A generic 'kind' of place. Something like 'bar', 'restaurant', 'stadium'
    """
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    name                = models.CharField(max_length=100)
    slug                = models.SlugField(prepopulate_from=('name',))
    image               = models.ImageField(upload_to='/img/places/placetype/', blank=True, help_text=u'Optional.')
    
    def __unicode__(self):
        return u'%s' % self.name
    
    @permalink
    def get_absolute_url(self):
        return ('place_type_detail', None, {'slug': self.slug})
    
    class Meta:
        verbose_name_plural = 'place types'
        db_table            = 'place_types'
    
    class Admin:
        pass


class Region(models.Model):
    """
    ie. Eastern Seaboard, Suffolk County
    """
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    name                = models.CharField(max_length=100)
    slug                = models.SlugField(prepopulate_from=('name',))
    image               = models.ImageField(upload_to='/img/places/region/', blank=True, help_text=u'Optional.')
    
    def __unicode__(self):
        return u'%s' % self.name
    
    @permalink
    def get_absolute_url(self):
        return ('place_region_detail', None, {'slug': self.slug})
    
    class Meta:
        verbose_name_plural = 'regions'
        db_table            = 'place_regions'
    
    class Admin:
        pass


class Country(models.Model):
    name                = models.CharField(max_length=100, unique=True)
    slug                = models.SlugField(prepopulate_from=('name',))
    image               = models.ImageField(upload_to='/img/places/country/', blank=True, help_text=u'Optional.')
    
    def __unicode__(self):
        return u'%s' % self.name
    
    @permalink
    def get_absolute_url(self):
        return ('place_country_detail', None, {'slug': self.slug})
    
    class Meta:
        verbose_name_plural = 'countries'
        db_table            = 'place_countries'
    
    class Admin:
        pass


class City(models.Model):
    name                = models.CharField(max_length=100)
    province            = models.CharField(max_length=4, choices=PROVINCE_CHOICES, default='on')
    slug                = models.SlugField(prepopulate_from=('province', 'name'))
    region              = models.ForeignKey(Region, null=True, blank=True, help_text=u'ie. Southwestern Ontario, GTA, Praries, Canadian Shield. Optional.')
    country             = models.ForeignKey(Country)
    image               = models.ImageField(upload_to='/img/places/city/', blank=True, help_text='Optional.')
    
    def __unicode__(self):
        return u'%s, %s' % (self.name, self.province)
    
    @permalink
    def get_absolute_url(self):
        return ('place_city_detail', None, {'slug': self.slug})
    
    class Admin:
        pass
    
    class Meta:
        verbose_name_plural = 'cities'
        db_table        = 'place_cities'
        unique_together = (('name', 'province',),)
        ordering        = ('province', 'name',)


class Point(models.Model):
    latitude            = models.FloatField(null=True, blank=True)
    longitude           = models.FloatField(null=True, blank=True)
    address             = models.CharField(max_length=200, blank=True, help_text=u'Optional.')
    city                = models.ForeignKey(City)
    #country             = models.ForeignKey(Country)
    postal_code         = models.CharField(max_length=10, blank=True, help_text=u'Optional.')
    
    def __unicode__(self):
      return u'%s - %s' % (self.city, self.address)
    
    class Meta:
        verbose_name = ('point')
        verbose_name_plural = ('points')
        db_table = 'place_points'
        ordering = ('address',)
    
    class Admin:
        list_display  = ('address', 'city', 'postal_code', 'latitude', 'longitude')
        list_filter   = ('city',)
        search_fields = ('address',)


class Place(models.Model):
    STATUS_CHOICES = (
        (0, 'Off'),
        (1, 'On'),
    )
    created             = models.DateTimeField(auto_now_add=True)
    modified            = models.DateTimeField(auto_now=True)
    point               = models.ForeignKey(Point)
    prefix              = models.CharField('Pre-name', blank=True, max_length=20, help_text=u'ie. possibly ont for Ontario. Optional.')
    name                = models.CharField(max_length=255)
    slug                = models.SlugField(prepopulate_from=('name',))
    nickname            = models.CharField(blank=True, max_length=100, help_text=u'Optional.')
    unit                = models.CharField(blank=True, max_length=100, help_text=u'Suite or Apartment #. Optional.')
    phone               = models.CharField(blank=True, max_length=20, help_text=u'Optional.')
    url                 = models.URLField(blank=True, verify_exists=False, help_text=u'Optional.')
    email               = models.EmailField(blank=True, help_text=u'Optional.')
    description         = models.TextField(blank=True, help_text=u'Optional.')
    status              = models.IntegerField(choices=STATUS_CHOICES, radio_admin=True, default=1)
    place_types         = models.ManyToManyField(PlaceType, blank=True, help_text=u'Optional.')
    tags                = TagField()
    
    def __unicode__(self):
        return '%s' % self.name
    
    @permalink
    def get_absolute_url(self):
        return ('place_detail', None, {'slug':self.slug})
    
    @property
    def city(self):
        return u'%s' % self.point.city
    
    @property
    def full_title(self):
        return u'%s %s' % (self.prefix, self.title)
    
    @property
    def longitude(self):
        return self.point.longitude
    
    @property
    def latitude(self):
        return self.point.latitude
    
    @property
    def address(self):
        return u'%s, %s %s' % (self.point.address, self.point.city, self.point.postal_code)
    
    class Meta:
        verbose_name = ('place')
        verbose_name_plural = ('places')
        db_table = 'places'
        ordering = ('name',)
    
    class Admin:
        list_display  = ('name', 'point', 'city', 'status')
        list_filter   = ('status', 'place_types')
        search_fields = ('name',)
