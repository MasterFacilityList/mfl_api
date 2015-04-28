from django.utils import timezone
from model_mommy import mommy

from common.tests.test_models import BaseTestCase
from facilities.models import Facility

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
        facility = mommy.make(Facility, name="Nairobi Hospital")
        method = mommy.make(GeoCodeMethod)
        source = mommy.make(GeoCodeSource)
        data = {
            "facility": facility,
            "latitude": "78.99",
            "longitude": "67.54",
            "method": method,
            "source": source,
            "collection_date": timezone.now()
        }
        data = self.inject_audit_fields(data)
        facility_gps = FacilityCoordinates.objects.create(**data)
        self.assertEquals(1, FacilityCoordinates.objects.count())

        # test unicode
        self.assertEquals("Nairobi Hospital", facility_gps.__unicode__())

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
