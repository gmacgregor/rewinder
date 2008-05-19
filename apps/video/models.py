from django.db import models
from django.conf import settings
from django.dispatch import dispatcher
from django.db.models import signals
from tagging.fields import TagField
from template_utils.markup import formatter
from typogrify.templatetags.typogrify import typogrify
from comment_utils.moderation import CommentModerator, moderator

from rewinder.apps.geo.models import Place
from rewinder.apps.generic.models import Source, Person
from rewinder.apps.tumblelog.models import TumblelogItem
from rewinder.lib.signals import create_tumblelog_item, kill_tumblelog_item
#from rewinder.util.timeconverter import time_to_utc

EXTERNAL_VIDEO_WIDTH = 499
EXTERNAL_VIDEO_HEIGHT = 300

class Video(models.Model):
    #publication details
    created_on          = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)
    pub_date            = models.DateTimeField(u'Publication Date')
    title               = models.CharField(max_length=255, unique_for_date='pub_date')
    slug                = models.SlugField(max_length=255, prepopulate_from=('title',), help_text=u'Automatically built from video title.', unique=True)
    description         = models.TextField(blank=True, help_text=u'Use Markdown syntax for HTML formatting. Optional.')
    html_description    = models.TextField(blank=True, null=True)
    commentary          = models.TextField(blank=True, help_text=u'Your opinion/additional comments about the video.  Use Markdown syntax for HTML formatting. Optional.')
    html_commentary     = models.TextField(blank=True, null=True)
    tags                = TagField()
    enable_comments     = models.BooleanField(default=True)
    
    #meta
    video_id            = models.CharField(u'Video ID', max_length=100, null=True, blank=True, help_text=u"The 'id' of the video. For example: http://youtube.com/watch?v=NakX-vtxYhI the 'id' is 'NakX-vtxYhI'. The system will make an attempt to determine this if not supplied.")
    running_time        = models.CharField(max_length=10, blank=True, help_text=u'Optional.')
    nsfw                = models.BooleanField(u'NSFW?', help_text=u'Is this video Not Suitable For Work?')
    source              = models.ForeignKey(Source, help_text=u'Youtube, CBC, CNN etc...')
    url                 = models.URLField(u'URL', help_text=u'For example: http://youtube.com/watch?v=rTZ6oDgUzkU', verify_exists=False)
    embed_code          = models.TextField(max_length=700, blank=True, help_text=u'The system will make an attempt to determine this if not supplied.')
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
    
    def _next_previous_helper(self, direction):
        return getattr(self, 'get_%s_by_pub_date' % direction)
    
    @property
    def get_next(self):
        return self._next_previous_helper('next')
    
    @property
    def get_previous(self):
        return self._next_previous_helper('previous')
    
    def youtube_small_image(self):
        if self.is_type('youtube.com') and self.video_id:
            return "http://i.ytimg.com/vi/%s/default.jpg" % self.video_id
        else:
            return None
    
    def youtube_small_image(self):
        if self.is_type('youtube.com') and self.video_id:
            return "http://i.ytimg.com/vi/%s/default.jpg" % self.video_id
        else:
            return None
    
    def related_videos(self):
        videos = Video.objects.all().filter(tags__icontains='%s') % self.tags
        return videos
    
    def is_type(self, type):
        if self.url.find(type) != -1:
            return True
        else:
            return False
    
    def get_video_id(self):
        if self.is_type('youtube.com'):
            params = self.url.split("v=")[1]
            if params.find("&") != -1:
                return params.split("&")[0]
            else:
                return params
        elif self.is_type('vimeo.com'):
            return self.url.split("/")[3]
        elif self.is_type('collegehumor.com'):
            return self.url.split(":")[2]
        else:
            return None
    
    def get_embed_code(self):
        if self.is_type('youtube.com'):
            embed = """
            <object width="%s" height="%s"><param name="movie" value="http://www.youtube.com/v/%s&hl=en">
            </param><param name="wmode" value="transparent"></param>
            <embed src="http://www.youtube.com/v/%s&amp;hl=en" type="application/x-shockwave-flash" 
            wmode="transparent" width="%s" height="%s">
            </embed></object>""" % (EXTERNAL_VIDEO_WIDTH, EXTERNAL_VIDEO_HEIGHT, self.video_id, 
            self.video_id, EXTERNAL_VIDEO_WIDTH, EXTERNAL_VIDEO_HEIGHT)
        elif self.is_type('vimeo.com'):
            embed = """<object type="application/x-shockwave-flash" width="%s" height="%s" 
            data="http://www.vimeo.com/moogaloop.swf?clip_id=%s&amp;server=www.vimeo.com&amp;fullscreen=1&amp;show_title=0&amp;
            show_byline=0&amp;show_portrait=0&amp;color=1a1819">
            <param name="quality" value="best" /><param name="allowfullscreen" value="true" />
            <param name="scale" value="showAll" /><param name="movie" value="http://www.vimeo.com/moogaloop.swf?clip_id=%s&amp;
            server=www.vimeo.com&amp;fullscreen=1&amp;show_title=0&amp;show_byline=0&amp;show_portrait=0&amp;
            color=1a1819" /></object>""" % (EXTERNAL_VIDEO_WIDTH, EXTERNAL_VIDEO_HEIGHT, self.video_id, self.video_id)
        elif self.is_type('collegehumor.com'):
            embed = """<object type="application/x-shockwave-flash" 
            data="http://www.collegehumor.com/moogaloop/moogaloop.swf?clip_id=%s&amp;fullscreen=1" 
            width="%s" height="%s" ><param name="allowfullscreen" value="true" />
            <param name="movie" quality="best" value="http://www.collegehumor.com/moogaloop/moogaloop.swf?clip_id=%s
            &amp;fullscreen=1" /></object>""" % (self.video_id, EXTERNAL_VIDEO_WIDTH, EXTERNAL_VIDEO_HEIGHT, self.video_id)
        else:
            embed = None
        return embed
    
    def _process_markup(self):
        self.html_description = typogrify(formatter(self.description))
        self.html_commentary = typogrify(formatter(self.commentary))
        return self
    
    def save(self):
        if not self.id:
            self.video_id = self.get_video_id()
        if not self.embed_code:
            self.embed_code = self.get_embed_code()
        #self.pub_date = time_to_utc(self.pub_date)
        self._process_markup()
        super(Video, self).save()
    
    class Admin:
        date_hierarchy = 'pub_date'
        fields = (
            ('Upload your own', {'fields': ('path',), 'classes': 'collapse'}),
            ('Publication details', {'fields': ('pub_date', 'title', 'slug', 'description', 'commentary', 'tags', 'enable_comments',)}),
            ('Details', {'fields': ('url', 'video_id', 'source', 'embed_code', 'running_time', 'rating', 'nsfw',)}),
            ('Related Material', {'fields': ('videos', 'people', 'places',), 'classes': 'collapse'}),
        )
        
        list_display    = ('title', 'url', 'source', 'pub_date', 'enable_comments',)
        search_fields   = ['title', 'description', 'source', 'people', 'url', 'tags']
        date_hierarchy  = 'created_on'


class VideoModerator(CommentModerator):
    akismet = settings.COMMENTS_AKISMET
    auto_moderate_field = 'pub_date'
    moderate_after = settings.COMMENTS_MODERATE_AFTER
    email_notification = settings.COMMENTS_EMAIL
    enable_field = settings.COMMENTS_ENABLE_FIELD
moderator.register(Video, VideoModerator)


dispatcher.connect(create_tumblelog_item, sender=Video, signal=signals.post_save)
dispatcher.connect(kill_tumblelog_item, sender=Video, signal=signals.post_delete)
