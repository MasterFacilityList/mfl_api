import json
import uuid

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from model_mommy import mommy

from ..models import (
    County,
    Contact,
    ContactType,
    Constituency,
    Ward,
    UserContact,
    UserConstituency,
    UserCounty,
    Town,
    SubCounty,
    ErrorQueue,
    UserSubCounty
)
from ..serializers import (
    ContactSerializer,
    WardSerializer,
    WardDetailSerializer,
    CountySerializer,
    CountyDetailSerializer,
    ConstituencySerializer,
    ConstituencyDetailSerializer,
    UserContactSerializer,
    UserConstituencySerializer
)


def default(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)


class LoginMixin(object):

    def setUp(self):
        password = 'mtihani124'
        self.user = get_user_model().objects.create_superuser(
            email='tester@ehealth.or.ke',
            first_name='Test',
            employee_number='124144124124',
            password=password,
            is_national=True
        )
        self.client.login(email='tester@ehealth.or.ke', password=password)
        self.maxDiff = None
        mommy.make(Group, name='Facility Viewing Group')
        super(LoginMixin, self).setUp()


class TestViewCounties(LoginMixin, APITestCase):

    def setUp(self):
        super(TestViewCounties, self).setUp()
        self.url = reverse('api:common:counties_list')

    def test_post(self):
        data = {
            "name": "Kiambu",
            "code": 22
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)

    def test_list_counties(self):
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        county_2 = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 2', code='101')
        url = reverse('api:common:counties_list')
        response = self.client.get(url)
        expected_data = {
            "results": [
                CountySerializer(
                    county_2,
                    context={
                        'request': response.request
                    }
                ).data,
                CountySerializer(
                    county,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(
            json.loads(json.dumps(expected_data['results'], default=default)),
            json.loads(json.dumps(response.data['results'], default=default)))
        self.assertEquals(200, response.status_code)

    def test_retrieve_single_county(self):
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        url = reverse('api:common:counties_list')
        url += "{}/".format(county.id)
        response = self.client.get(url)
        expected_data = CountyDetailSerializer(
            county,
            context={
                'request': response.request
            }
        ).data
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
        self.assertEquals(200, response.status_code)


class TestViewConstituencies(LoginMixin, APITestCase):

    def setUp(self):
        super(TestViewConstituencies, self).setUp()

    def test_list_constituencies(self):
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        constituency = Constituency.objects.create(
            created_by=self.user, updated_by=self.user, county=county,
            name='constituency 1',
            code='335')
        constituency_2 = Constituency.objects.create(
            created_by=self.user, updated_by=self.user, name='constituency 2',
            code='337', county=county)
        url = reverse('api:common:constituencies_list')
        response = self.client.get(url)
        expected_data = {
            "results": [
                ConstituencySerializer(
                    constituency_2, context={
                        'request': response.request
                    }).data,
                ConstituencySerializer(
                    constituency,
                    context={
                        'request': response.request
                    }).data
            ]
        }
        # some weird ordering the dumps string
        # json.loads the dumped string to check equality of dicts
        self.assertEquals(
            json.loads(json.dumps(expected_data['results'], default=default)),
            json.loads(json.dumps(response.data['results'], default=default)))
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('count'))

    def test_retrive_single_constituency(self):
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        constituency = Constituency.objects.create(
            created_by=self.user, updated_by=self.user, county=county,
            name='constituency 1',
            code='335')
        url = reverse('api:common:constituencies_list')
        url += "{}/".format(constituency.id)
        response = self.client.get(url)
        expected_data = ConstituencyDetailSerializer(
            constituency,
            context={
                'request': response.request
            }).data
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
        self.assertEquals(200, response.status_code)


class TestViewWards(LoginMixin, APITestCase):

    def setUp(self):
        super(TestViewWards, self).setUp()

    def test_list_wards(self):
        county = mommy.make(County)
        constituency = Constituency.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100', county=county)
        ward_1 = Ward.objects.create(
            created_by=self.user, updated_by=self.user,
            constituency=constituency, name='ward 1',
            code='335')
        ward_2 = Ward.objects.create(
            created_by=self.user, updated_by=self.user, name='ward 2',
            code='337', constituency=constituency)
        url = reverse('api:common:wards_list')
        response = self.client.get(url)
        expected_data = {
            "results": [
                WardSerializer(
                    ward_2,
                    context={
                        'request': response.request
                    }).data,
                WardSerializer(
                    ward_1,
                    context={
                        'request': response.request
                    }).data
            ]
        }
        self.assertEquals(
            json.loads(json.dumps(expected_data['results'], default=default)),
            json.loads(json.dumps(response.data['results'], default=default)))
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('count'))

    def test_retrive_single_ward(self):

        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        constituency = mommy.make(Constituency, county=county)
        ward = Ward.objects.create(
            created_by=self.user, updated_by=self.user,
            constituency=constituency,
            name='sub county',
            code='335')
        url = reverse('api:common:wards_list')
        url += "{}/".format(ward.id)
        response = self.client.get(url)
        expected_data = WardDetailSerializer(
            ward,
            context={
                'request': response.request
            }).data
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
        self.assertEquals(200, response.status_code)


class TestContactView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestContactView, self).setUp()
        self.url = reverse("api:common:contacts_list")

    def test_get_contacts(self):
        contact_type = mommy.make(ContactType, name="EMAIL")
        contact_type_1 = mommy.make(ContactType, name="PHONE")
        contact = mommy.make(
            Contact,
            contact='test@gmail.com', contact_type=contact_type)
        contact_1 = mommy.make(
            Contact,
            contact='0784636499', contact_type=contact_type_1)

        response = self.client.get(self.url)
        expected_data = {
            "results": [
                ContactSerializer(
                    contact_1,
                    context={
                        'request': response.request
                    }
                ).data,
                ContactSerializer(
                    contact,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(
            json.loads(json.dumps(expected_data['results'], default=default)),
            json.loads(json.dumps(response.data['results'], default=default)))

    def test_post_created_by_not_supplied(self):
        # Special case, to test AbstractFieldsMixin
        contact_type = mommy.make(ContactType)
        data = {
            "contact": "072578980",
            "contact_type": str(contact_type.id)
        }
        response = self.client.post(self.url, data)

        self.assertEquals(201, response.status_code)
        self.assertEquals(1, Contact.objects.count())
        self.assertIn('id', json.dumps(response.data, default=default))
        self.assertIn('contact', json.dumps(response.data, default=default))
        self.assertIn(
            'contact_type', json.dumps(response.data, default=default))

    def test_post_created_by_supplied(self):
        # Special case, to test AbstractFieldsMixin
        contact_type = mommy.make(ContactType)
        data = {
            "contact": "072578980",
            "contact_type": str(contact_type.id),
            "created_by": str(self.user.id)
        }
        response = self.client.post(self.url, data)

        self.assertEquals(201, response.status_code)
        self.assertEquals(1, Contact.objects.count())
        self.assertIn('id', json.dumps(response.data, default=default))
        self.assertIn('contact', json.dumps(response.data, default=default))
        self.assertIn(
            'contact_type', json.dumps(response.data, default=default))

    def test_retrieve_contact(self):
        contact = mommy.make(Contact)
        url = self.url + "{}/".format(contact.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_filtering(self):
        pass


class TestContactTypeView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestContactTypeView, self).setUp()
        self.url = reverse("api:common:contact_types_list")

    def test_post_contact_types(self):
        data = {
            "created": "2015-04-10T08:41:05.169411Z",
            "updated": "2015-04-10T08:41:05.169411Z",
            "name": "EMAIL",
            "description": "This is an email contact typ"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertIn("id", response.data)
        self.assertIn("name", response.data)
        self.assertIn("description", response.data)

        #  run the other side of the default method

    def test_default_method(self):
        obj = uuid.uuid4()
        result = default(obj)
        self.assertIsInstance(result, str)
        obj_2 = ""
        result = default(obj_2)
        self.assertIsNone(result)


class TestTownView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestTownView, self).setUp()
        self.url = reverse("api:common:towns_list")

    def test_post_contact_types(self):
        data = {
            "name": "Kiamaiko Taon"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertIn("id", response.data)
        self.assertIn("name", response.data)
        self.assertEqual("Kiamaiko Taon", response.data['name'])


class TestAPIRootView(LoginMixin, APITestCase):

    def setUp(self):
        self.url = reverse('api:root_listing')
        cache.clear()
        super(TestAPIRootView, self).setUp()

    def test_api_and_metadata_root_view(self):
        """
        So, you've landed here, presumably after an exasperating test failure
        ( probably cursing under your breath ).

        There's a high chance that one of two things is wrong:

            * you have a concrete model in an app that is in
            `settings.LOCAL_APPS` that has no list & detail views and URLs OR
            * you violated the URL naming conventions (for the `name` param )

        What are these naming conventions, I hear you ask...

            * detail views -> 'api:<app_name>:<applicable_model_verbose_name>'
            * list views ->
                'api:<app_name>:<applicable_model_verbose_name_plural>'

        If Django gives your model a funny `verbose_name_plural` ( because
        it ends with a 'y' or 's' and silly Django just appends an 's' ),
        set a better `verbose_name_plural` in the model's `Meta`. Once in
        a while, Django will also pick a `verbose_name` that is not to your
        liking; you can override that too.

        PS: Yes, this is a bitch. It is also a good discipline master.
        And - it is stupid, only assembling metadata for CRUD views.
        """
        # It is not the size of the dog in the fight that matters...
        # This is one sensitive bitch of a test!
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)

        # Test that the root redirects here
        redirect_response = self.client.get(
            reverse('root_redirect'), follow=True)
        self.assertEquals(200, redirect_response.status_code)


class TestUserContactView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestUserContactView, self).setUp()
        self.url = reverse("api:common:user_contacts_list")

    def test_save(self):
        user_contact_1 = mommy.make(UserContact)
        user_contact_2 = mommy.make(UserContact)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                UserContactSerializer(
                    user_contact_2,
                    context={
                        'request': response.request
                    }
                ).data,
                UserContactSerializer(
                    user_contact_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]

        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data['results'], default=default)),
            json.loads(json.dumps(response.data['results'], default=default)))

    def test_retrieve_user_contact(self):
        user_contact = mommy.make(UserContact)
        url = self.url + "{}/".format(user_contact.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        expected_data = UserContactSerializer(
            user_contact,
            context={
                'request': response.request
            }).data
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))


