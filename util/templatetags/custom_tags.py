from django.template import Library, Node, TemplateSyntaxError
from django.db.models import get_model
from django.conf import settings
from tagging.models import Tag
from django.template.defaultfilters import stringfilter, date
from rewinder.apps.blog.models import Article
from rewinder.apps.flickr.models import Photo

import random

register = Library()

@register.simple_tag
def date_format(token):
    mdy = date(token, "F jS, Y")
    hma = date(token, "g:i a")
    return "%s at %s" % (mdy, hma)

@register.simple_tag
def utc_to_eastern(token):
    import pytz
    tz = pytz.timezone(settings.TIME_ZONE)
    loc_dt = token.replace(tzinfo=pytz.utc).astimezone(tz)
    mdy = date(loc_dt, "F jS, Y")
    hma = date(loc_dt, "g:i a")
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
    """
    get_latest_posts 3 as latest_posts
    """
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
    """
    get_latest delicious.Bookmark as latest_link
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])

class PopularTagsNode(Node):
    def __init__(self, limit, limit_varname, tags_varname, count_varname, top_count_varname):
        self.limit, self.limit_varname, self.tags_varname, self.count_varname, self.top_count_varname = limit, limit_varname, tags_varname, count_varname, top_count_varname
    
    def render(self, context):
        all_tags = Tag.objects.all()
        count = all_tags.count()
        tags = {}
        for tag in all_tags:
            tags[tag] = tag.items.count()
        items = tags.items()
        items = [(v, k) for (k, v) in items]
        items.sort()
        items.reverse()
        context[self.limit_varname] = self.limit
        context[self.count_varname] = count
        context[self.tags_varname] = items[:int(self.limit)]
        context[self.top_count_varname] = items[0][0]
        return ''
        
@register.tag(name="get_popular_tags")
def get_popular_tags(parser, token):
    """
    get_popular_tags 200 as limit tags total_count top_count
    """
    bits = token.contents.split()
    if len(bits) != 7:
        raise TemplateSyntaxError, "get_popular_tags tag takes exactly 6 arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to get_popular_tags tag must be 'as'"
    return PopularTagsNode(bits[1], bits[3], bits[4], bits[5], bits[6])


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

@register.tag(name="get_popular_tags_for")
def get_popular_tags_for(parser, token):
    """
    get_popular_tags_for delicious.Bookmark 40 as top_tags top_count
    """
    bits = token.contents.split()
    if len(bits) != 6:
        raise TemplateSyntaxError, "get_popular_tags tag takes exactly five arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_popular_tags tag must be 'as'"
    return TagCountForModelNode(bits[1], bits[2], bits[4], bits[5])


class RandomPhotoNode(Node):
    def __init__(self, varname, related_by_tag):
        self.varname, self.related_by_tag = varname, related_by_tag
    
    def render(self, context):
        photo = random.choice(Photo.sixminutes.all())
        tags = Tag.objects.get_for_object(photo)[:1]
        context[self.varname] = photo
        context[self.related_by_tag] = Photo.sixminutes.all().filter(tags__icontains=tags[0]).exclude(id__exact=photo.id)[:6]
        return ''

@register.tag(name="get_random_photo")
def get_random_photo(parser, token):
    """
    get_random_photo as photo related_photos
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_random_photo tag takes exactly 2 arguments"
    if bits[1] != 'as':
        raise TemplateSyntaxError, "first argument to get_random_photo tag must be 'as'"
    return RandomPhotoNode(bits[2], bits[3])


class RandomContentNode(Node):
    def __init__(self, model, pool, varname):
        self.pool, self.varname = pool, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        import random
        context[self.varname] = random.choice(self.model._default_manager.all()[:self.pool])
        return ''

@register.tag(name="get_random")
def get_random(parser, token):
    """
    get_random delicious.Bookmark 5 as random_link
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_random tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_random tag must be 'as'"
    return RandomContentNode(bits[1], bits[2], bits[4])


class RandomContentWithRelatedNode(Node):
    def __init__(self, model, num, varname, related, related_num, relator_varname):
        self.num, self.varname, self.related, self.related_num, self.relator_varname = num, varname, related, related_num, relator_varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        import random
        content = random.choice(self.model._default_manager.all()[:self.num])
        tags = content.tags.split()
        tag = random.choice(tags)
        try:
            related_content = self.model.objects.filter(tags__icontains=tag).exclude(id__exact=content.id)[:self.related_num]
            context[self.varname] = content
            context[self.related] = related_content
            context[self.relator_varname] = tag
        except IndexError:
            pass
        return ''

@register.tag(name="get_random_with_related")
def get_random_with_related(parser, token):
    """
    get_random_with_related delicious.Bookmark 5 as random_link related_links 3 relator
    """
    bits = token.contents.split()
    if len(bits) != 8:
        raise TemplateSyntaxError, "get_random tag takes exactly five arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_random tag must be 'as'"
    return RandomContentWithRelatedNode(bits[1], bits[2], bits[4], bits[5], bits[6], bits[7])
    
class DatesForModelNode(Node):
    def __init__(self, model, varname, field):
        self.varname, self.field = varname, field
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.dates(self.field, 'year').order_by('DESC')
        return ''

@register.tag(name="get_archive_dates")
def get_archive_dates(parser, token):
    """
    get_archive_dates delicious.Bookmark as archive date_field
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_archive_dates tag takes exactly four arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return DatesForModelNode(bits[1], bits[3], bits[4])