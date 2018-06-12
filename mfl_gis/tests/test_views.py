from rest_framework.test import APITestCase
from common.tests.test_views import LoginMixin
from common.models import Ward, County, Constituency
from django.core.urlresolvers import reverse
from model_mommy import mommy

from facilities.models import FacilityUpdates, Facility

from ..models import (
    WorldBorder,
    CountyBoundary,
    ConstituencyBoundary,
    WardBoundary,
    FacilityCoordinates,
    GeoCodeMethod,
    GeoCodeSource
)
from ..serializers import WorldBorderDetailSerializer


class TestCountryBoundariesView(LoginMixin, APITestCase):

    def test_retrieve_single_country_boundary(self):
        country = mommy.make(WorldBorder)
        url = reverse(
            'api:mfl_gis:world_border_detail', kwargs={'pk': country.pk})
        response = self.client.get(url)
        expected_data = WorldBorderDetailSerializer(
            country,
            context={
                'request': response.request
            }
        ).data
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

    def test_create_facility_coordinates_success(self):
        mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        facilities = Facility.objects.all()
        ward = facilities[0].ward
        facility = mommy.make(Facility, ward=ward)
        method = mommy.make(GeoCodeMethod)
        source = mommy.make(GeoCodeSource)
        facility_coords = FacilityCoordinates.objects.all()
        data = {
            "facility": str(facility.id),
            "method": str(method.id),
            "source": str(source.id),
            "coordinates": {
                "type": "POINT",
                "coordinates": [
                    facility_coords[0].coordinates[0],
                    facility_coords[0].coordinates[1]
                ]

            }

        }
        url = self.url
        response = self.client.post(url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(2, FacilityCoordinates.objects.count())

    def test_create_facility_coordinates_success_facility_approved(self):
        mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        facilities = Facility.objects.all()
        ward = facilities[0].ward
        facility = mommy.make(Facility, ward=ward)
        facility.approved = True
        facility.save(allow_save=True)
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertTrue(facility_refetched.approved)
        method = mommy.make(GeoCodeMethod)
        source = mommy.make(GeoCodeSource)
        facility_coords = FacilityCoordinates.objects.all()
        data = {
            "facility": facility.id,
            "method": method.id,
            "source": source.id,
            "coordinates": {
                "type": "POINT",
                "coordinates": [
                    facility_coords[0].coordinates[0],
                    facility_coords[0].coordinates[1]
                ]

            }

        }
        url = self.url
        response = self.client.post(url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, FacilityCoordinates.objects.count())
        self.assertEquals(1, FacilityUpdates.objects.count())

        update = FacilityUpdates.objects.all()[0]
        approval_url = reverse(
            "api:facilities:facility_updates_detail",
            kwargs={'pk': str(update.id)})
        approval_payload = {
            "approved": True
        }
        approval_response = self.client.patch(approval_url, approval_payload)
        self.assertEquals(200, approval_response.status_code)
        self.assertEquals(2, FacilityCoordinates.objects.count())

    def test_create_facility_coordinates_error(self):
        mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        facilities = Facility.objects.all()
        ward = facilities[0].ward
        facility = mommy.make(Facility, ward=ward)
        method = mommy.make(GeoCodeMethod)
        source = mommy.make(GeoCodeSource)
        facility_coords = FacilityCoordinates.objects.all()
        data = {
            "facility": str(facility.id),
            "method": str(method.id),
            "source": str(source.id),
            "coordinates": {
                "type": "POINT",
                "coordinates": [
                    facility_coords[0].coordinates[1],
                    facility_coords[0].coordinates[0]
                ]

            }

        }

        response = self.client.post(self.url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(1, FacilityCoordinates.objects.count())

    def test_update_facility_coordinates(self):
        mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        method = mommy.make(GeoCodeMethod)
        source = mommy.make(GeoCodeSource)
        data = {
            "method": str(method.id),
            "source": str(source.id),
            "coordinates": {
                "type": "POINT",
                "coordinates": [13525, 23525]

            }

        }
        facility_coords = FacilityCoordinates.objects.all()
        url = self.url + str(facility_coords[0].id) + "/"
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(0, FacilityUpdates.objects.count())

    def test_update_facility_coordinates_success(self):
        mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        method = mommy.make(GeoCodeMethod)
        source = mommy.make(GeoCodeSource)
        facility_coords = FacilityCoordinates.objects.all()
        facility = facility_coords[0].facility
        facility.approved = True
        facility.save(allow_save=True)
        data = {
            "facility": str(facility.id),
            "method": str(method.id),
            "source": str(source.id),
            "coordinates": {
                "type": "POINT",
                "coordinates": [
                    facility_coords[0].coordinates[0],
                    facility_coords[0].coordinates[1]
                ]

            }

        }

        url = self.url + str(facility_coords[0].id) + "/"
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityCoordinates.objects.count())
        self.assertEquals(1, FacilityUpdates.objects.count())

        # approve the facility updates
        update = FacilityUpdates.objects.all()[0]
        approval_url = reverse(
            "api:facilities:facility_updates_detail",
            kwargs={'pk': str(update.id)})
        approval_payload = {
            "approved": True
        }
        approval_response = self.client.patch(approval_url, approval_payload)
        self.assertEquals(200, approval_response.status_code)
        self.assertEquals(1, FacilityCoordinates.objects.count())

    def test_update_facility_coordinates_success_facility_not_approved(self):
        mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        method = mommy.make(GeoCodeMethod)
        source = mommy.make(GeoCodeSource)
        facility_coords = FacilityCoordinates.objects.all()
        facility = facility_coords[0].facility
        data = {
            "facility": str(facility.id),
            "method": str(method.id),
            "source": str(source.id),
            "coordinates": {
                "type": "POINT",
                "coordinates": [
                    facility_coords[0].coordinates[0],
                    facility_coords[0].coordinates[1]
                ]

            }

        }

        url = self.url + str(facility_coords[0].id) + "/"
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, FacilityUpdates.objects.count())
        self.assertEquals(1, FacilityCoordinates.objects.count())

    def test_update_coordinates_only(self):
        mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')

        facility_coords = FacilityCoordinates.objects.all()
        facility = facility_coords[0].facility
        facility.approved = True
        facility.save(allow_save=True)
        data = {
            "facility": str(facility.id),
            "coordinates": {
                "type": "POINT",
                "coordinates": [
                    facility_coords[0].coordinates[0],
                    facility_coords[0].coordinates[1]
                ]

            }

        }

        url = self.url + str(facility_coords[0].id) + "/"
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityCoordinates.objects.count())
        self.assertEquals(1, FacilityUpdates.objects.count())

        update = FacilityUpdates.objects.all()[0]
        approval_url = reverse(
            "api:facilities:facility_updates_detail",
            kwargs={'pk': str(update.id)})
        approval_payload = {
            "approved": True
        }
        approval_response = self.client.patch(approval_url, approval_payload)
        self.assertEquals(200, approval_response.status_code)
        self.assertEquals(1, FacilityCoordinates.objects.count())


