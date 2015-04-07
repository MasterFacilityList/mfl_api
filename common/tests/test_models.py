from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import (
    Contact, County, SubCounty, Constituency)


class BaseTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@gmail.com", "test", "test", "test")
        super(BaseTestCase, self).setUp()

    def inject_audit_fields(self, data):
        data["created_by"] = self.user
        data["updated_by"] = self.user
        data["created"] = timezone.now()
        data["updated"] = timezone.now()
        return data


class TestContactModel(BaseTestCase):
    def test_save_contact(self):
        contact_data = {
            "contact": "test@mail.com",
            "contact_type": "EMAIL"
        }
        contact_data = self.inject_audit_fields(contact_data)
        Contact.objects.create(**contact_data)
        self.assertEquals(1, Contact.objects.count())

    def test_unicode(self):
        contact_data = {
            "contact": "0756832902",
            "contact_type": "PHONE"
        }
        contact_data = self.inject_audit_fields(contact_data)
        obj = Contact.objects.create(**contact_data)
        self.assertEquals("1", obj.__unicode__())


class TestCountyModel(BaseTestCase):

    def test_save_county(self):
        county_data = {
            "name": "WAJIR",
            "code": "WA1"
        }
        county_data = self.inject_audit_fields(county_data)
        County.objects.create(**county_data)
        self.assertEquals(1, County.objects.count())

    def test_unicode(self):
        county_name = "Texas"
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name=county_name, code='some code')
        self.assertEquals(county_name, county.__unicode__())


class TestConstituencyModel(BaseTestCase):
    def setUp(self):
        super(TestConstituencyModel, self).setUp()
        self.county = County.objects.create(
            updated_by=self.user, created_by=self.user,
            name='county', code='county code')

    def test_save_constituency(self):
        constituency_data = {
            "name": "KAPSA",
            "code": "1125",
            "county": self.county

        }
        constituency_data = self.inject_audit_fields(constituency_data)
        Constituency.objects.create(**constituency_data)
        self.assertEquals(1, Constituency.objects.count())

    def test_unicode(self):
        const = Constituency.objects.create(
            created_by=self.user, updated_by=self.user,
            name="jina", code='some code', county=self.county)
        self.assertEquals("jina", const.__unicode__())


class TestSubCountyModel(BaseTestCase):
    def setUp(self):
        super(TestSubCountyModel, self).setUp()
        self.county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county', code='county code')

    def test_save_constituency(self):
        data = {
            "name": "KAPSA",
            "code": "1125",
            "county": self.county
        }
        data = self.inject_audit_fields(data)
        SubCounty.objects.create(**data)
        self.assertEquals(1, SubCounty.objects.count())

    def test_unicode(self):
        const = SubCounty.objects.create(
            updated_by=self.user, created_by=self.user,
            name="jina", code='some code', county=self.county)
        self.assertEquals("jina", const.__unicode__())
