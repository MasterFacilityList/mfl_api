import json

from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from ..models import County, Contact, Constituency, SubCounty
from .test_models import BaseTestCase


class TestViewCounties(BaseTestCase, APITestCase):
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
                {
                    "id": county.id,
                    "name": county.name,
                    "code": county.code,
                },
                {
                    "id": county_2.id,
                    "name": county_2.name,
                    "code": county_2.code
                }
            ]
        }
        self.assertEquals(expected_data, response.data)
        self.assertEquals(200, response.status_code)

    def test_retrieve_single_county(self):
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        url = reverse('api:common:counties_list')

        response = self.client.get(url, args={'id': county.id})
        expected_data = {
            "id": county.id,
            "name": county.name,
            "code": county.code

        }
        self.assertEquals(expected_data, response.data)
        self.assertEquals(200, response.status_code)


class TestViewConstituencies(BaseTestCase, APITestCase):
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
                {
                    "id": constituency.id,
                    "name": constituency.name,
                    "code": constituency.code,
                    "county": constituency.county.id
                },
                {
                    "id": constituency_2.id,
                    "name": constituency_2.name,
                    "code": constituency_2.code,
                    "county": constituency_2.county.id
                }
            ]
        }
        self.assertEquals(expected_data, response.data)
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
        response = self.client.get(url, args={'id': constituency.id})
        expected_data = {
            "id": constituency.id,
            "name": constituency.name,
            "code": constituency.code,
            "county": constituency.county.id
        }
        self.assertEquals(expected_data, response.data)
        self.assertEquals(200, response.status_code)


class TestViewSubCounties(BaseTestCase, APITestCase):
    def test_list_sub_counties(self):
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        sub_county_1 = SubCounty.objects.create(
            created_by=self.user, updated_by=self.user, county=county,
            name='sub county 1',
            code='335')
        sub_county_2 = SubCounty.objects.create(
            created_by=self.user, updated_by=self.user, name='sub county 2',
            code='337', county=county)
        url = reverse('api:common:sub_counties_list')
        response = self.client.get(url)
        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": sub_county_1.id,
                    "name": sub_county_1.name,
                    "code": sub_county_1.code,
                    "county": sub_county_1.county.id
                },
                {
                    "id": sub_county_2.id,
                    "name": sub_county_2.name,
                    "code": sub_county_2.code,
                    "county": sub_county_2.county.id
                }
            ]
        }
        self.assertEquals(expected_data, response.data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('count'))

    def test_retrive_single_sub_county(self):
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        sub_county = SubCounty.objects.create(
            created_by=self.user, updated_by=self.user, county=county,
            name='sub county',
            code='335')
        url = reverse('api:common:sub_counties_list')
        url += "{}/".format(sub_county.id)
        import pdb
        pdb.set_trace()
        response = self.client.get(url)
        expected_data = {
            "id": sub_county.id,
            "name": sub_county.name,
            "code": sub_county.code,
            "county": sub_county.county.id
        }
        self.assertEquals(expected_data, response.data)
        self.assertEquals(200, response.status_code)
