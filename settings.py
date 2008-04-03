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
MEDIA_URL = 'http://localhost/site_media/'

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
    'django.contrib.comments',
    'tagging',
    'typogrify',
    'rewinder.apps.blog',
    'rewinder.apps.links',
    'rewinder.apps.video',
    'rewinder.apps.places',
    'rewinder.apps.quirp',
    'rewinder.apps.tumblelog',
    'rewinder.apps.photos',
    'rewinder.util',
    'syncr.flickr',
    'syncr.youtube',
    'syncr.delicious',
    'syncr.twitter',
)
# http://www.b-list.org/weblog/2007/nov/03/working-models/
# app label (normalized to lowercase), model name (normalized to lowercase)
TUMBLELOG_MODELS = ('quirp.quirp','video.video','links.link', 'delicious.bookmark')

#http://code.google.com/p/django-template-utils/
MARKUP_FILTER = ('markdown', {})

DELICIOUS_USERNAME = 'sixminutes'
DELICIOUS_PASSWORD = 'faerie'

FORCE_LOWERCASE_TAGS = True

TWITTER_USERNAME = 'gmacgregor'