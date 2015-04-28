import os

from common.tests.test_models import BaseTestCase
from django.core.management import call_command
from django.conf import settings


class TestLoadKenyaBoundaries(BaseTestCase):
    def test_default_load(self):
        data_files = os.path.join(settings.BASE_DIR, 'data/data/*')
        call_command('bootstrap', data_files)
        call_command('load_kenyan_administrative_boundaries')
