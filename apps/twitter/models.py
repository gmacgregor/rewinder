from django.conf import settings
from django.db import models
from django.dispatch import dispatcher
from django.db.models import signals
from rewinder.util.timeconverter import time_to_settings
from threadedcomments.moderation import CommentModerator, moderator
from rewinder.lib.signals import create_tumblelog_item, kill_tumblelog_item

from rewinder.util.timeconverter import time_to_settings

class Tweet(models.Model):
    pub_time            = models.DateTimeField()
    twitter_id          = models.PositiveIntegerField()
    text                = models.TextField()
    user                = models.ForeignKey('TwitterUser')
    enable_comments     = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s' % (self.text)
    
    @models.permalink
    def get_absolute_url(self):
        return ('tweet_detail', (), {
            'year': self.pub_time.year,
            'month': str(self.pub_time.month).zfill(2),
            'day': str(self.pub_time.day).zfill(2),
            'object_id': self.id,
            })
    
    def url(self):
        return u'http://twitter.com/%s/statuses/%s' % (self.user.screen_name, self.twitter_id)
    
    def save(self):
        if not self.id:
            self.pub_time = time_to_settings(self.pub_time)
        super(Tweet, self).save()
    
    def _next_previous_helper(self, direction):
        return getattr(self, 'get_%s_by_pub_time' % direction)
    
    @property
    def get_next(self):
        return self._next_previous_helper('next')
    
    @property
    def get_previous(self):
        return self._next_previous_helper('previous')
    
    class Meta:
        ordering = ('-pub_time',)
        get_latest_by = 'pub_time'
    
    class Admin:
        date_hierarchy = 'pub_time'
        list_display = ('user', 'pub_time', 'text', 'enable_comments')

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


class TweetModerator(CommentModerator):
    akismet = settings.COMMENTS_AKISMET
    auto_moderate_field = 'pub_time'
    moderate_after = settings.COMMENTS_MODERATE_AFTER
    email_notification = settings.COMMENTS_EMAIL
    enable_field = settings.COMMENTS_ENABLE_FIELD
moderator.register(Tweet, TweetModerator)

dispatcher.connect(create_tumblelog_item, sender=Tweet, signal=signals.post_save)
dispatcher.connect(kill_tumblelog_item, sender=Tweet, signal=signals.post_delete)
