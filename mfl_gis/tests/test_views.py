from rest_framework.test import APITestCase
from common.tests.test_views import LoginMixin
from common.models import Ward, County, Constituency
from django.core.urlresolvers import reverse
from model_mommy import mommy

from ..models import (
    WorldBorder,
    CountyBoundary,
    ConstituencyBoundary,
    WardBoundary
)
from ..serializers import WorldBorderDetailSerializer


class TestCountryBoundariesView(LoginMixin, APITestCase):

    def test_retrieve_single_country_boundary(self):
        country = mommy.make(WorldBorder)
        url = reverse(
            'api:mfl_gis:world_border_detail', kwargs={'pk': country.pk})
        response = self.client.get(url)
        expected_data = WorldBorderDetailSerializer(country).data
        # Silly issues with floats being rounded to different precisions
        # between the serializer and the "round trip through the view" version
        self.assertEqual(
            expected_data['properties']['code'],
            response.data['properties']['code']
        )


class TestCountyBoundaryViews(LoginMixin, APITestCase):
    def setUp(self):
        super(TestCountyBoundaryViews, self).setUp()
        self.list_url = reverse('api:mfl_gis:county_boundaries_list')

    def test_listing(self):
        mommy.make(CountyBoundary)
        mommy.make(CountyBoundary)
        boundary_list_response = self.client.get(self.list_url)
        self.assertEqual(200, boundary_list_response.status_code)
        self.assertEqual(2, len(boundary_list_response.data['results']))


class TestConstituencyBoundaryViews(LoginMixin, APITestCase):
    def setUp(self):
        super(TestConstituencyBoundaryViews, self).setUp()
        self.list_url = reverse('api:mfl_gis:constituency_boundaries_list')

    def test_listing(self):
        mommy.make(ConstituencyBoundary)
        mommy.make(ConstituencyBoundary)
        boundary_list_response = self.client.get(self.list_url)
        self.assertEqual(200, boundary_list_response.status_code)
        self.assertEqual(2, len(boundary_list_response.data['results']))


class TestWardBoundaryViews(LoginMixin, APITestCase):
    def setUp(self):
        super(TestWardBoundaryViews, self).setUp()
        self.list_url = reverse('api:mfl_gis:ward_boundaries_list')

    def test_listing(self):
        mommy.make(WardBoundary)
        mommy.make(WardBoundary)
        boundary_list_response = self.client.get(self.list_url)
        self.assertEqual(200, boundary_list_response.status_code)
        self.assertEqual(2, len(boundary_list_response.data['results']))

    def test_get_single(self):
        boundary = mommy.make(WardBoundary)
        url = self.list_url + "{}/".format(boundary.id)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        assert not response.data.get('properties').get('facility_ids')


class TestFacilityCoordinatesListing(LoginMixin, APITestCase):
    def test_list_facility_coordinates(self):
        url = reverse("api:mfl_gis:facility_coordinates_list")
        ward = mommy.make(Ward)
        const = mommy.make(Constituency)
        county = mommy.make(County)
        response = self.client.get(url)
        self.assertIsInstance(response.data, list)
        response = self.client.get(url)
        self.assertIsInstance(response.data, list)
        self.assertEquals(0, len(response.data))

        # test ward filter
        ward_url = url + "?ward={}".format(ward.id)
        response = self.client.get(ward_url)
        self.assertIsInstance(response.data, list)
        self.assertEquals(0, len(response.data))

        # test county
        county_url = url + "?county={}".format(county.id)
        response = self.client.get(county_url)
        self.assertIsInstance(response.data, list)
        self.assertEquals(0, len(response.data))

        # test constituency
        const_url = url + "?constituency={}".format(const.id)
        response = self.client.get(const_url)
        self.assertIsInstance(response.data, list)
        self.assertEquals(0, len(response.data))


class TestPostingFacilityCoordinates(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:mfl_gis:facility_coordinates_simple_list")
        super(TestPostingFacilityCoordinates, self).setUp()

    def test_get(self):
        mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)

    def test_retrieve(self):
        facility_gps = mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        url = self.url + "{}/".format(str(facility_gps.id))
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
