DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('', ''),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'America/Toronto'
#TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/gmacgregor/webapps/static_media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.rewinder.ca/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'KEY'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'rewinder.lib.sql_debug.SqlPrintingMiddleware',
)

ROOT_URLCONF = 'rewinder.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/gmacgregor/webapps/django/rewinder/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django_evolution',
    #'django.contrib.comments',
    'threadedcomments',
    #template utils -- ie. using markdown for presentation
    'template_utils',
    'tagging',
    'typogrify',
    'comment_utils',
    'rewinder.apps.blog',
    'rewinder.apps.tumblelog',
    'rewinder.apps.delicious',
    'rewinder.apps.flickr',
    'rewinder.apps.twitter',
    'rewinder.apps.video',
    'rewinder.apps.generic',
    'rewinder.apps.geo',
    'rewinder.util', #templatetags
)

CACHE_BACKEND = ''

#http://code.google.com/p/django-template-utils/
MARKUP_FILTER = ('markdown', {})

DEFAULT_MARKUP = 1
DEFAULT_MAX_COMMENT_LENGTH = '2000'
DEFAULT_MAX_COMMENT_DEPTH = '5'

GRAVATAR_DEFAULT_IMG = MEDIA_URL + 'icons/gravatar.png'
GRAVATAR_SIZE = 50

#tagging
FORCE_LOWERCASE_TAGS = True

#comment_utils
AKISMET_API_KEY = ''
COMMENTS_AKISMET = True
COMMENTS_CLOSE_AFTER = 60
COMMENTS_MODERATE_AFTER = 30
COMMENTS_EMAIL = True
COMMENTS_ENABLE_FIELD = 'enable_comments'

RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'), 
)

FLICKR_API_KEY = ''
FLICKR_API_SECRET = ''

YOUTUBE_API_KEY = ''
YOUTUBE_DEV_ID = ''

DIGG_AUTH = ''

DELICIOUS_USERNAME = ''
DELICIOUS_PASSWORD = ''