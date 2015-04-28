import os

from common.tests.test_models import BaseTestCase
from django.core.management import call_command
from django.conf import settings
from django.core.management import CommandError

from mfl_gis.management.commands.shared import _get_mpoly_from_geom


class TestLoadKenyaBoundaries(BaseTestCase):
    def test_default_load(self):
        county_files = os.path.join(
            settings.BASE_DIR, 'data/data/0001_counties.json')
        constituencies_files = os.path.join(
            settings.BASE_DIR, 'data/data/0002_constituencies.json')
        wards_files = os.path.join(
            settings.BASE_DIR, 'data/data/0009_wards.json')

        call_command('bootstrap', county_files)
        call_command('bootstrap', constituencies_files)
        call_command('bootstrap', wards_files)

        call_command('load_world_boundaries')
        call_command('load_kenyan_administrative_boundaries')

        # Test the handling of the "existing records" path
        call_command('load_world_boundaries')
        call_command('load_kenyan_administrative_boundaries')

    def test_get_mpoly_from_geom(self):
        with self.assertRaises(CommandError) as c:
            _get_mpoly_from_geom(None)

        self.assertEqual(
            c.exception.message,
            "Expected a Polygon or MultiPolygon, got <type 'NoneType'>"
        )

    def test_load_boundaries_non_existent_geographic_area(self):
        with self.assertRaises(CommandError):
            call_command('load_kenyan_administrative_boundaries')