class TestFilteringSummariesView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestFilteringSummariesView, self).setUp()
        self.url = reverse('api:common:filtering_summaries')

    def test_get_summaries(self):
        mommy.make(County, name="muranga")
        ward = mommy.make(Ward, name='kizito')
        mommy.make(Constituency, name='kiambaa')
        response = self.client.get(self.url + '?fields=ward')
        self.assertEquals(200, response.status_code)
        self.assertTrue('ward' in response.data)
        self.assertEqual(response.data['ward'][0]['name'], ward.name)

    def test_get_summaries_no_fields_specified(self):
        mommy.make(County, name="muranga")
        mommy.make(Ward, name='kizito')
        mommy.make(Constituency, name='kiambaa')
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEqual(response.data, {})

    def test_get_summaries_some_fields_wrong(self):
        mommy.make(County, name="muranga")
        ward = mommy.make(Ward, name='kizito')
        mommy.make(Constituency, name='kiambaa')
        response = self.client.get(self.url + '?fields=ward,hakuna')
        self.assertEquals(200, response.status_code)
        self.assertTrue('ward' in response.data)
        self.assertEqual(response.data['ward'][0]['name'], ward.name)


class TestDeleting(LoginMixin, APITestCase):

    def setUp(self):
        self.url = reverse('api:common:counties_list')
        super(TestDeleting, self).setUp()

    def test_delete_county(self):
        county = mommy.make(County)
        url = self.url + '{}/'.format(county.id)
        response = self.client.delete(url)
        # assert status code due to cache time of 15 seconds
        self.assertEquals(200, response.status_code)
        # self.assertEquals("Not Found", response.data.get('detail'))

        with self.assertRaises(County.DoesNotExist):
            County.objects.get(id=county.id)

        self.assertEquals(1, County.everything.filter(id=county.id).count())


