import logging

from .base import *  # NOQA


DEBUG = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

if os.getenv('CI') == 'true':
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'circle_test',
        'USER': 'ubuntu',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }


SOUTH_TESTS_MIGRATE = False

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

logging.disable(logging.ERROR)
