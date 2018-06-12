from model_mommy import mommy
from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError
from common.tests.test_models import BaseTestCase

from ..models import (
    GeoCodeSource, GeoCodeMethod, FacilityCoordinates, WorldBorder)


class TestWorldBoundaryModel(BaseTestCase):

    def test_geom_property(self):
        self.assertEqual(WorldBorder().geometry, {})


class TestGeoCodeSourceModel(BaseTestCase):

    def test_save(self):
        data = {
            "name": "Kenya Medical Research Institute",
            "description": "",
            "abbreviation": "KEMRI"
        }
        data = self.inject_audit_fields(data)
        GeoCodeSource.objects.create(**data)
        self.assertEquals(1, GeoCodeSource.objects.count())


class TesGeoCodeMethodModel(BaseTestCase):

    def test_save(self):
        data = {
            "name": "Taken with GPS device",
            "description": "GPS device was used to get the geo codes"
        }
        data = self.inject_audit_fields(data)
        GeoCodeMethod.objects.create(**data)
        self.assertEquals(1, GeoCodeMethod.objects.count())

    def test_deletion(self):
        method = mommy.make(GeoCodeMethod)
        mommy.make(GeoCodeMethod)
        self.assertEquals(2, GeoCodeMethod.objects.count())
        method.delete()
        self.assertEquals(1, GeoCodeMethod.objects.count())
        self.assertEquals(2, GeoCodeMethod.everything.count())


class TestFacilityCoordinatesModel(BaseTestCase):

    def setUp(self):
        # Linked to geographic units ( county, ward, constituency) that
        # do not have boundaries; intended to test validation
        self.test_fac = mommy.make_recipe(
            'mfl_gis.tests.facility_recipe',
            ward=mommy.make_recipe('mfl_gis.tests.ward_recipe')
        )
        self.test_ward = self.test_fac.ward
        self.test_constituency = self.test_ward.constituency
        self.test_county = self.test_constituency.county
        self.test_coords = mommy.prepare_recipe(
            'mfl_gis.tests.facility_coordinates_recipe',
            facility=self.test_fac
        )

    def test_save(self):
        facility_gps = mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        self.assertEquals(1, FacilityCoordinates.objects.count())
        self.assertEquals(
            facility_gps, facility_gps.facility.coordinates)

    def test_simplify_coordinates(self):
        facility_gps = mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        self.assertEquals(1, FacilityCoordinates.objects.count())
        self.assertIsInstance(facility_gps.simplify_coordinates, dict)

    def test_features_json(self):
        facility_gps = mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        self.assertEquals(1, FacilityCoordinates.objects.count())
        self.assertIsInstance(facility_gps.json_features, dict)

    def test_validate_long_and_lat_within_kenya_invalid(self):
        """The Kampala Serena - 0.319590, 32.586484; definitely not in Kenya"""
        with self.assertRaises(ValidationError):
            mommy.make_recipe(
                'mfl_gis.tests.facility_coordinates_recipe',
                coordinates=Point(32.586484, 0.319590)
            )

    def test_validate_long_and_lat_within_county_invalid(self):
        """Thomson Falls - 0.044444, 36.370416 - is in Kenya but not Nairobi"""
        with self.assertRaises(ValidationError):
            mommy.make_recipe(
                'mfl_gis.tests.facility_coordinates_recipe',
                coordinates=Point(36.370416, 0.044444)
            )

    def test_validate_long_and_lat_within_constituency_invalid(self):
        """Taj Mall (-1.323139, 36.898769) is in Nrb but not Dagoretti North"""
        with self.assertRaises(ValidationError):
            mommy.make_recipe(
                'mfl_gis.tests.facility_coordinates_recipe',
                coordinates=Point(36.898769, -1.323139)
            )

    def test_validate_long_and_lat_within_ward_invalid(self):
        """Kenya High (-1.275611, 36.780612) - is just outside Kilimani ward"""
        with self.assertRaises(ValidationError):
            mommy.make_recipe(
                'mfl_gis.tests.facility_coordinates_recipe',
                coordinates=Point(36.780612, -1.275611)
            )

    def test_validate_longitude_and_latitude_no_country_boundaries(self):
        with self.assertRaises(ValidationError) as c:
            self.test_coords.validate_long_and_lat_within_kenya()

        self.assertTrue(
            'Setup error: Kenyan boundaries not loaded'
            in c.exception.detail
        )

    def test_validate_longitude_and_latitude_no_county_boundaries(self):
        with self.assertRaises(ValidationError) as c:
            self.test_coords.validate_long_and_lat_within_county(
                self.test_county)

        self.assertIn(
            str(self.test_county),
            c.exception.detail["coordinates"][0]
        )

    def test_validate_longitude_and_latitude_no_constituency_boundaries(self):
        with self.assertRaises(ValidationError) as c:
            self.test_coords.validate_long_and_lat_within_constituency(
                self.test_constituency
            )

        self.assertIn(
            str(self.test_constituency),
            c.exception.detail["coordinates"][0]
        )

    def test_validate_longitude_and_latitude_no_ward_boundaries(self):
        self.test_coords.validate_long_and_lat_within_ward(self.test_ward)
        # Because some wards have no boundaries, we choose to let this pass
