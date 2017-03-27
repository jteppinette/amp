"""
Django settings for amp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cmttfpnk9+6^vs0ow=umgt3$bue+pm=a&-n&$&6@%ww9gpl2x@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
]

ALLOWED_HOSTS = []

# Authentication
AUTH_USER_MODEL = 'authentication.User'

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'

# Application definition

INSTALLED_APPS = (
    'bootstrapforms',
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'amp.urls'

WSGI_APPLICATION = 'amp.wsgi.application'

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if DEBUG:

    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    MEDIA_ROOT = BASE_DIR 
    MEDIA_URL = '/media/'

else:

    DEFAULT_FILE_STORAGE = 'api.util.storages.PrefixedStorage'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    STATIC_ROOT = 'staticfiles'
    STATIC_URL = 'http://s3.amazonaws.com/gdsamp/'

    AWS_ACCESS_KEY_ID = 'AKIAI53U4MXHDBTSOBWA'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'gdsamp'

    MEDIA_ROOT = 'media'
    MEDIA_URL = 'https://s3.amazonaws.com/gdsamp/media/'

STATICFILES_DIRS = (
    os.path.abspath(os.path.join(BASE_DIR, '..', 'static')),
    os.path.abspath(os.path.join(BASE_DIR, '..', 'app', 'static')),
)

# Mail
import os
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587

if DEBUG:
    EMAIL_HOST_USER = 'app26343405@heroku.com'
    EMAIL_HOST_PASSWORD = 'IYZR90-QFNR60BxjxcifhA'
else:
    EMAIL_HOST_USER = os.environ['MANDRILL_USERNAME']
    EMAIL_HOST_PASSWORD = os.environ['MANDRILL_APIKEY']

EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'notfications@gdsamp.com'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'amp',
            'USER': 'postgres',
            'PASSWORD': 'test',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }
else:
    import dj_database_url
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Honor the `X-Forwarded-Proto` header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
