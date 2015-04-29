from model_mommy import mommy
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from common.tests.test_models import BaseTestCase

from ..models import GeoCodeSource, GeoCodeMethod, FacilityCoordinates


class TestGeoCodeSourceModel(BaseTestCase):
    def test_save(self):
        data = {
            "name": "Kenya Medical Research Institute",
            "description": "",
            "abbreviation": "KEMRI"
        }
        data = self.inject_audit_fields(data)
        source = GeoCodeSource.objects.create(**data)
        self.assertEquals(1, GeoCodeSource.objects.count())

        # test unicode
        self.assertEquals(
            "Kenya Medical Research Institute",
            source.__unicode__())


class TesGeoCodeMethodModel(BaseTestCase):
    def test_save(self):
        data = {
            "name": "Taken with GPS device",
            "description": "GPS device was used to get the geo codes"
        }
        data = self.inject_audit_fields(data)
        method = GeoCodeMethod.objects.create(**data)
        self.assertEquals(1, GeoCodeMethod.objects.count())

        # test unicode
        self.assertEquals("Taken with GPS device", method.__unicode__())


class TestFacilityCoordinatesModel(BaseTestCase):
    def test_save(self):
        facility_gps = mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe'
        )
        self.assertEquals(1, FacilityCoordinates.objects.count())

        # test unicode
        self.assertEquals(
            facility_gps.facility.name, facility_gps.__unicode__())

    def test_validate_longitude_and_latitude_within_kenya_invalid(self):
        """The Kampala Serena - 0.319590, 32.586484; definitely not in Kenya"""
        with self.assertRaises(ValidationError):
            mommy.make_recipe(
                'mfl_gis.tests.facility_coordinates_recipe',
                coordinates=Point(32.586484, 0.319590)
            )

    def test_validate_longitude_and_latitude_within_county_invalid(self):
        """Thomson Falls - 0.044444, 36.370416 - is in Kenya but not Nairobi"""
        with self.assertRaises(ValidationError):
            mommy.make_recipe(
                'mfl_gis.tests.facility_coordinates_recipe',
                coordinates=Point(36.370416, 0.044444)
            )

    def test_validate_longitude_and_latitude_within_constituency_invalid(self):
        """Taj Mall (-1.323139, 36.898769) is in Nrb but not Dagoretti North"""
        with self.assertRaises(ValidationError):
            mommy.make_recipe(
                'mfl_gis.tests.facility_coordinates_recipe',
                coordinates=Point(36.898769, -1.323139)
            )

    def test_validate_longitude_and_latitude_within_ward_invalid(self):
        """SIL - -1.300470, 36.791655 - is just outside Kilimani ward"""
        with self.assertRaises(ValidationError):
            mommy.make_recipe(
                'mfl_gis.tests.facility_coordinates_recipe',
                coordinates=Point(36.791655, -1.300470)
            )
