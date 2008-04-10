from django.db import models
from tagging.fields import TagField


class Video(models.Model):
    feed                = models.URLField()
    video_id            = models.CharField(max_length=50)
    published           = models.DateTimeField()
    updated             = models.DateTimeField()
    title               = models.CharField(max_length=250)
    author              = models.ForeignKey('YoutubeUser')
    description         = models.TextField(blank=True)
    tags                = TagField()
    view_count          = models.PositiveIntegerField()
    url                 = models.URLField()
    thumbnail_url       = models.URLField()
    length              = models.PositiveIntegerField()
    #enable_comments     = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def save(self):
        super(Video, self).save()
    
    def embed_url(self):
        return u'http://www.youtube.com/v/%s' % self.video_id
    
    #def embed_code(self):
    #    return '<object width="%s" height="250"><param name="movie" value="http://www.youtube.com/v/wnVJZkDuVBM&hl=en&rel=0&color1=0x3a3a3a&color2=0x999999"></param><param name="wmode" value="transparent"></param><embed src="http://www.youtube.com/v/wnVJZkDuVBM&hl=en&rel=0&color1=0x3a3a3a&color2=0x999999" type="application/x-shockwave-flash" wmode="transparent" width="300" height="250"></embed></object>'
    
    class Meta:
        ordering = ('-published',)
    
    class Admin:
        list_display = ('title', 'author', 'video_id', 'view_count')
    


class Playlist(models.Model):
    feed                = models.URLField()
    updated             = models.DateTimeField()
    title               = models.CharField(max_length=200)
    description         = models.TextField(blank=True)
    author              = models.ForeignKey('YoutubeUser')
    url                 = models.URLField()
    videos              = models.ManyToManyField('PlaylistVideo')
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def numVideos(self):
        return self.videos.count()
    
    class Admin:
        list_display = ('title', 'description', 'author', 'numVideos')


class PlaylistVideo(models.Model):
    feed                = models.URLField()
    title               = models.CharField(max_length=250)
    description         = models.TextField(blank=True)
    original            = models.ForeignKey('Video')
    
    def __unicode__(self):
        return u'%s' % self.title
    
    class Admin:
        list_display = ('title', 'description')


class YoutubeUser(models.Model):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    feed                = models.URLField()
    username            = models.CharField(max_length=50)
    first_name          = models.CharField(max_length=50)
    age                 = models.PositiveIntegerField(null=True, blank=True)
    gender              = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    thumbnail_url       = models.URLField()
    watch_count         = models.PositiveIntegerField()
    url                 = models.URLField()
    playlists           = models.ManyToManyField('Playlist')
    favorites           = models.ManyToManyField('Video')
    
    def __unicode__(self):
        return u'%s' % self.username
    
    class Admin:
        list_display = ('username', 'first_name', 'age', 'gender', 'watch_count')
