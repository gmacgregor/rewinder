from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.db import connection

class TumblelogItemManager(models.Manager):
    
    def get_objects_for_year(self, year):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT t.pub_date, t.content_type, t.object_id, t.content_object
            FROM tumblelog_tumblelogitem t
            JOIN ON django_content_type d
            WHERE t.pub_date = 2007
            """)
    
class TumblelogItem(models.Model):
    '''
    Any TumblelogItem is assumed to contain a pub_date
    '''
    pub_date            = models.DateTimeField()
    content_type        = models.ForeignKey(ContentType)
    object_id           = models.PositiveIntegerField()
    content_object      = GenericForeignKey()
    
    def get_content_object(self):
        '''
        A method for retrieving a certain type of object
        '''
        try:
            return self.content_type.get_object_for_this_type(pk=self.object_id)
        except ObjectDoesNotExist:
            return None
    
    class Meta:
        ordering = ['-pub_date']
        unique_together = (('content_type', 'object_id'),)
    
    class Admin:
        date_hierarchy = 'pub_date'
        list_display = ('get_content_object', 'pub_date', 'content_type')
        list_filter = ('pub_date', 'content_type',)