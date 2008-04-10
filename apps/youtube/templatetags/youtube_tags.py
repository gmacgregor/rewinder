from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError
from rewinder.apps.youtube.models import Video

register = Library()

class YoutubeVideoEmbedNode(Node):
    def __init__(self, video):
        print video
        self.video_id = None
        #self.video_id = video_id
        self.embed_code = None
    
    def render(self, context):
        parts =  '<object width="%s" height="%s"><param name="movie" value="http://www.youtube.com/v/%s&hl=en&rel=0&color1=0x3a3a3a&color2=0x999999"></param>' % (settings.YOUTUBE_EMBED_WIDTH, settings.YOUTUBE_EMBED_HEIGHT, self.video_id)
        parts = parts.join('<param name="wmode" value="transparent"></param>')
        parts = parts.join('<embed src="http://www.youtube.com/v/%s&hl=en&rel=0&color1=0x3a3a3a&color2=0x999999" type="application/x-shockwave-flash" wmode="transparent" width="%s" height="%s"></embed></object>' % (settings.YOUTUBE_EMBED_WIDTH, settings.YOUTUBE_EMBED_HEIGHT, self.video_id))
        context[self.embed_code] = parts
        return ''

@register.tag(name='get_embed_code')
def video_embed_code(parser, token):
    """
    Call this tag with: 
        get_twitter_status as tweet
    """
    bits = token.split_contents()
    if len(bits) != 3:
        raise TemplateSyntaxError, "%s takes 2 arguments" % bits[0]
    if bits[1] != "for":
        raise TemplateSyntaxError, "First argument for %s should be 'for'" % bits[0]
    return YoutubeVideoEmbedNode(bits[2])