class TestBoundaryBoundsView(LoginMixin, APITestCase):

    def test_get_county_boundary(self):
        boundary = mommy.make(CountyBoundary)
        url = reverse(
            "api:mfl_gis:county_bound",
            kwargs={'pk': str(boundary.id)})
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_constituency_boundary(self):
        boundary = mommy.make(ConstituencyBoundary)
        url = reverse(
            "api:mfl_gis:constituency_bound",
            kwargs={'pk': str(boundary.id)})
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)


class TestIkoWapi(LoginMixin, APITestCase):

    def setUp(self):
        super(TestIkoWapi, self).setUp()
        self.url = reverse("api:mfl_gis:ikowapi")

    def test_invalid_lat_long(self):
        resp = self.client.post(self.url, {
            "longitude": "1.234",
            "latitude": "32.234"
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("longitude", resp.data)
        self.assertIn("latitude", resp.data, )

    def test_invalid_lat(self):
        resp = self.client.post(self.url, {
            "longitude": 1.234,
            "latitude": "32.234"
        })
        self.assertEqual(resp.status_code, 400)
        self.assertNotIn("longitude", resp.data)
        self.assertIn("latitude", resp.data)

    def test_invalid_long(self):
        resp = self.client.post(self.url, {
            "longitude": "1.234",
            "latitude": 32.234
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("longitude", resp.data)
        self.assertNotIn("latitude", resp.data)

    def test_find_ward_found(self):
        mommy.make_recipe("mfl_gis.tests.ward_boundary_recipe")
        resp = self.client.post(self.url, {
            "longitude": 36.78378206656476,
            "latitude": -1.2840274151085824
        })
        self.assertEqual(resp.status_code, 200)
        for i in ['ward', 'constituency', 'county']:
            self.assertIn(i, resp.data)

    def test_find_ward_not_found(self):
        mommy.make_recipe("mfl_gis.tests.ward_boundary_recipe")
        resp = self.client.post(self.url, {
            "longitude": 3.780612,
            "latitude": -1.275611
        })
        self.assertEqual(resp.status_code, 400)


class TestDrillDownFacility(LoginMixin, APITestCase):

    def setUp(self):
        super(TestDrillDownFacility, self).setUp()
        self.url = reverse("api:mfl_gis:drilldown_facility")

    def test_listing(self):
        mommy.make_recipe('mfl_gis.tests.facility_coordinates_recipe')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class TestDrillDownCountry(LoginMixin, APITestCase):

    def setUp(self):
        super(TestDrillDownCountry, self).setUp()
        self.url = reverse("api:mfl_gis:drilldown_country")

    def test_get_listing(self):
        mommy.make_recipe('mfl_gis.tests.county_boundary_recipe')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['meta']['name'], 'KENYA')
        self.assertIsInstance(resp.data['geojson'], dict)


class TestDrillDownCounty(LoginMixin, APITestCase):

    def setUp(self):
        super(TestDrillDownCounty, self).setUp()
        self.url = "api:mfl_gis:drilldown_county"

    def test_get_listing(self):
        cb = mommy.make_recipe('mfl_gis.tests.county_boundary_recipe')
        mommy.make_recipe("mfl_gis.tests.constituency_boundary_recipe")
        resp = self.client.get(
            reverse(self.url, kwargs={"code": cb.area.code})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['meta']['name'], cb.area.name)
        self.assertIsInstance(resp.data['geojson'], dict)


class TestDrillDownConstituency(LoginMixin, APITestCase):

    def setUp(self):
        super(TestDrillDownConstituency, self).setUp()
        self.url = "api:mfl_gis:drilldown_constituency"

    def test_get_listing(self):
        mommy.make_recipe('mfl_gis.tests.county_boundary_recipe')
        cb2 = mommy.make_recipe("mfl_gis.tests.constituency_boundary_recipe")
        mommy.make_recipe("mfl_gis.tests.ward_boundary_recipe")
        resp = self.client.get(
            reverse(self.url, kwargs={"code": cb2.area.code})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['meta']['name'], cb2.area.name)
        self.assertEqual(
            resp.data['meta']['county_code'], cb2.area.county.code
        )
        self.assertIsInstance(resp.data['geojson'], dict)


class TestDrillDownWard(LoginMixin, APITestCase):

    def setUp(self):
        super(TestDrillDownWard, self).setUp()
        self.url = "api:mfl_gis:drilldown_ward"

    def test_get_listing(self):
        wb = mommy.make_recipe("mfl_gis.tests.ward_boundary_recipe")
        resp = self.client.get(
            reverse(self.url, kwargs={"code": wb.area.code})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['properties']['name'], wb.area.name)
        self.assertEqual(
            resp.data['properties']['county_code'],
            wb.area.constituency.county.code
        )
        self.assertEqual(
            resp.data['properties']['constituency_code'],
            wb.area.constituency.code
        )
        self.assertEqual(
            resp.data['id'], wb.area.code
        )
        self.assertIsInstance(resp.data['geometry'], dict)
