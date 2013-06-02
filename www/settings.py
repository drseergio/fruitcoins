# -*- coding: utf-8 -*-
from djcelery import setup_loader
from os.path import dirname
from os.path import join
from os.path import realpath
from sys import argv

setup_loader()

DEBUG = True
CAPTCHA = False
TEMPLATE_DEBUG = DEBUG
ADMIN_ENABLED = True
COMPRESS_HTML = False

PROJECT_ROOT = realpath(dirname(__file__))

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
)

INSTALLED_APPS += (
    'social_auth',
    'djcelery',
    'emailconfirmation',
    'sentry',
    'raven.contrib.django',
    'piston',
    'filetransfers'
)

INSTALLED_APPS += (
    'api',       # REST API that powers the app
    'core',      # the application
    'fx',        # currency handling
    'mobile'     # mobile version
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
        'NAME': 'moneypit',
        'USER': 'moneypit',
        'PASSWORD': '',
        'HOST': '/var/run/mysqld/mysqld.sock',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

TIME_ZONE = 'Europe/Zurich'

SECRET_KEY = ''

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'core.middleware.MinifyHTMLMiddleware',
    'api.middleware.NotFound',
    'minidetector.Middleware'
)

if 'test' in argv:
  DATABASES['default'] = {'ENGINE': 'sqlite3'}
  MIDDLEWARE_CLASSES += (
    'api.middleware.InsertWealth',)

AUTHENTICATION_BACKENDS = (
#    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
#    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
#    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
#    'social_auth.backends.contrib.orkut.OrkutBackend',
#    'social_auth.backends.contrib.foursquare.FoursquareBackend',
#    'social_auth.backends.contrib.github.GithubBackend',
#    'social_auth.backends.contrib.dropbox.DropboxBackend',
#    'social_auth.backends.contrib.flickr.FlickrBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'facebook', 'linkedin')

TEMPLATE_LOADERS = (
   'django.template.loaders.filesystem.Loader',
   'django.template.loaders.app_directories.Loader',
   'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_type_backends',
)

SITE_ID = 1
ROOT_URLCONF = 'urls'

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_URL = '/files/'
STATIC_URL = '/static/'

GEOIP_PATH = join(dirname(__file__), 'geoip')

LOGIN_URL          = '/user/login'
LOGOUT_URL         = '/user/logout'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/user/login'
CURRENCY_URL       = '/user/currency'
EMAIL_CONFIRMATION_DAYS = 2
INVITE_ONLY        = False

FEEDBACK_EMAIL = 'feedback@fruitcoins.com'
SENDER_EMAIL = 'noresponse@fruitcoins.com'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/moneypit-messages'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_EXTRA_DATA = False
SOCIAL_AUTH_CREATE_USERS = not INVITE_ONLY
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''
LINKEDIN_CONSUMER_KEY = ''
LINKEDIN_CONSUMER_SECRET = ''
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

TEMPLATE_DIRS = (join(dirname(__file__), 'templates'),)
MEDIA_ROOT = '/var/uploads'

ADMINS = (
    ('Sergey Pisarenko', 'drseergio@gmail.com'),
)

MANAGERS = ADMINS

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
       'simple': {
            'format': '%(asctime)s %(levelname)s: %(message)s [%(module)s]'
        },
    },
    'handlers': {
        'file':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/uwsgi/moneypit-debug.log',
         }
    },
    'loggers': {
       'core': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'fx': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'exporter': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'importer': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'logic': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'social_auth': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'api': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
   }
}

MAX_TRANSACTIONS_PER_PAGE = 500
DEFAULT_TRANSACTIONS_PER_PAGE = 30
RATE_URL = 'http://quote.yahoo.com/d/quotes.csv?s=%s%s=X&f=l1'
CURRENCY_RATE_VALIDITY = 20 * 60  # 20 minutes
MAX_IMPORT_SIZE = 100 * 1024  # 100 KB
MAX_RECEIPTS = 20
MAX_RECEIPT_DIMENSION = 1200 
MAX_RECEIPT_SIZE = 5 * 1024 * 1024  # 5MB
RECEIPT_STORAGE = 'receipts'
ANALYTICS_ID = 'XXXXX'

try:
  from local_settings import *
except ImportError:
  pass
