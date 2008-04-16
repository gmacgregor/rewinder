from django.template import Library, Node, TemplateSyntaxError
from django.conf import settings
from django.template.defaultfilters import stringfilter

from datetime import datetime
from time import strptime

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
    

@register.filter(name='with_links')
@stringfilter
def with_links(tweet):
    '''
    Takes a twitter tweet and makes all @'s link to the @owner profile. Also creates links to URLs
    '''
    import re
    reg = re.compile('(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
    words = tweet.split()
    li = []
    for word in words:
        if word.find('@') != -1:
            owner = word.replace('@','')
            if owner.isalpha():
                word = '<a href="http://twitter.com/%s" title="Go to %s\'s Twitter page">%s</a>' % (owner, owner, word)
        if reg.match(word):
            word = '<a href="%s" title="Visit this link">%s</a>' % (word, word)
        li.append(word)
    return ' '.join(li)