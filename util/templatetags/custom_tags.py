from django.template import Library, Node, TemplateSyntaxError
from django.conf import settings
from datetime import datetime
from time import strptime
import twitter
import random

register = Library()

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