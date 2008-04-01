from django.db import models
from tagging.fields import TagField
from django.conf import settings
import pydelicious
import datetime

# Create your models here.
class Link(models.Model):
    pub_date            = models.DateTimeField(default=datetime.datetime.today)
    url                 = models.URLField(u'URL', max_length=250, unique=True, verify_exists=False)
    title               = models.CharField(max_length=250)
    slug                = models.SlugField(prepopulate_from=('title',), unique_for_date='pub_date', help_text=u'Must be unique for the publication date.')  
    description         = models.CharField(max_length=250, blank=True)
    tags                = TagField()
    via_name            = models.CharField(u'Via', max_length=250, blank=True, null=True, help_text=u'The name of the person whose site you spotted the link on. Optional.')
    via_url             = models.URLField(u'Via URL', verify_exists=False, blank=True, null=True, help_text=u'The URL of the site where you spotted the link. Optional.')   
    enable_comments     = models.BooleanField(default=True)
    post_elsewhere      = models.BooleanField(u'Post to del.icio.us', default=True, help_text=u'If checked, this link will be posted both to your weblog and to your del.icio.us account.')
    update_elsewhere    = models.BooleanField(u'Update on del.icio.us?', default=False, help_text=u'Check to update a link already posted to your del.icio.us account.')
    #delete_elsewhere   = models.BooleanField(u'Delete on del.icio.us?', help_text=u'Check to delete a link already posted to your del.icio.us account.', default=False)
    
    def __unicode__(self):
        return self.title
    
    #def save(self):
    #   """
    #   New links are posted to del.ici.ous if post elswhere is checked (default True)
    #   """
    #   if not self.id and self.post_elsewhere:
    #       try:
    #           pydelicious.add(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD, self.url, self.title, self.tags, self.description)
    #       except:
    #           pass
    #   if self.id and self.update_elsewhere:
    #       try:
    #           pydelicious.delete(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD, self.url)
    #           pydelicious.add(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD, self.url, self.title, self.tags, self.description)
    #       except:
    #           pass
    #   self.update_elsewhere, self.delete_elsewhere = False
    #   super(Link, self).save()
    
    #def delete(self):
    #   """
    #   Always try to delete from del.icio.us first
    #   """
    #   try:
    #       pydelicious.delete(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD, self.url)
    #   except:
    #       pass
    #   super(Link, self).delete()
    
    class Admin:
        pass