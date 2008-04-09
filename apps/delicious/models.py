from django.conf import settings
from django.db import models
from tagging.fields import TagField
from django.dispatch import dispatcher
from django.db.models import signals
from rewinder.lib.signals import create_tumblelog_item, kill_tumblelog_item
import datetime
import pydelicious


class Bookmark(models.Model):
    saved_date              = models.DateTimeField(default=datetime.datetime.today)
    description             = models.CharField(max_length=250, blank=True)
    url                     = models.URLField()
    tags                    = TagField()
    extended_info           = models.CharField(max_length=250, blank=True)
    post_hash               = models.CharField(max_length=100, null=True, blank=True)
    via_url                 = models.URLField(u'Via URL', verify_exists=False, blank=True, null=True, help_text=u'The URL of the site where you spotted the link. Optional.')
    enable_comments         = models.BooleanField(default=True)
    post_elsewhere          = models.BooleanField(u'Post to del.icio.us', default=False, help_text=u'If checked, this link will be posted both to your weblog and to your del.icio.us account.')
    
    def __unicode__(self):
        return u'%s' % self.description
    
    @models.permalink
    def get_absolute_url(self):
        return ('link_detail', (), {'object_id': self.id})
    
    def save(self):
        if self.post_elsewhere:
            try:
                pydelicious.add(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD, self.url, self.description, self.tags, self.extended_info)
            except:
                raise
        super(Bookmark, self).save()
    
    #def delete(self):
    #   """
    #   Always try to delete from del.icio.us first
    #   """
    #   try:
    #       pydelicious.delete(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD, self.url)
    #   except:
    #       pass
    #   super(Link, self).delete()
    
    class Meta:
        ordering = ('-saved_date',)
        get_latest_by = 'saved_date'
        
    class Admin:
        list_display = ('description', 'saved_date', 'extended_info')
        search_fields = ['description', 'extended_info']
        date_hierarchy = 'saved_date'

dispatcher.connect(create_tumblelog_item, sender=Bookmark, signal=signals.post_save)
dispatcher.connect(kill_tumblelog_item, sender=Bookmark, signal=signals.post_delete)