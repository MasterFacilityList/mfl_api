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
        self.assertEquals(2, response.data.get('count'))
        self.assertEquals(200, response.status_code)

    def test_retrieve_single_county(self):
        county = County.objects.create(
            created_by=self.user, updated_by=self.user,
            name='county 1', code='100')
        url = reverse('api:common:counties_list')

        response = self.client.get(url, {'id': county.id})
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
        response = self.client.get(url, {'id': constituency.id})
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
        response = self.client.get(url, {'id': sub_county.id})
        self.assertEquals(200, response.status_code)
