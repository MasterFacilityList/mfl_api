from datetime import timedelta, datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from model_mommy import mommy


from ..models import (
    Contact,
    County,
    Ward,
    Constituency,
    Town,
    ContactType,
    PhysicalAddress,
    UserCounty,
    UserContact,
    UserConstituency,
    SubCounty,
    ErrorQueue
)
from facilities.models import RegulationStatus


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
            in ve.exception.detail)

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
        self.user = get_user_model().objects.create_superuser(
            email='tester1@ehealth.or.ke',
            first_name='Test',
            employee_number='2124124124',
            password='mtihani124',
            is_national=True
        )
        self.default_regulation_status = mommy.make(
            RegulationStatus, name="Pending Regulation", is_default=True)

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

    def test_county_code_seq(self):
        # make code None so that model mommy does not supply it
        county = mommy.make(County, code=None)
        county_2 = mommy.make(County, code=None)
        county_2_code = int(county.code) + 1
        self.assertEquals(county_2_code, county_2.code)

    def test_lookup_facility_coordinates(self):
        county = mommy.make(County)
        self.assertEqual(
            county.facility_coordinates,
            []
        )

    def test_county_bound(self):
        county = mommy.make(County)
        self.assertEqual(
            county.county_bound,
            {}
        )


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

    def test_constituency_code_sequence(self):
        constituency_1 = mommy.make(Constituency, code=None)
        constituency_2 = mommy.make(Constituency, code=None)
        constituency_2_code = int(constituency_1.code) + 1
        self.assertEquals(constituency_2_code, int(constituency_2.code))

    def test_consituency_bound(self):
        const = mommy.make(Constituency)
        self.assertEqual(
            const.constituency_bound,
            {}
        )


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

    def test_sub_county_code_seq(self):
        sub_county_1 = mommy.make(Ward, code=None)
        sub_county_2 = mommy.make(Ward, code=None)
        sub_county_2_code = int(sub_county_1.code) + 1
        self.assertEquals(sub_county_2_code, int(sub_county_2.code))

    def test_get_county(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        self.assertEquals(county, ward.county)

    def test_ward_county(self):
        # test that the county for the sub-county and the constituency
        # are the same
        sub_county = mommy.make(SubCounty)
        const = mommy.make(Constituency)
        with self.assertRaises(ValidationError):
            mommy.make(Ward, constituency=const, sub_county=sub_county)


class TestPhysicalAddress(BaseTestCase):

    def test_save(self):
        data = {
            "town": mommy.make(Town, name="Nairobi"),
            "nearest_landmark": "",
            "plot_number": "35135"
        }
        data = self.inject_audit_fields(data)
        PhysicalAddress.objects.create(**data)
        self.assertEquals(1, PhysicalAddress.objects.count())


class TestUserCountyModel(BaseTestCase):

    def test_save(self):
        user = mommy.make(get_user_model())
        county = mommy.make(County)
        data = {
            "user": user,
            "county": county
        }
        UserCounty.objects.create(**data)
        self.assertEquals(1, UserCounty.objects.count())

    def test_user_linked_to_a_county_once(self):
        user = mommy.make(get_user_model())
        county = mommy.make(County)
        # First time should save with no issue
        user_county_rec = mommy.make(UserCounty, user=user, county=county)
        # Deactivating the record should have no incident
        user_county_rec.active = False
        user_county_rec.save()
        self.assertFalse(UserCounty.objects.get(user=user).active)

        user_county_rec.active = True
        user_county_rec.save()
        self.assertTrue(UserCounty.objects.get(user=user).active)


class TestUserContactModel(BaseTestCase):

    def test_save(self):
        user = mommy.make(get_user_model())
        contact = mommy.make(Contact)
        data = {
            "user": user,
            "contact": contact
        }
        data = self.inject_audit_fields(data)
        UserContact.objects.create(**data)
        self.assertEquals(1, UserContact.objects.count())

    def test_user_and_contact_unique(self):
        contact = mommy.make(Contact)
        user = mommy.make(get_user_model())
        mommy.make(UserContact, user=user, contact=contact)
        with self.assertRaises(ValidationError):
            mommy.make(UserContact, user=user, contact=contact)

    def test_user_contact_deletion(self):
        contact = mommy.make(Contact)
        user = mommy.make(get_user_model())
        user_contact = mommy.make(UserContact, user=user, contact=contact)
        self.assertEquals(1, UserContact.objects.filter(user=user).count())
        user_contact.delete()
        self.assertEquals(0, UserContact.objects.filter(user=user).count())


class TestUserConstituencyModel(BaseTestCase):

    def test_save(self):
        user = mommy.make(get_user_model())
        county = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        creator_user = mommy.make(get_user_model())
        mommy.make(
            UserCounty, county=county, user=creator_user)
        mommy.make(
            UserConstituency, constituency=const, user=user,
            created_by=creator_user)
        self.assertEquals(1, UserConstituency.objects.count())

    def test_validator_constituency_in_creators_county(self):
        county = mommy.make(County)
        county_2 = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        const_2 = mommy.make(Constituency, county=county_2)
        user = mommy.make(get_user_model())
        user_2 = mommy.make(get_user_model())
        creator_user = mommy.make(get_user_model())
        mommy.make(UserCounty, county=county, user=creator_user)

        # should save without incidence
        mommy.make(
            UserConstituency, user=user, constituency=const,
            created_by=creator_user
        )
        self.assertEquals(1, UserConstituency.objects.count())
        # should raise validation error'
        with self.assertRaises(ValidationError):
            mommy.make(UserConstituency, user=user_2, constituency=const_2)
        # test user constituencies
        self.assertEquals(const, user.constituency)

    def test_user_created_is_in_the_creators_sub_county(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        constituency_2 = mommy.make(Constituency)
        user = mommy.make(get_user_model())
        user_2 = mommy.make(get_user_model())
        user_3 = mommy.make(get_user_model())
        mommy.make(UserCounty, county=county, user=user)
        mommy.make(
            UserConstituency, constituency=constituency,
            user=user_2, created_by=user, updated_by=user)

        # the user being created and the creating user are not in
        # the same constituency
        with self.assertRaises(ValidationError):
            mommy.make(
                UserConstituency, constituency=constituency_2,
                user=user_3, created_by=user_2, updated_by=user_2)

    def test_user_linked_to_a_constituency_once(self):
        user = mommy.make(get_user_model())
        county = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        creator_user = mommy.make(get_user_model())
        mommy.make(UserCounty, user=creator_user, county=county)
        # First time should save with no issue
        user_const_rec = mommy.make(
            UserConstituency, user=user, constituency=const,
            created_by=creator_user, updated_by=creator_user)
        # Deactivating the record should have no incident
        user_const_rec.active = False
        user_const_rec.save()
        self.assertFalse(UserConstituency.objects.get(user=user).active)

        user_const_rec.active = True
        user_const_rec.save()
        self.assertTrue(UserConstituency.objects.get(user=user).active)


class TestSubCounty(TestCase):

    def test_save(self):
        mommy.make(SubCounty)
        self.assertEquals(1, SubCounty.objects.count())


class TestErrorQueue(TestCase):
    def test_save(self):
        mommy.make(ErrorQueue)
        self.assertEquals(1, ErrorQueue.objects.count())

    def test_representation(self):
        error = mommy.make(
            ErrorQueue,
            object_pk='1',
            app_label='users',
            model_name='MflUser')
        string_rep = "1 - users - MflUser"
        self.assertEquals(string_rep, error.__str__())
