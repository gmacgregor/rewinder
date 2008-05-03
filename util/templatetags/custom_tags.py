from django.template import Library, Node, TemplateSyntaxError
from django.db.models import get_model
from django.conf import settings
from tagging.models import Tag
from django.template.defaultfilters import stringfilter, date
from rewinder.apps.blog.models import Article
from rewinder.apps.flickr.models import Photo


register = Library()

@register.simple_tag
def date_format(token):
    mdy = date(token, "F jS, Y")
    hma = date(token, "g:i a")
    return "%s at %s" % (mdy, hma)


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
            try:
                owner = re.search(tweeter_re, word).group(0)
                word = '<a href="http://twitter.com/%s/" title="Go to %s\'s Twitter page">%s</a>' % (owner, owner, word)
            except:
                pass
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

class TagCountForModelNode(Node):
    def __init__(self, model, num, varname, count_name):
        self.num, self.varname, self.top_count = num, varname, count_name
        self.model = get_model(*model.split('.'))

    def render(self, context):
        num = int(self.num)
        tags = Tag.objects.usage_for_model(self.model, counts=True)
        items = [(tag.count, tag.name) for tag in tags]
        items.sort()
        items.reverse()
        items = items[:num]
        context[self.varname] = items
        context[self.top_count] = items[0][0]
        return ''

@register.tag(name="get_popular_tags")
def get_popular_tags(parser, token):
    bits = token.contents.split()
    if len(bits) != 6:
        raise TemplateSyntaxError, "get_popular_tags tag takes exactly five arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_popular_tags tag must be 'as'"
    return TagCountForModelNode(bits[1], bits[2], bits[4], bits[5])


class RandomPhotoNode(Node):
    def __init__(self, varname):
        self.varname = varname
    
    def render(self, context):
        import random
        photos = Photo.objects.all().filter(owner='sixminutes')
        context[self.varname] = random.choice(photos)
        return ''

@register.tag(name="get_random_photo")
def get_popular_tags(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "get_random_photo tag takes exactly 2 arguments"
    if bits[1] != 'as':
        raise TemplateSyntaxError, "first argument to get_random_photo tag must be 'as'"
    return RandomPhotoNode(bits[2])