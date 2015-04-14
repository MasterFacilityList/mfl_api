import json
import uuid

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from model_mommy import mommy

from ..models import (
    County, Contact, ContactType, Constituency, Ward)
from ..serializers import (
    ContactSerializer, WardSerializer, CountySerializer,
    ConstituencySerializer)
from .test_models import BaseTestCase


def default(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)


class LogginMixin(object):

    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.client.force_authenticate(user=self.user)
        super(LogginMixin, self).setUp()


class TestViewCounties(LogginMixin, BaseTestCase, APITestCase):
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
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                CountySerializer(county).data,
                CountySerializer(county_2).data
            ]
        }
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
        self.assertEquals(200, response.status_code)

    def test_retrieve_single_county(self):
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        url = reverse('api:common:counties_list')
        url += "{}/".format(county.id)
        response = self.client.get(url)
        expected_data = CountySerializer(county).data
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
        self.assertEquals(200, response.status_code)


class TestViewConstituencies(LogginMixin, BaseTestCase, APITestCase):
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
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                ConstituencySerializer(constituency).data,
                ConstituencySerializer(constituency_2).data
            ]
        }
        # some weird ordering the dumps string
        # json.loads the dumped string to check equality of dicts
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
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
        expected_data = ConstituencySerializer(constituency).data
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
        self.assertEquals(200, response.status_code)


class TestViewWards(LogginMixin, BaseTestCase, APITestCase):
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
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                WardSerializer(ward_1).data,
                WardSerializer(ward_2).data
            ]
        }
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
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
        expected_data = WardSerializer(ward).data
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
        self.assertEquals(200, response.status_code)


class TestContactView(LogginMixin, BaseTestCase, APITestCase):
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

        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                ContactSerializer(contact).data,
                ContactSerializer(contact_1).data
            ]
        }
        response = self.client.get(self.url)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

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


class TestContactTypeView(LogginMixin, BaseTestCase, APITestCase):
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


class TestAPIRootView(APITestCase):
    def test_list_endpoints(self):
        url = reverse('api:common:url_listing')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
