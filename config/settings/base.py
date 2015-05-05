import os
import environ

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# The env based settings are non-forgiving, intentionally
# If you do not have a setting...a kinder outcome will be had if the app
# blows up at the first opportunity
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
ENV_DB = env.db()
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': ENV_DB['HOST'],
        'NAME': ENV_DB['NAME'],
        'PASSWORD': ENV_DB['PASSWORD'],
        'PORT': ENV_DB['PORT'],
        'USER': ENV_DB['USER'],
    }
}  # Env should have DATABASE_URL
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
ALLOWED_HOSTS = ['.ehealth.or.ke', '.slade360.co.ke', '.localhost']
INSTALLED_APPS = (
    'users',
    'django.contrib.admin',
    'common',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'corsheaders',
    'rest_framework_swagger',
    'django.contrib.gis',
    'reversion',
    'django_extensions',
    'gunicorn',
    'facilities',
    'data_bootstrap',
    'chul',
    'data',
    'mfl_gis',
)
# LOCAL_APPS is now just a convenience setting for the metadata API
# It is *NOT* appended to INSTALLED_APPS ( **deliberate** DRY violation )
# This was forced by the need to override rest_framework templates in common
# It is a list because order matters
LOCAL_APPS = [
    'users',
    'common',
    'facilities',
    'chul',
    'mfl_gis',
    'data_bootstrap',
    'data',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
AUTH_USER_MODEL = 'users.MflUser'
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'  # This is INTENTIONAL
USE_TZ = True
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False  # Turn on in production
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_METADATA_CLASS': 'common.metadata.CustomMetadata',
    'PAGINATE_BY': 25,
    'PAGINATE_BY_PARAM': 'page_size',
    # Should be able to opt in to see all wards at once
    'MAX_PAGINATE_BY': 1500,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DATETIME_FORMAT': 'iso-8601',
    'DATE_FORMAT': 'iso-8601',
    'TIME_FORMAT': 'iso-8601'
}
SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '2.0',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': True,
    'is_superuser': False,
    'info': {
        'contact': 'developers@savannahinformatics.com',
        'description': 'Explore the MFL v2 API',
        'license': 'MIT License',
        'licenseUrl': 'http://choosealicense.com/licenses/mit/',
        'title': 'MFL v2 API',
    },
    'doc_expansion': 'full',
}
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60  # One hour
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s: %(asctime)s [%(module)s] %(message)s'  # NOQA
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'rest_framework': {
            'handlers': ['console'],
            'level': 'ERROR'
        },
        'common': {
            'handlers': ['console'],
            'level': 'ERROR'
        },
        'facilities': {
            'handlers': ['console'],
            'level': 'ERROR'
        },
        'users': {
            'handlers': ['console'],
            'level': 'ERROR'
        },
        'data_bootstrap': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'mfl_gis': {
            'handlers': ['console'],
            'level': 'ERROR'
        }
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': os.path.join(BASE_DIR, '/common/templates/'),
        'APP_DIRS': True,
    },
]
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
        'TIMEOUT': 60 * 60,
        'OPTIONS': {
            'MAX_ENTRIES': 10000
        }
    }
}
# django-allauth related settings
# some of these settings take into account that the target audience
# of this system is not super-savvy
LOGIN_REDIRECT_URL = '/api/'

SEARCH = {
    "ELASTIC_URL": "http://localhost:9200/",
    "INDEX_NAME": "mfl_index"
}

OAUTH2_PROVIDER_APPLICATION_MODEL = 'users.MFLOAuthApplication'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Master Facilities List]'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/api/'
ACCOUNT_SESSION_REMEMBER = True

# django_rest_auth settings
OLD_PASSWORD_FIELD_ENABLED = True
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.MflUserSerializer'
}
