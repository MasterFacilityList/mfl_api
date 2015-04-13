from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from model_mommy import mommy

from ..models import (
    Contact, County, SubCounty, Constituency, ContactType, PhysicalAddress)


class BaseTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            "test@gmail.com", "test", "test", "test")
        super(BaseTestCase, self).setUp()

    def inject_audit_fields(self, data):
        data["created_by"] = self.user.id
        data["updated_by"] = self.user.id
        data["created"] = timezone.now()
        data["updated"] = timezone.now()
        return data


class TestContactModel(BaseTestCase):
    def test_save_contact(self):
        contact_type = mommy.make(ContactType, name='EMAIL')
        contact_data = {
            "contact": "test@mail.com",
            "contact_type": contact_type
        }
        contact_data = self.inject_audit_fields(contact_data)
        Contact.objects.create(**contact_data)
        self.assertEquals(1, Contact.objects.count())

    def test_unicode(self):
        contact_type = mommy.make(ContactType, name='PHONE')
        contact_data = {
            "contact": "0756832902",
            "contact_type": contact_type
        }
        contact_data = self.inject_audit_fields(contact_data)
        obj = Contact.objects.create(**contact_data)
        self.assertEquals("PHONE::0756832902", obj.__unicode__())

    def test_save_model_with_id(self):
        contact_type = mommy.make(ContactType)
        contact = Contact.objects.create(
            pk='1a049a8a-6e1f-4427-9098-a779cf9f63fa',
            contact='375818195',
            contact_type=contact_type)
        self.assertEquals(1, Contact.objects.count())

        # try recreate the model again to confirm that created
        # by and created are preserved
        contact_refetched = Contact.objects.get(
            id='1a049a8a-6e1f-4427-9098-a779cf9f63fa')
        contact_refetched.created = "2015-04-10T08:41:05.169411Z"
        contact_refetched.save()
        self.assertNotEquals(
            contact_refetched.created, "2015-04-10T08:41:05.169411Z")
        self.assertEquals(contact.created, contact_refetched.created)

        contact_refetched.created_by = "1a049a8a-6e1f-4427-9098-a779cf9f63fa"
        contact_refetched.save()
        self.assertNotEquals(
            contact_refetched.created_by,
            "1a049a8a-6e1f-4427-9098-a779cf9f63fa")
        self.assertEquals(contact.created_by, contact_refetched.created_by)


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


class TestContactType(BaseTestCase):
    def test_unicode_(self):
        ct = mommy.make(ContactType, name='EMAIL')
        self.assertEquals('EMAIL', ct.__unicode__())


class TestPhysicalAddress(BaseTestCase):
    def test_save(self):
        data = {
            "town": "Nairobi",
            "postal_code": "00200",
            "address": "356",
            "nearest_landmark": "",
            "plot_number": "35135"
        }
        data = self.inject_audit_fields(data)
        phy = PhysicalAddress.objects.create(**data)
        self.assertEquals(1, PhysicalAddress.objects.count())
        self.assertEquals("00200: 356", phy.__unicode__())
