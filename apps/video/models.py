from django.db import models
from django.conf import settings
from django.dispatch import dispatcher
from django.db.models import signals
from tagging.fields import TagField
from template_utils.markup import formatter
from comment_utils.moderation import CommentModerator, moderator

from rewinder.apps.geo.models import Place
from rewinder.apps.generic.models import Source, Person
from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.lib.signals import create_tumblelog_item, kill_tumblelog_item


class Video(models.Model):
    #publication details
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField(u'Publication Date', auto_now=True)
    original_date       = models.DateTimeField(blank=True, help_text=u'The original creation date of the video. Optional, but preferred.')
    title               = models.CharField(max_length=255, unique_for_date='pub_date')
    slug                = models.SlugField(max_length=255, prepopulate_from=('title',), help_text=u'Automatically built from video title.', unique=True)
    description         = models.TextField(blank=True, help_text=u'Use Markdown syntax for HTML formatting. Optional.')
    html_description    = models.TextField(blank=True, null=True)
    commentary          = models.TextField(blank=True, help_text=u'Your opinion/additional comments about the video.  Use Markdown syntax for HTML formatting. Optional.')
    html_commentary     = models.TextField(blank=True, null=True)
    tags                = TagField()
    enable_comments     = models.BooleanField(default=True)
    
    #meta
    video_id            = models.CharField(u'Video ID', max_length=100, blank=True, help_text=u"The 'id' of the video. For example: http://youtube.com/watch?v=NakX-vtxYhI the 'id' is 'NakX-vtxYhI'. If this is a youtube.com video then it can be determined for you. Optional.")
    running_time        = models.CharField(max_length=10, blank=True, help_text=u'Optional.')
    nsfw                = models.BooleanField(u'NSFW?', help_text=u'Is this video Not Suitable For Work?')
    source              = models.ForeignKey(Source, help_text=u'Youtube, CBC, CNN etc...')
    url                 = models.URLField(u'URL', help_text=u'For example: http://youtube.com/watch?v=rTZ6oDgUzkU', verify_exists=False)
    embed_code          = models.TextField(max_length=400, blank=True, help_text=u'Optional.')
    rating              = models.CharField(max_length=20, choices=settings.RATING_CHOICES, blank=True, help_text=u'Totally arbitray and completely optional.')
    
    #related items
    videos              = models.ManyToManyField('self', filter_interface=models.HORIZONTAL, null=True, blank=True, help_text=u'Optional.')
    people              = models.ManyToManyField(Person, filter_interface=models.HORIZONTAL, null=True, blank=True, help_text=u'Optional.')
    places              = models.ManyToManyField(Place, filter_interface=models.HORIZONTAL, null=True, blank=True, help_text=u'Optional.')
    
    #uploaded video
    path                = models.FileField(upload_to='video/%Y/%m/%d', blank=True)
    
    def __unicode__(self):
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('video_detail', (), {
            'year': self.pub_date.year,
            'month': str(self.pub_date.month).zfill(2),
            'day': str(self.pub_date.day).zfill(2),
            'slug': self.slug,
        })
    
    def youtube_small_image(self):
        if self.url.find('youtube') and self.video_id:
            return "http://i.ytimg.com/vi/%s/default.jpg" % self.video_id
        else:
            return None
    
    def youtube_small_image(self):
        if self.url.find('youtube') and self.video_id:
            return "http://i.ytimg.com/vi/%s/default.jpg" % self.video_id
        else:
            return None
    
    def related_videos(self):
        videos = Video.objects.all().filter(tags__icontains='%s') % self.tags
        return videos
    
    def save(self):
        if not self.id:
            if self.source.title.lower().count("youtube"):
                params = self.url.split("v=")[1]
                if params.find("&"):
                    self.video_id = params.split("&")[0]
                else:
                    self.video_id = params[0]
        if self.description:
                self.html_description = formatter(self.description)
        if self.commentary:
                self.html_commentary = formatter(self.commentary)
        super(Video, self).save()
    
    class Admin:
        date_hierarchy = 'pub_date'
        fields = (
            ('Upload your own', {'fields': ('path',), 'classes': 'collapse'}),
            ('Publication details', {'fields': ('pub_date', 'original_date', 'title', 'slug', 'description', 'commentary', 'tags', 'enable_comments',)}),
            ('Details', {'fields': ('url', 'video_id', 'source', 'embed_code', 'running_time', 'rating', 'nsfw',)}),
            ('Related Material', {'fields': ('videos', 'people', 'places',), 'classes': 'collapse'}),
        )
        
        list_display    = ('title', 'url', 'source', 'enable_comments', 'running_time',)
        search_fields   = ['title', 'description', 'source', 'people', 'url', 'tags']
        date_hierarchy  = 'created_on'


class VideoModerator(CommentModerator):
    akismet = settings.COMMENTS_AKISMET
    auto_close_field = 'pub_date'
    close_after = settings.COMMENTS_CLOSE_AFTER
    email_notification = settings.COMMENTS_EMAIL
    enable_field = settings.COMMENTS_ENABLE_FIELD
moderator.register(Video, VideoModerator)


dispatcher.connect(create_tumblelog_item, sender=Video, signal=signals.post_save)
dispatcher.connect(kill_tumblelog_item, sender=Video, signal=signals.post_delete)
