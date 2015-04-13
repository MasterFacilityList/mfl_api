from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from model_mommy import mommy

from ..models import (
    Contact, County, Ward, Constituency, ContactType, PhysicalAddress)


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
            "name": "WAJIR"
        }
        county_data = self.inject_audit_fields(county_data)
        county = County.objects.create(**county_data)
        self.assertEquals(1, County.objects.count())
        self.assertIsNotNone(county.code)

    def test_unicode(self):
        county_name = "Texas"
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name=county_name, code='some code')
        self.assertEquals(county_name, county.__unicode__())

    def test_county_code_seq(self):
        # make code None so that model mommy does not supply it
        county = mommy.make(County, code=None)
        county_2 = mommy.make(County, code=None)
        county_2_code = int(county.code) + 1
        self.assertEquals(county_2_code, county_2.code)


class TestConstituencyModel(BaseTestCase):
    def setUp(self):
        super(TestConstituencyModel, self).setUp()
        self.county = County.objects.create(
            updated_by=self.user, created_by=self.user,
            name='county')

    def test_save_constituency(self):
        constituency_data = {
            "name": "KAPSA",
            "county": self.county

        }
        constituency_data = self.inject_audit_fields(constituency_data)
        constituency = Constituency.objects.create(**constituency_data)
        self.assertEquals(1, Constituency.objects.count())
        self.assertIsNotNone(constituency.code)

    def test_unicode(self):
        const = Constituency.objects.create(
            created_by=self.user, updated_by=self.user,
            name="jina", code='some code', county=self.county)
        self.assertEquals("jina", const.__unicode__())

    def test_constituency_code_sequence(self):
        constituency_1 = mommy.make(Constituency, code=None)
        constituency_2 = mommy.make(Constituency, code=None)
        constituency_2_code = int(constituency_1.code) + 1
        self.assertEquals(constituency_2_code, int(constituency_2.code))


class TestWardModel(BaseTestCase):
    def setUp(self):
        super(TestWardModel, self).setUp()
        county = mommy.make(County)
        self.constituency = Constituency.objects.create(
            created_by=self.user, updated_by=self.user,
            name='constituency', county=county)

    def test_save_ward(self):
        data = {
            "name": "KAPSA",
            "constituency": self.constituency
        }
        data = self.inject_audit_fields(data)
        ward = Ward.objects.create(**data)
        self.assertEquals(1, Ward.objects.count())
        self.assertIsNotNone(ward.code)

    def test_unicode(self):
        const = Ward.objects.create(
            updated_by=self.user, created_by=self.user,
            name="jina", constituency=self.constituency)
        self.assertEquals("jina", const.__unicode__())

    def test_sub_county_code_seq(self):
        sub_county_1 = mommy.make(Ward, code=None)
        sub_county_2 = mommy.make(Ward, code=None)
        sub_county_2_code = int(sub_county_1.code) + 1
        self.assertEquals(sub_county_2_code, int(sub_county_2.code))


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
