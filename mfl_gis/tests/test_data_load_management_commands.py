from common.tests.test_models import BaseTestCase
from django.core.management import call_command


class TestLoadKenyaBoundaries(BaseTestCase):
    def test_default_load(self):
        call_command('load_kenyan_administrative_boundaries')
