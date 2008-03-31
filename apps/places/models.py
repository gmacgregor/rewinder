from django.db import models
from django.db.models import permalink
from django.core import validators
from tagging.fields import TagField

PROVINCE_CHOICES = (
	('ab', 'Alberta'),
	('bc', 'British Columbia'),
	('man', 'Manitoba'),
	('nb', 'New Brunswick'),
	('nfld', 'Newfoundland and Labrador'),
	('nwt', 'Northwest Territories'),
	('ns', 'Nova Scotia'),
	('nun', 'Nunavut'),
	('on', 'Ontario'),
	('pei', 'Prince Edward Island'),
	('que', 'Quebec'),
	('sask', 'Saskatchewan'),
	('yuk', 'Yukon'),	 
)

class PlaceType(models.Model):
	"""P
	A generic 'kind' of place. Something like 'bar', 'restaurant', 'stadium'
	"""
	created_on			= models.DateTimeField(auto_now_add=True)
	last_modified		= models.DateTimeField(auto_now=True)
	name				= models.CharField(max_length=100)
	slug				= models.SlugField(prepopulate_from=('name',))
	
	def __unicode__(self):
		return '%s' % self.name
	
	@permalink
	def get_absolute_url(self):
		return ('place_type_detail', None, {'slug': self.slug})
	
	class Meta:
		verbose_name_plural	= 'place types'
		db_table		= 'place_types'
	
	class Admin:
		pass

class Region(models.Model):
	"""
	ie. Eastern Seaboard, Suffolk County
	"""
	created_on			= models.DateTimeField(auto_now_add=True)
	last_modified		= models.DateTimeField(auto_now=True)
	name				= models.CharField(max_length=100)
	slug				= models.SlugField(prepopulate_from=('name',))
	image 				= models.ImageField(upload_to='/img/places/regions/', blank=True, help_text='Optional.')	
	
	def __unicode__(self):
		return '%s' % self.name
	
	@permalink
	def get_absolute_url(self):
		return ('place_region_detail', None, {'slug': self.slug})
	
	class Meta:
		verbose_name_plural	= 'regions'
		db_table			= 'place_regions'
	
	class Admin:
		pass


class Country(models.Model):
	name				= models.CharField(max_length=100, unique=True)
	slug				= models.SlugField(prepopulate_from=('name',))
	image 				= models.ImageField(upload_to='/img/places/regions/', blank=True, help_text='Optional.')
	
	def __unicode__(self):
		return '%s' % self.name
	
	@permalink
	def get_absolute_url(self):
		return ('place_country_detail', None, {'slug': self.slug})
	
	class Meta:
		verbose_name_plural = 'countries'
		db_table 			= 'place_countries'
	
	class Admin:
		pass


class City(models.Model):
	name				= models.CharField(max_length=100)
	province			= models.CharField(max_length=4, choices=PROVINCE_CHOICES, default='on', blank=True, help_text='Optional, but preferred.')
	country				= models.ForeignKey(Country)
	region				= models.ForeignKey(Region, blank=True, help_text=u'ie. Southwestern Ontario, GTA, Praries, Canadian Shield. Optional.')
	postal_code			= models.CharField(max_length=10, blank=True, help_text=u'The postal/zip code of the downtown core. Optional.')
	slug				= models.SlugField(prepopulate_from=('name', 'province',))
	image 				= models.ImageField(upload_to='/img/places/cities/', blank=True, help_text='Optional.')
	
	def __unicode__(self):
		return '%s' % self.name
	
	@permalink
	def get_absolute_url(self):
		return ('place_city_detail', None, {'slug': self.slug})
	
	class Admin:
		pass
	
	class Meta:
		verbose_name_plural	= 'cities'
		db_table		= 'place_cities'
		unique_together	= (('name', 'province',),)
		ordering		= ('province', 'name',)

class Point(models.Model):
	latitude			= models.FloatField()
	longitude			= models.FloatField()
	address				= models.CharField(max_length=200, blank=True)
	city				= models.ForeignKey(City, blank=True, null=True)
	country				= models.ForeignKey(Country, blank=True, null=True)
	postal_code			= models.CharField(max_length=10, blank=True)
	description			= models.TextField(blank=True)
			
	class Meta:
		db_table = 'place_points'
		ordering = ('address',)
	
	class Admin:
		pass

	def __unicode__(self):
		return '%s' % self.address

class Place(models.Model):
	STATUS_CHOICES = (
		(0, 'Off'),
		(1, 'On'),
	)
	created				= models.DateTimeField(auto_now_add=True)
	modified			= models.DateTimeField(auto_now=True)
	point				= models.ForeignKey(Point)
	city				= models.ForeignKey(City, help_text=u'The nearest city, town.')
	prefix				= models.CharField('Pre-name', blank=True, max_length=20, help_text=u'ie. possibly ont for Ontario. Optional.')
	name				= models.CharField(max_length=255)
	slug				= models.SlugField(prepopulate_from=('name',))
	nickname			= models.CharField(blank=True, max_length=100, help_text=u'Optional.')
	unit				= models.CharField(blank=True, max_length=100, help_text=u'Suite or Apartment #. Optional')
	phone				= models.CharField(blank=True, max_length=20, help_text='Optional.')
	url					= models.URLField(blank=True, verify_exists=False, help_text='Optional.')
	email				= models.EmailField(blank=True, help_text='Optional.')
	description			= models.TextField(blank=True, help_text='Optional.')
	status				= models.IntegerField(choices=STATUS_CHOICES, radio_admin=True, default=1)
	place_types			= models.ManyToManyField(PlaceType, blank=True, help_text='Optional.')
	tags				= TagField()
	
	class Meta:
		db_table = 'places'
		ordering = ('name',)
	
	class Admin:
		search_fields = ('name',)
	
	def __unicode__(self):
		return '%s' % self.name
	
	@permalink
	def get_absolute_url(self):
		return ('place_detail', None, {'slug':self.slug})
	
	@property
	def address(self):
		return '%s, %s %s' % (self.point.address, self.point.city, self.point.postal_code)