from django.db import models
from django.dispatch import dispatcher
from django.db.models import signals
from rewinder.util.timeconverter import time_to_settings
from rewinder.lib.signals import create_tumblelog_item, kill_tumblelog_item


class Tweet(models.Model):
    pub_time            = models.DateTimeField()
    twitter_id          = models.PositiveIntegerField()
    text                = models.TextField()
    user                = models.ForeignKey('TwitterUser')
    
    def __unicode__(self):
        return u'%s' % (self.text)
    
    def url(self):
        return u'http://twitter.com/%s/statuses/%s' % (self.user.screen_name, self.twitter_id)
    
    def save(self):
        if not self.id:
            self.pub_time = time_to_settings(self.pub_time)
        super(Tweet, self).save()
    
    class Meta:
        ordering = ('-pub_time',)
        get_latest_by = 'pub_time'
    
    class Admin:
        date_hierarchy = 'pub_time'
        list_display = ('user', 'pub_time', 'text')

class TwitterUser(models.Model):
    screen_name         = models.CharField(max_length=50)
    description         = models.CharField(max_length=250, blank=True, null=True)
    location            = models.CharField(max_length=50, blank=True, null=True)
    name                = models.CharField(max_length=50, blank=True, null=True)
    thumbnail_url       = models.URLField()
    url                 = models.URLField(blank=True, null=True)
    friends             = models.ManyToManyField('TwitterUser', related_name='friends_user_set', blank=True, null=True)
    followers           = models.ManyToManyField('TwitterUser', related_name='followers_user_set', blank=True, null=True)
    
    def numFriends(self):
        return self.friends.count()
    
    def numFollowers(self):
        return self.followers.count()
    
    def __unicode__(self):
        return self.screen_name
    
    class Admin:
        list_display = ('screen_name', 'name', 'location', 'numFriends', 'numFollowers')


dispatcher.connect(create_tumblelog_item, sender=Tweet, signal=signals.post_save)
dispatcher.connect(kill_tumblelog_item, sender=Tweet, signal=signals.post_delete)
