from model_moomy import mommy

from common.tests.test_models import BaseTestCase
from common.models import Contact

from ..models import (
    OwnerType, Owner, JobTitle, OfficerIncharge,
    OfficerIchargeContact, ServiceCategory,
    Service, FacilityStatus, FacilityType,
    RegulatingBody, RegulationStatus, Facility,
    FacilityRegulationStatus, GeoCodeSource,
    GeoCodeMethod, FacilityGPS,
    FacilityService, FacilityContact

)


class TetOwnwerTypes(BaseTestCase):
    def test_save(self):
        data = {
            "name": "FBO",
            "description": "The the faith based organisation owners"
        }
        data = self.inject_audit_fields(data)
        owner_type = OwnerType.objects.create(**data)
        self.assertEquals(1, OwnerType.objects.count())

        # test unicode
        self.assertEquals("FBO", owner_type.__unicode__())


class TestOwnerModel(BaseTestCase):
    def test_save(self):
        owner_type = mommy.make(OwnerType, name="FBO")
        data = {
            "owner_type": owner_type,
            "name": "CHAK",
            "description": "this is some description",
            "code": "HJUAFHJA",
            "abbreviation": "CHAK"
        }
        data = self.inject_audit_fields(data)
        owner = Owner.objects.create(**data)
        self.assertEquals(1, Owner.objects.count())

        # test unicode
        self.assertEquals("CHAK", owner.__unicode__())


class TestJobTitleModel(BaseTestCase):
    def test_save(self):
        data = {
            "name": "Nurse officer incharge",
            "description": "some good description"
        }
        data = self.inject_audit_fields(data)
        jt = JobTitle.objects.create(**data)
        self.assertEquals(1, JobTitle.objects.count())

        # test unicode
        self.assertEquals("Nurse officer incharge", jt.__unicode__())


class TestOfficerIncharge(BaseTestCase):
    def test_save(self):
        jt = mommy.make(JobTitle)
        data = {
            "name": "Kimani Maruge",
            "registration_number": "78736790",
            "job_title": jt
        }
        data = self.inject_audit_fields(data)
        officer = OfficerIncharge.objects.create(**data)
        self.assertEquals(1, OfficerIncharge.objects.count())

        # test unicode
        self.assertEquals("Kimani Maruge", officer.__unicode__())


class TestOfficerInchargeContactModel(BaseTestCase):
    def test_save(self):
        officer = mommy.make(OfficerIncharge)
        contact = mommy.make(Contact)
        data = {
            "officer": officer,
            "contact": contact
        }
        data = self.inject_audit_fields(**data)
        contact = OfficerIchargeContact.objects.create(**data)
        self.assertEquals(1, OfficerIchargeContact.objects.count())

        # test unicode
        expected = "{}:{}".format(officer.name, contact.con)
        self.assertEquals(expected, contact.__unicode__())


class TestServiceCategory(BaseTestCase):
    pass


class TestServiceModel(BaseTestCase):
    pass
