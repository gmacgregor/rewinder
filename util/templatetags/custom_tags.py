from django.template import Library, Node, TemplateSyntaxError
from django.db.models import get_model
from django.conf import settings
from django.template.defaultfilters import stringfilter, date
from rewinder.apps.blog.models import Article

register = Library()

@register.filter(name='twitter_links')
@stringfilter
def twitter_links(tweet):
    """
    Takes a twitter tweet and makes all @'s link to the @owner profile. 
    Also creates links to URLs.
    """
    import re
    url_re = re.compile('(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
    tweeter_re = re.compile('[A-Za-z0-9]+')
    words = tweet.split()
    li = []
    for word in words:
        if word.startswith('@'):
            owner = re.search(tweeter_re, word).group(0)
            word = '<a href="http://twitter.com/%s/" title="Go to %s\'s Twitter page">%s</a>' % (owner, owner, word)
        if url_re.match(word):
            word = '<a href="%s" title="Visit this link">%s</a>' % (word, word)
        li.append(word)
    return ' '.join(li)


class LatestArticleNode(Node):
    def __init__(self, num, varname):
        self.num, self.varname = num, varname
    
    def render(self, context):
        context[self.varname] = Article.published_articles.all()[:self.num]
        return ''

@register.tag(name="get_latest_posts")
def get_latest_posts(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_latest_posts tag takes exactly four arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest_posts tag must be 'as'"
    return LatestArticleNode(bits[1], bits[3])


class LatestContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''

@register.tag(name="get_latest")
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])

@register.simple_tag
def date_format(token):
    mdy = date(token, "F jS, Y")
    hma = date(token, "g:i a")
    return "%s at %s" % (mdy, hma)