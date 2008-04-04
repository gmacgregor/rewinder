from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models


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

