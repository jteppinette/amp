import os

# ROOT
ROOT = os.path.dirname(os.path.dirname(__file__))

# DEBUG
DEBUG = True

# COMPANY SETTINGS
APP_URL = 'http://localhost:8080'
COMPANY_NAME = 'LUS'

# TEMPLATES
TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [
    os.path.join(ROOT, 'templates'),
]

# AUTH
AUTH_USER_MODEL = 'authentication.User'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'

# INSTALLED APPS
INSTALLED_APPS = (
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'authentication'
)

# MIDDLEWARE
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# URLS
ROOT_URLCONF = 'project.urls'

# WSGI
WSGI_APPLICATION = 'project.wsgi.application'

# STATIC ASSETS
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(ROOT, 'media')
MEDIA_URL = '/media/'
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(ROOT, 'static')),
)

# MAIL
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/amp-mail'

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# SECURITY
SECRET_KEY = 'cmttfpnk9+6^vs0ow=umgt3$bue+pm=a&-n&$&6@%ww9gpl2x@'

# HEADER MANAGEMENT
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
