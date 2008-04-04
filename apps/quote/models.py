from django.db import models
from rewinder.apps.quirp.models import Source, Person

class Quote(models.Model):
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField('Publication Date')
    author              = models.ForeignKey(Person, null=True, blank=True)
    source              = models.ForeignKey(Source)
    text                = models.TextField()
    
    def __unicode__(self):
        return u'%s' % self.text
    
    class Admin:
        pass
