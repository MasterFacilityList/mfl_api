import os

from common.tests.test_models import BaseTestCase
from django.core.management import call_command
from django.conf import settings
from django.core.management import CommandError

from mfl_gis.management.commands.shared import _get_mpoly_from_geom
from ..models import (
    WorldBorder, CountyBoundary, ConstituencyBoundary, WardBoundary)


class TestLoadKenyaBoundaries(BaseTestCase):

    def test_default_load(self):
        county_files = os.path.join(
            settings.BASE_DIR, 'data/data/admin_units/0001_counties.json')
        constituencies_files = os.path.join(
            settings.BASE_DIR,
            'data/data/admin_units/0002_constituencies.json')
        wards_files = os.path.join(
            settings.BASE_DIR, 'data/data/admin_units/0009_wards.json')

        call_command('bootstrap', county_files)
        call_command('bootstrap', constituencies_files)
        call_command('bootstrap', wards_files)

        call_command('load_world_boundaries')
        call_command('load_kenyan_administrative_boundaries')

        # Test the handling of the "existing records" path
        call_command('load_world_boundaries')
        call_command('load_kenyan_administrative_boundaries')

        # Take advantage of this to confirm that we can resolve the
        # .geometry class for Kenya, every county, every constituency and
        # every ward
        ken = WorldBorder.objects.get(code='KEN')
        assert ken.geometry

        for county_boundary in CountyBoundary.objects.all():
            assert county_boundary.geometry

        for constituency_boundary in ConstituencyBoundary.objects.all():
            assert constituency_boundary.geometry

        for ward_boundary in WardBoundary.objects.all():
            assert ward_boundary.geometry

    def test_get_mpoly_from_geom(self):
        with self.assertRaises(CommandError) as c:
            _get_mpoly_from_geom(None)

        self.assertEqual(
            c.exception.message,
            "Expected a Polygon or MultiPolygon, got <type 'NoneType'>"
        )

    def test_fallback_path(self):
        # No boundaries defined, should raise
        with self.assertRaises(CommandError):
            call_command('load_kenyan_administrative_boundaries')
