from model_mommy import mommy
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

    def test_validate_longitude_and_latitude_within_kenya_valid(self):
        pass

    def test_validate_longitude_and_latitude_within_kenya_invalid(self):
        pass

    def test_validate_longitude_and_latitude_within_county_valid(self):
        pass

    def test_validate_longitude_and_latitude_within_county_invalid(self):
        pass

    def test_validate_longitude_and_latitude_within_constituency_valid(self):
        pass

    def test_validate_longitude_and_latitude_within_constituency_invalid(self):
        pass

    def test_validate_longitude_and_latitude_within_ward_valid(self):
        pass

    def test_validate_longitude_and_latitude_within_ward_invalid(self):
        pass
