# Django settings for sixminutes project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Greg MacGregor', 'gmacgregor@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'rewinder.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

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
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/Users/gmacgregor/dev/rewinder/site_media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'y#h#&g^gba9=#x@q#v)a(-##s4$f6$r%vm9#%=b5s=d)v0+=^p'

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
)

ROOT_URLCONF = 'rewinder.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/Users/gmacgregor/dev/rewinder/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
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
#TUMBLELOG_MODELS = ('blog.article','delicious.bookmark','flickr.photo','twitter.tweet')

#http://code.google.com/p/django-template-utils/
MARKUP_FILTER = ('markdown', {})

DEFAULT_MARKUP = 1
DEFAULT_MAX_COMMENT_LENGTH = '2000'
DEFAULT_MAX_COMMENT_DEPTH = '5'

GRAVATAR_DEFAULT_IMG = 'http://up1.vox.com/6a00c2251e54f18fdb00c2251f46818e1d-50si'
GRAVATAR_SIZE = 50

#tagging
FORCE_LOWERCASE_TAGS = True

#comment_utils
AKISMET_API_KEY = '2d963b0633db'
COMMENTS_AKISMET = True
COMMENTS_CLOSE_AFTER = 14
COMMENTS_EMAIL = True
COMMENTS_ENABLE_FIELD = 'enable_comments'

RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'), 
)

FLICKR_API_KEY = 'c5b82d5a4ae7101366113790d947da9e'
FLICKR_API_SECRET = '072822dd97710515'

YOUTUBE_API_KEY = 'AI39si7dE0uopXa7u6wVFzAQZF0_B3NOtztaYqK9pLzSafZOu7TScU-g2dvLmaMEmgpvocgoCGnZQUBUGMjr-4MnxfulgA7KWA'
YOUTUBE_DEV_ID = 'MlRUm9Gt1ro'

DIGG_AUTH = 'http://www.example.com/digg'

DELICIOUS_USERNAME = 'sixminutes'
DELICIOUS_PASSWORD = 'faerie'
#TWITTER_USERNAME = 'gmacgregor'