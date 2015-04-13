from datetime import timedelta, datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from model_mommy import mommy


from ..models import (
    Contact, County, SubCounty, Constituency,
    ContactType, PhysicalAddress, UserCounties)
from ..models import get_default_system_user_id


class AbstractBaseModelTest(TestCase):

    def setUp(self):
        self.leo = timezone.now()
        self.jana = timezone.now() - timedelta(days=1)
        self.juzi = timezone.now() - timedelta(days=2)
        self.user_1 = mommy.make(settings.AUTH_USER_MODEL)
        self.user_2 = mommy.make(settings.AUTH_USER_MODEL)

    def test_validate_updated_date_greater_than_created(self):
        fake = ContactType(created=self.leo, updated=self.jana)

        with self.assertRaises(ValidationError) as ve:
            fake.validate_updated_date_greater_than_created()
        self.assertTrue(
            'The updated date cannot be less than the created date'
            in ve.exception.messages)

    def test_preserve_created_and_created_by(self):
        # Create  a new instance
        fake = mommy.make(ContactType, created=self.jana, updated=self.leo,
                          created_by=self.user_1, updated_by=self.user_1)
        # Switch the create
        fake.created = self.juzi
        fake.save()

        self.assertEqual(self.jana, fake.created)

        # Switch created_by
        fake.created_by = self.user_2
        fake.updated_by = self.user_2
        fake.save()

        self.assertEqual(self.user_1.id, fake.created_by.id)
        self.assertEqual(self.user_2.id, fake.updated_by.id)

    def test_delete_override(self):
        bp_type = mommy.make(ContactType, created=timezone.now(),
                             updated=timezone.now())
        bp_type.delete()
        with self.assertRaises(ContactType.DoesNotExist):
            self.assertTrue(ContactType.objects.get(
                pk=bp_type.id))

        assert ContactType.everything.get(pk=bp_type.id)

    def test_timezone(self):
        naive_datetime = datetime.now()
        instance = mommy.make(ContactType)
        instance.updated = naive_datetime
        with self.assertRaises(ValidationError):
            instance.save()

        naive_after_object_is_saved = datetime.now()
        instance.updated = naive_after_object_is_saved
        instance.save()
        self.assertTrue(timezone.is_aware(instance.updated))

        # Test that we don't need to make created timezone aware
        # It is already tizezone aware
        self.assertTrue(timezone.is_aware(instance.created))
        created_naive_datetime = datetime.now()
        instance.create = created_naive_datetime  # This should not even update
        instance.save()
        self.assertTrue(timezone.is_aware(instance.created))


class BaseTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.get(pk=get_default_system_user_id)
        super(BaseTestCase, self).setUp()

    def inject_audit_fields(self, data):
        data["created_by"] = self.user
        data["updated_by"] = self.user
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
        Contact.objects.create(
            pk='1a049a8a-6e1f-4427-9098-a779cf9f63fa',
            contact='375818195',
            contact_type=contact_type)
        self.assertEquals(1, Contact.objects.count())


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
            name=county_name, code=234)
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
            name="jina", code=687, county=self.county)
        self.assertEquals("jina", const.__unicode__())

    def test_constituency_code_sequence(self):
        constituency_1 = mommy.make(Constituency, code=None)
        constituency_2 = mommy.make(Constituency, code=None)
        constituency_2_code = int(constituency_1.code) + 1
        self.assertEquals(constituency_2_code, int(constituency_2.code))


class TestSubCountyModel(BaseTestCase):
    def setUp(self):
        super(TestSubCountyModel, self).setUp()
        self.county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county')

    def test_save_sub_county(self):
        data = {
            "name": "KAPSA",
            "county": self.county
        }
        data = self.inject_audit_fields(data)
        sub_county = SubCounty.objects.create(**data)
        self.assertEquals(1, SubCounty.objects.count())
        self.assertIsNotNone(sub_county.code)

    def test_unicode(self):
        const = SubCounty.objects.create(
            updated_by=self.user, created_by=self.user,
            name="jina", code=879, county=self.county)
        self.assertEquals("jina", const.__unicode__())

    def test_sub_county_code_seq(self):
        sub_county_1 = mommy.make(SubCounty, code=None)
        sub_county_2 = mommy.make(SubCounty, code=None)
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


class TestUserCountiesModel(BaseTestCase):
    def test_save(self):
        user = mommy.make(get_user_model())
        county = mommy.make(County)
        data = {
            "user": user,
            "county": county

        }
        user_county = UserCounties.objects.create(**data)
        self.assertEquals(1, UserCounties.objects.count())
        expected_unicode = "{}: {}".format(user.email, county.name)
        self.assertEquals(expected_unicode, user_county.__unicode__())

    def test_user_is_only_active_in_one_count(self):
        user = mommy.make(get_user_model())
        county_1 = mommy.make(County)
        county_2 = mommy.make(County)
        UserCounties.objects.create(
            user=user,
            county=county_1
        )
        with self.assertRaises(ValidationError):
            UserCounties.objects.create(
                user=user,
                county=county_2
            )