class TestSlimDetailViews(LoginMixin, APITestCase):

    def test_get_county_slim_detail_view(self):
        county = mommy.make(County)
        url = reverse('api:common:county_slim_detail', args=[str(county.id)])
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_consituency_slim_detail_view(self):
        const = mommy.make(Constituency)
        url = reverse(
            'api:common:constituency_slim_detail', args=[str(const.id)])
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_ward_slim_detail_view(self):
        ward = mommy.make(Ward)
        url = reverse('api:common:ward_slim_detail', args=[str(ward.id)])
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)


class TestUserConstituenciesView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestUserConstituenciesView, self).setUp()
        self.url = reverse("api:common:user_constituencies_list")

    def test_test_listing(self):
        user = mommy.make(get_user_model())
        county = mommy.make(County)
        mommy.make(UserCounty, user=user, county=county)
        const = mommy.make(Constituency, county=county)
        mommy.make(UserCounty, user=self.user, county=county)
        user_const_1 = mommy.make(
            UserConstituency, constituency=const, created_by=user)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        expected_data = {
            "results": [
                UserConstituencySerializer(
                    user_const_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(
            json.loads(json.dumps(expected_data['results'], default=default)),
            json.loads(json.dumps(response.data['results'], default=default)))

    def test_retrieve_single_user_constituency(self):
        user = mommy.make(get_user_model())
        user_2 = mommy.make(get_user_model())
        county = mommy.make(County)
        mommy.make(UserCounty, user=user, county=county)
        const = mommy.make(Constituency, county=county)
        user_const_1 = mommy.make(
            UserConstituency, constituency=const, created_by=user)
        mommy.make(
            UserConstituency, user=user_2, constituency=const,
            created_by=user)
        url = self.url + "{}/".format(user_const_1.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        expected_data = UserConstituencySerializer(
            user_const_1,
            context={
                'request': response.request
            }).data
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_posting(self):
        user = mommy.make(get_user_model())
        county = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        mommy.make(UserCounty, user=self.user, county=county, active=True)
        data = {
            "constituency": str(const.id),
            "user": str(user.id)
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, UserConstituency.objects.count())
        self.assertIn('id', json.loads(json.dumps(
            response.data, default=default)))


class TestFilteringAdminUnits(APITestCase):

    def setUp(self):
        self.county = mommy.make(County)
        self.constituency = mommy.make(Constituency, county=self.county)
        self.initial_user = mommy.make(get_user_model())
        mommy.make(UserCounty, user=self.initial_user, county=self.county)
        super(TestFilteringAdminUnits, self).setUp()

    def test_filter_wards_by_user_constituency(self):
        user = mommy.make(get_user_model())
        mommy.make(
            UserConstituency,
            user=user, created_by=self.initial_user,
            constituency=self.constituency,
            updated_by=self.initial_user)
        ward_1 = mommy.make(Ward, constituency=self.constituency)
        ward_2 = mommy.make(Ward, constituency=self.constituency)
        mommy.make(Ward)

        self.client.force_authenticate(user)
        url = reverse("api:common:wards_list")
        response = self.client.get(url)
        expected_data = [
            WardSerializer(
                ward_2,
                context={
                    'request': response.request
                }
            ).data,
            WardSerializer(
                ward_1,
                context={
                    'request': response.request
                }
            ).data]
        self.assertEquals(
            json.loads(
                json.dumps(expected_data, default=default)),
            json.loads(
                json.dumps(
                    response.data.get("results"), default=default)
            )
        )

    def test_filter_consituencies_by_user_county(self):
        self.maxDiff = None
        user = mommy.make(get_user_model())
        mommy.make(
            UserCounty,
            user=user, created_by=self.initial_user,
            county=self.county,
            updated_by=self.initial_user)
        const_1 = mommy.make(Constituency, county=self.county)
        const_2 = mommy.make(Constituency, county=self.county)
        mommy.make(Constituency)

        self.client.force_authenticate(user)
        url = reverse("api:common:constituencies_list")
        response = self.client.get(url)
        expected_data = [
            ConstituencySerializer(
                const_2,
                context={
                    'request': response.request
                }
            ).data,
            ConstituencySerializer(
                const_1,
                context={
                    'request': response.request
                }
            ).data,
            ConstituencySerializer(
                self.constituency,
                context={
                    'request': response.request
                }
            ).data
        ]
        self.assertEquals(
            json.loads(
                json.dumps(expected_data, default=default)),
            json.loads(
                json.dumps(
                    response.data.get("results"), default=default)
            )
        )

    def test_national_user_sees_everything(self):
        self.maxDiff = None
        self.initial_user.is_national = True
        self.initial_user.save()

        self.client.force_authenticate(self.initial_user)

        # get constituencies
        url = reverse("api:common:constituencies_list")
        response = self.client.get(url)

        self.assertEquals(
            Constituency.objects.count(), len(response.data.get("results"))
        )

        # get wards
        url = reverse("api:common:wards_list")
        response = self.client.get(url)
        self.assertEquals(
            Ward.objects.count(), len(response.data.get("results"))
        )

    def test_national_user_sees_all_towns(self):
        county = mommy.make(County)
        user = mommy.make(get_user_model())
        user.is_national = True
        user.save()
        mommy.make(UserCounty, user=user, county=county)
        mommy.make(Town, name='The shire')
        mommy.make(Town, name='sparta')
        url = reverse("api:common:towns_list")
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, len(response.data.get("results")))

    def test_sub_county_user_sees_all_towns(self):
        county = mommy.make(County)
        user = mommy.make(get_user_model())
        user_2 = mommy.make(get_user_model())
        mommy.make(UserCounty, user=user, county=county)
        const = mommy.make(Constituency, county=county)
        mommy.make(
            UserConstituency, user=user_2,
            created_by=user, updated_by=user, constituency=const)
        mommy.make(Town, name='Rome')
        mommy.make(Town, name='Rivendell')
        url = reverse("api:common:towns_list")
        self.client.force_authenticate(user_2)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, len(response.data.get("results")))

    def test_county_user_sees_only_wards_in_county(self):
        user = mommy.make(get_user_model())
        mommy.make(
            UserCounty,
            user=user,
            county=self.county)
        ward_1 = mommy.make(Ward, constituency=self.constituency)
        ward_2 = mommy.make(Ward, constituency=self.constituency)
        mommy.make(Ward)

        self.client.force_authenticate(user)
        url = reverse("api:common:wards_list")
        response = self.client.get(url)
        expected_data = [
            WardSerializer(
                ward_2,
                context={
                    'request': response.request
                }
            ).data,
            WardSerializer(
                ward_1,
                context={
                    'request': response.request
                }
            ).data]
        self.assertEquals(
            json.loads(
                json.dumps(expected_data, default=default)),
            json.loads(
                json.dumps(
                    response.data.get("results"), default=default)
            )
        )


class TestSubCountyView(LoginMixin, APITestCase):

    def setUp(self):
        self.url = reverse("api:common:sub_counties_list")
        super(TestSubCountyView, self).setUp()

    def test_posting(self):
        county = mommy.make(County)
        data = {
            "name": "test subcounty",
            "county": county.id
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, SubCounty.objects.count())
        self.assertIn("id", response.data)

    def test_listing(self):
        mommy.make(SubCounty)
        mommy.make(SubCounty)
        mommy.make(SubCounty)
        mommy.make(SubCounty)
        mommy.make(SubCounty)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(5, response.data.get("count"))
        self.assertEquals(5, SubCounty.objects.count())

    def test_retreiving(self):
        mommy.make(SubCounty)
        sub_county = mommy.make(SubCounty)
        url = self.url + "{}/".format(sub_county.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(str(sub_county.id), response.data.get("id"))

    def test_updating(self):
        sub_county = mommy.make(SubCounty)
        data = {
            "name": "name has been edited"
        }
        url = self.url + "{}/".format(sub_county.id)
        response = self.client.patch(url, data)
        ssub_county_refetched = SubCounty.objects.get(id=sub_county.id)
        self.assertEquals(200, response.status_code)
        self.assertEquals(ssub_county_refetched.name, data.get("name"))


class TestErrorQueueView(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:common:error_queues_list")
        super(TestErrorQueueView, self).setUp()

    def test_listing(self):
        mommy.make(ErrorQueue, _quantity=6)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(6, response.data.get('count'))

    def test_retrieval(self):
        error = mommy.make(ErrorQueue)
        mommy.make(ErrorQueue)
        url = self.url + "{}/".format(error.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(error.id, response.data.get('id'))

    def test_filtering(self):
        mommy.make(ErrorQueue, error_type='SEARCH_INDEXING_ERROR')
        mommy.make(ErrorQueue, error_type='SEND_EMAIL_ERROR')
        url = self.url + "?error_type=SEND_EMAIL_ERROR"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            'SEND_EMAIL_ERROR',
            response.data.get('results')[0].get('error_type'))

        url = self.url + "?error_type=SEARCH_INDEXING_ERROR"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            'SEARCH_INDEXING_ERROR',
            response.data.get('results')[0].get('error_type'))


class TestAdminUnitsFiltering(LoginMixin, APITestCase):
    def test_filter_counties(self):
        nat_user = mommy.make(get_user_model(), is_national=True)

        # should see all counties
        mommy.make(County, _quantity=5)
        self.client.force_authenticate(nat_user)
        url = reverse("api:common:counties_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(5, response.data.get('count'))
        self.client.logout()

        # county user should see only his county
        county_user = mommy.make(get_user_model())
        county = mommy.make(County)
        mommy.make(UserCounty, user=county_user, county=county)
        self.client.force_authenticate(county_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            county.name, response.data.get('results')[0].get('name'))
        self.client.logout()

        # constituency user should see the county they belong to
        const = mommy.make(Constituency, county=county)
        const_user = mommy.make(get_user_model())
        mommy.make(
            UserConstituency, constituency=const, created_by=county_user,
            updated_by=county_user, user=const_user)
        self.client.force_authenticate(const_user)
        response = self.client.get(url)

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            county.name, response.data.get('results')[0].get('name'))
        self.client.logout()

        # sub-county user should see the county they belong to
        sub = mommy.make(SubCounty, county=county)
        sub_user = mommy.make(get_user_model())
        mommy.make(
            UserSubCounty, sub_county=sub, created_by=county_user,
            updated_by=county_user, user=sub_user)
        self.client.force_authenticate(sub_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            county.name, response.data.get('results')[0].get('name'))
        self.client.logout()

    def test_filter_constituencies(self):
        nat_user = mommy.make(get_user_model(), is_national=True)

        # should see all counties
        mommy.make(Constituency, _quantity=5)
        self.client.force_authenticate(nat_user)
        url = reverse("api:common:constituencies_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(5, response.data.get('count'))
        self.client.logout()

        # county user should see only his county
        county_user = mommy.make(get_user_model())
        county = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        mommy.make(UserCounty, user=county_user, county=county)
        self.client.force_authenticate(county_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            const.name, response.data.get('results')[0].get('name'))
        self.client.logout()

        # constituency user should see the county they belong to
        const = mommy.make(Constituency, county=county)
        const_user = mommy.make(get_user_model())
        mommy.make(
            UserConstituency, constituency=const, created_by=county_user,
            updated_by=county_user, user=const_user)
        self.client.force_authenticate(const_user)
        response = self.client.get(url)

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            const.name, response.data.get('results')[0].get('name'))
        self.client.logout()

        # sub-county user should see the county they belong to
        sub = mommy.make(SubCounty, county=county)
        sub_user = mommy.make(get_user_model())
        mommy.make(
            UserSubCounty, sub_county=sub, created_by=county_user,
            updated_by=county_user, user=sub_user)
        self.client.force_authenticate(sub_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('count'))
        self.assertEquals(
            const.name, response.data.get('results')[0].get('name'))
        self.client.logout()

    def test_filter_wards(self):
        nat_user = mommy.make(get_user_model(), is_national=True)

        # should see all counties
        mommy.make(Ward, _quantity=5)
        self.client.force_authenticate(nat_user)
        url = reverse("api:common:wards_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(5, response.data.get('count'))
        self.client.logout()

        # county user should see only his county
        county_user = mommy.make(get_user_model())
        county = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=const)
        mommy.make(UserCounty, user=county_user, county=county)
        self.client.force_authenticate(county_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            ward.name, response.data.get('results')[0].get('name'))
        self.client.logout()

        # constituency user should see the county they belong to
        const = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=const)
        const_user = mommy.make(get_user_model())
        mommy.make(
            UserConstituency, constituency=const, created_by=county_user,
            updated_by=county_user, user=const_user)
        self.client.force_authenticate(const_user)
        response = self.client.get(url)

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            ward.name, response.data.get('results')[0].get('name'))
        self.client.logout()

        # sub-county user should see the county they belong to
        sub = mommy.make(SubCounty, county=county)
        ward = mommy.make(Ward, constituency=const, sub_county=sub)
        sub_user = mommy.make(get_user_model())
        mommy.make(
            UserSubCounty, sub_county=sub, created_by=county_user,
            updated_by=county_user, user=sub_user)
        self.client.force_authenticate(sub_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            ward.name, response.data.get('results')[0].get('name'))
        self.client.logout()

        # test user assigned both sub-county and constituency
        mommy.make(
            UserConstituency, user=sub_user, created_by=county_user,
            updated_by=county_user, constituency=const)
        self.client.force_authenticate(sub_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get("count"))

    def test_filter_sub_counties(self):
        nat_user = mommy.make(get_user_model(), is_national=True)

        # should see all counties
        mommy.make(SubCounty, _quantity=5)
        self.client.force_authenticate(nat_user)
        url = reverse("api:common:sub_counties_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(5, response.data.get('count'))
        self.client.logout()

        # county user should see only his county
        county_user = mommy.make(get_user_model())
        county = mommy.make(County)
        sub = mommy.make(SubCounty, county=county)
        mommy.make(UserCounty, user=county_user, county=county)
        self.client.force_authenticate(county_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.assertEquals(
            sub.name, response.data.get('results')[0].get('name'))
        self.client.logout()

        # constituency user should see the county they belong to
        const = mommy.make(Constituency, county=county)
        const_user = mommy.make(get_user_model())
        mommy.make(
            UserConstituency, constituency=const, created_by=county_user,
            updated_by=county_user, user=const_user)
        self.client.force_authenticate(const_user)
        response = self.client.get(url)

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

        # sub-county user should see the county they belong to
        sub = mommy.make(SubCounty, county=county)
        sub_user = mommy.make(get_user_model())
        mommy.make(
            UserSubCounty, sub_county=sub, created_by=county_user,
            updated_by=county_user, user=sub_user)
        self.client.force_authenticate(sub_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('count'))
        self.assertEquals(
            sub.name, response.data.get('results')[0].get('name'))
        self.client.logout()
