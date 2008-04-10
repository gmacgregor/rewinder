from django.template import Library, Node, TemplateSyntaxError
from django.conf import settings
from datetime import datetime
from time import strptime

from rewinder.apps.youtube.models import Video

import random

register = Library()

class YoutubeVideoEmbedNode(Node):
    def __init__(self, video):
        self.video = video
    
    def render(self, context):
        video = Video.objects.get(video_id=self.video.video_id)
        parts =  '<object width="300" height="250"><param name="movie" value="http://www.youtube.com/v/wnVJZkDuVBM&hl=en&rel=0&color1=0x3a3a3a&color2=0x999999"></param>' % (settings.YOUTUBE_EMBED_WIDTH, settings.YOUTUBE_EMBED_HEIGHT, video.video_id)
        parts = parts.join('<param name="wmode" value="transparent"></param>')
        parts = parts.join('<embed src="http://www.youtube.com/v/%s&hl=en&rel=0&color1=0x3a3a3a&color2=0x999999" type="application/x-shockwave-flash" wmode="transparent" width="%s" height="%s"></embed></object>' % (settings.YOUTUBE_EMBED_WIDTH, settings.YOUTUBE_EMBED_HEIGHT, video.video_id))
        context[self.embed_code] = parts
        return ''

@register.tag(name='embed_video')
def video_embed_code(parser, token):
    """
    Call this tag with: 
        get_twitter_status as tweet
    """
    bits = token.split_contents()
    if len(bits) != 3:
            raise TemplateSyntaxError, "%s takes 2 arguments" % bits[0] 
    if bits[1] = "for":
        raise TemplateSyntaxError, "First argument for %s should be 'for'" % bits[0] 
    return YoutubeVideoEmbedNode(bits[2])


class RandomTitleNode(Node):
    def __init__(self, title):
        self.title = title
    
    def render(self, context):
        titles = [
            "hoopla!",
            "coffee me!",
            "I'm in yr base...",
            "Julius Caesar or rollerblades? Why?",
            "I should have been in bed 3 hours ago",
        ]
        choice = random.choice(titles)
        context[self.title] = choice
        return ''

@register.tag(name='get_random_title')
def random_title(parser, token):
    """ get_random_title as title """
    bits = token.split_contents()
    if len(bits) != 3:
        raise TemplateSyntaxError, "%s takes 2 arguments" % bits[0]
    if bits[1] != "as":
        raise TemplateSyntaxError, "First argument for %s should be 'as'" % bits[0] 
    return RandomTitleNode(bits[2])

class TwitterStatusNode(Node):
    def __init__(self, tweet):
        self.tweet = tweet
    
    def render(self, context):
        import twitter
        try:
            api = twitter.Api()
            most_recent_status = api.GetUserTimeline(settings.TWITTER_USERNAME)[0]
            context[self.tweet] = {
                "status": "%s" % most_recent_status.text,
                "url": "http://twitter.com/%s/statuses/%s" % (settings.TWITTER_USERNAME, most_recent_status.id),
                "time": "%s" % most_recent_status.relative_created_at,
            }           
        except:
            context[self.tweet] = {
                "status": "Ack! Looks like Twitter's codes are broken!",
                "url": "",
                "time": "",
            }           
        return ''

@register.tag(name='get_twitter_status')
def twitter_status(parser, token):
    """
    Call this tag with: 
        get_twitter_status as tweet
    """
    bits = token.split_contents()
    if len(bits) != 3:
            raise TemplateSyntaxError, "%s takes 2 arguments" % bits[0] 
    if bits[1] != "as":
        raise TemplateSyntaxError, "First argument for %s should be 'as'" % bits[0]
    return TwitterStatusNode(bits[2])