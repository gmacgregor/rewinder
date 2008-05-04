from django.conf import settings
from django.db import models
from django.dispatch import dispatcher
from django.db.models import signals
#from comment_utils.moderation import CommentModerator, moderator
from threadedcomments.moderation import CommentModerator, moderator
from tagging.fields import TagField
from rewinder.util.timeconverter import time_to_settings
from rewinder.lib.signals import create_tumblelog_item, kill_tumblelog_item

import datetime

class Bookmark(models.Model):
    saved_date              = models.DateTimeField(default=datetime.datetime.today)
    description             = models.CharField(max_length=255, blank=True)
    slug                    = models.SlugField(max_length=255, prepopulate_from=('description',), help_text='Automatically built from description.', unique_for_date='saved_date') 
    url                     = models.URLField()
    tags                    = TagField()
    extended_info           = models.CharField(max_length=255, blank=True)
    post_hash               = models.CharField(max_length=100, null=True, blank=True)
    via_url                 = models.URLField(u'Via URL', verify_exists=False, blank=True, null=True, help_text=u'The URL of the site where you spotted the link. Optional.')
    enable_comments         = models.BooleanField(default=True)
    post_elsewhere          = models.BooleanField(u'Post to del.icio.us', default=False, help_text=u'If checked, this link will be posted both to your weblog and to your del.icio.us account.')
    
    def __unicode__(self):
        return u'%s' % self.description
    
    @models.permalink
    def get_absolute_url(self):
        return ('bookmark_detail', (), {
            'year': self.saved_date.year,
            'month': str(self.saved_date.month).zfill(2),
            'day': str(self.saved_date.day).zfill(2),
            'slug': self.slug,
        })
    
    def _next_previous_helper(self, direction):
        return getattr(self, 'get_%s_by_saved_date' % direction)
    
    @property
    def get_next(self):
        return self._next_previous_helper('next')
    
    @property
    def get_previous(self):
        return self._next_previous_helper('previous')
    
    def save(self):
        """
        If this link is being saved for the first time (ie. imported from del.icou.us):
            1. create self.slug based on self.description
            2. remove any tags that contain the characters: :+./&#
            3. check if post_elsewhere is true, and if so, attempt to post to del.icio.us
        """
        if not self.id:
            import re
            from django.template.defaultfilters import slugify
            self.slug = slugify(self.description)
            self.saved_date = time_to_settings(self.saved_date)
            tags_re = re.compile('[\:|\+|\&|\/|\#|\.]+')
            tags = self.tags.split()
            new_tags = []
            for tag in tags:
                if not tags_re.search(tag):
                    new_tags.append(tag)
            self.tags = ' '.join(new_tags)
            if self.post_elsewhere:
                import pydelicious
                try:
                    pydelicious.add(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD, self.url, self.description, self.tags, self.extended_info)
                except:
                    pass
        super(Bookmark, self).save()
    
    class Meta:
        ordering = ('-saved_date',)
        get_latest_by = 'saved_date'
        
    class Admin:
        list_display = ('description', 'saved_date', 'extended_info')
        search_fields = ['description', 'extended_info']
        date_hierarchy = 'saved_date'

class BookmarkModerator(CommentModerator):
    akismet = settings.COMMENTS_AKISMET
    auto_close_field = 'saved_date'
    close_after = settings.COMMENTS_CLOSE_AFTER
    email_notification = settings.COMMENTS_EMAIL
    enable_field = settings.COMMENTS_ENABLE_FIELD
moderator.register(Bookmark, BookmarkModerator)


dispatcher.connect(create_tumblelog_item, sender=Bookmark, signal=signals.post_save)
dispatcher.connect(kill_tumblelog_item, sender=Bookmark, signal=signals.post_delete)
