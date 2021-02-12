import os
from datetime import timedelta

from environ import Env
from raven import fetch_git_sha
from raven.exceptions import InvalidGitRepository

from ast import literal_eval

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert os.path.isfile(os.path.join(BASE_DIR, 'manage.py'))

#####################
# Local environment #
#####################
env = Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

########################
# Django core settings #
########################
DEBUG = env.bool('DEBUG', default=True)
TIER = env.str('TIER', default='dev')
SECRET_KEY = env.str('SECRET_KEY', default=('' if not DEBUG else 'xxx'))

ALLOWED_HOSTS = literal_eval(env.str('ALLOWED_HOSTS', default="['*']"))
#########
# Paths #
#########
default_var_root = os.path.join(BASE_DIR, 'var')
user_var_root = os.path.expanduser('~/var')
if os.path.isdir(user_var_root):
    default_var_root = user_var_root
VAR_ROOT = env.str('VAR_ROOT', default_var_root)

# Create var root if it doesn't exist
if not os.path.isdir(VAR_ROOT):
    os.makedirs(VAR_ROOT)

MEDIA_ROOT = os.path.join(VAR_ROOT, 'media')
MEDIA_URL = '/media/'
ROOT_URLCONF = 'parkkihubi.urls'
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
STATIC_URL = '/static/'
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
#     )
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
############
# Database #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER_RUNTIME'),
        'PASSWORD': env.str('DB_RUNTIME_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.int('DB_SERVICE_PORT')
    }
}
##########
# Caches #
##########
CACHES = {'default': env.cache_url(default='locmemcache://')}

##################
# Installed apps #
##################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'raven.contrib.django.raven_compat',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'django_filters',
    'parkkihubi',
    'parkings',
    'sanitized_dump',
] + env.list("EXTRA_INSTALLED_APPS", default=['parkkihubi_hel'])


if DEBUG and TIER == 'dev':
    # shell_plus and other goodies
    INSTALLED_APPS.append("django_extensions")

##############
# Middleware #
##############
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'parkkihubi.middleware.AdminTimezoneMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

#############
# Templates #
#############
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

##########
# Sentry #
##########
try:
    git_sha = fetch_git_sha(BASE_DIR)
except InvalidGitRepository:
    git_sha = None
RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', default=None),
    'release': git_sha,
}

############################
# Languages & Localization #
############################
LANGUAGE_CODE = env.str('LANGUAGE_CODE', default='en')
TIME_ZONE = env.str('TIME_ZONE', default='UTC')
ADMIN_TIME_ZONE = env.str('ADMIN_TIME_ZONE', default='Europe/Helsinki')
USE_I18N = True
USE_L10N = True
USE_TZ = True

########
# WSGI #
########
WSGI_APPLICATION = 'parkkihubi.wsgi.application'

##########
# Mailer #
##########
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', default=None)
EMAIL_PORT = env.int('EMAIL_PORT', default=None)
if env.bool('CONSOLE_EMAIL', default=False) == True:
    EMAIL_HOST = 'localhost'
else:
    EMAIL_HOST = env.str('EMAIL_HOST', default=None)
    EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default=None)
    EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default=None)
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)

#########################
# Django REST Framework #
#########################
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # Make nothing accessible to non-admins by default.  Viewsets
        # should specify permission_classes to override permissions.
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'parkings.authentication.ApiKeyAuthentication',
        'drf_jwt_2fa.authentication.Jwt2faAuthentication',
    ] + ([  # Following two are only for DEBUG mode in dev environment:
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ] if (DEBUG and TIER == 'dev') else []),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'ALLOWED_VERSIONS': ('v1',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'EXCEPTION_HANDLER': 'parkings.exception_handler.parkings_exception_handler',
    'PAGE_SIZE': 100,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(minutes=30),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}

JWT2FA_AUTH = {
    'CODE_TOKEN_THROTTLE_RATE': '5/15m',
    'AUTH_TOKEN_RETRY_WAIT_TIME': timedelta(seconds=10),
    'EMAIL_SENDER_SUBJECT_OVERRIDE': '{code} - PGS - verification code',
    'EMAIL_SENDER_BODY_OVERRIDE': (
        'Hi!\n'
        '\n'
        'Your verification code for login is: {code}\n'),
}

CORS_ORIGIN_ALLOW_ALL = True

##############
# Parkkihubi #
##############
PARKKIHUBI_TIME_PARKINGS_EDITABLE = timedelta(minutes=2)
PARKKIHUBI_TIME_OLD_PARKINGS_VISIBLE = timedelta(minutes=15)
PARKKIHUBI_NONE_END_TIME_REPLACEMENT = env.str(
    'PARKKIHUBI_NONE_END_TIME_REPLACEMENT', default='')
PARKKIHUBI_PUBLIC_API_ENABLED = env.bool('PARKKIHUBI_PUBLIC_API_ENABLED', True)
PARKKIHUBI_MONITORING_API_ENABLED = env.bool(
    'PARKKIHUBI_MONITORING_API_ENABLED', True)
PARKKIHUBI_OPERATOR_API_ENABLED = env.bool('PARKKIHUBI_OPERATOR_API_ENABLED', True)
PARKKIHUBI_ENFORCEMENT_API_ENABLED = (
    env.bool('PARKKIHUBI_ENFORCEMENT_API_ENABLED', True))
PARKKIHUBI_PERMITS_PRUNABLE_AFTER = timedelta(days=3)

DEFAULT_ENFORCEMENT_DOMAIN = (env.str('DEFAULT_ENFORCEMENT_DOMAIN', default='Helsinki'),
                              env.str('DEFAULT_ENFORCEMENT_DOMAIN_ABBREVIATION', default='HKI'))

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')