from django.conf import settings
from django.template import defaultfilters
#from rewinder.apps.links.models import Link

#import pydelicious

from BeautifulSoup import BeautifulSoup

#def import_links():
try:
    f = open('/Users/gmacgregor/Desktop/delicious.html', 'r')
    soup = BeautifulSoup(f)
    soup.prettify()
    dts = soup.findAll('dt')
    for dt in dts:
        if dt.nextSibling:
            if dt.nextSibling.name == 'dd':
                description = dt.nextSibling.contents[0]
            else:
                description = ''
        url = dt.a.attrs[0][1]
        title = dt.next.contents[0]
        slug = defaultfilters.slugify(title)
        pub_date = dt.a.attrs[2][1]
        tags = dt.a.attrs[3][1]
        print tags
        #l = Link(pub_date=pub_date, url=url, title=title, slug=slug, description=description, tags=tags, post_elsewhere=False)
        #l.save()
except IOError:
    print  "input file %s wasn't found" % path

def import_all():
    """
    'extended': '', 'hash': 'e964d994d482b8032d119d6133348050', 'description': "Color + Design Blog / Some Summer Color Lovin' Inspiration by COLOURlovers", 'tag': 'design colour inspiration palettes resource', 'href': 'http://www.colourlovers.com/blog/2007/07/17/some-summer-color-lovin/', 'time': '2007-07-18T15:30:56Z'}
    
    pub_date            = models.DateTimeField(default=datetime.datetime.today)
    url                 = models.URLField(u'URL', max_length=250, unique=True, verify_exists=False)
    title               = models.CharField(max_length=250)
    slug                = models.SlugField(prepopulate_from=('title',), unique_for_date='pub_date', help_text=u'Must be unique for the publication date.')  
    description         = models.CharField(max_length=250, blank=True)
    tags                = TagField()
    via_name            = models.CharField(u'Via', max_length=250, blank=True, null=True, help_text=u'The name of the person whose site you spotted the link on. Optional.')
    via_url             = models.URLField(u'Via URL', verify_exists=False, blank=True, null=True, help_text=u'The URL of the site where you spotted the link. Optional.')   
    enable_comments     = models.BooleanField(default=True)
    post_elsewhere      = models.BooleanField(u'Post to del.icio.us', default=True, help_text=u'If checked, this link will be posted both to your weblog and to your del.icio.us account.')
    update_elsewhere
    
    """
    api = pydelicious.apiNew(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD)
    all_posts = api.posts_all()
    for post in all_posts['posts']:
        print "Saving " + post['description'] + "..."
        l = Link(
            pub_date=post['time'],
            url=post['href'],
            title=post['description'],
            slug=defaultfilters.slugify(post['description']),
            description=post['extended'],
            tags=post['tag'],
            post_elsewhere=False
        )
        l.save()

def delete_all():
    links = Link.objects.all()
    for link in links:
        print "Deleting %s ..." % link
        link.delete()
 
    
def get_posts():
    qs = pydelicious.get(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD)
    for post in qs['posts']:
        print post

    
def update():
    #api = pydelicious.apiNew(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD)
    pass
    