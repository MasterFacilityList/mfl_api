import json

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import (
    LoginMixin,
    default
)
from common.models import Ward, UserCounty

from ..serializers import (
    OwnerSerializer,
    FacilitySerializer,
    FacilityStatusSerializer,
    FacilityUnitSerializer
)
from ..models import (
    OwnerType,
    Owner,
    FacilityStatus,
    Facility,
    FacilityUnit,
    FacilityRegulationStatus
)


class TestOwnersView(LoginMixin, APITestCase):
    def setUp(self):
        super(TestOwnersView, self).setUp()
        self.url = reverse('api:facilities:owners_list')

    def test_list_owners(self):
        ownertype = mommy.make(OwnerType)
        owner_1 = mommy.make(Owner, owner_type=ownertype)
        owner_2 = mommy.make(Owner, owner_type=ownertype)
        response = self.client.get(self.url)
        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                OwnerSerializer(owner_2).data,
                OwnerSerializer(owner_1).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_post(self):
        owner_type = mommy.make(OwnerType)

        data = {

            "name": "Ministry of Health",
            "description": "This is the minisrry of health Kenya",
            "abbreviation": "MOH",
            "owner_type": owner_type.id
        }
        response = self.client.post(self.url, data)
        response_data = json.dumps(response.data, default=default)
        self.assertEquals(201, response.status_code)
        self.assertIn("id", response_data)
        self.assertIn("code", response_data)
        self.assertIn("name", response_data)
        self.assertIn("description", response_data)
        self.assertIn("abbreviation", response_data)
        self.assertIn("owner_type", response_data)
        self.assertEquals(1, Owner.objects.count())

    def test_retrive_single_owner(self):
        owner_type = mommy.make(OwnerType)
        owner = mommy.make(Owner, owner_type=owner_type)
        url = self.url + "{}/".format(owner.id)
        response = self.client.get(url)
        expected_data = OwnerSerializer(owner).data
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_filtering(self):
        owner_type_1 = mommy.make(OwnerType)
        owner_type_2 = mommy.make(OwnerType)
        owner_1 = mommy.make(Owner, name='CHAK', owner_type=owner_type_1)
        owner_2 = mommy.make(Owner, name='MOH', owner_type=owner_type_1)
        owner_3 = mommy.make(Owner, name='Private', owner_type=owner_type_2)
        expected_data_1 = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                # Due to ordering in view CHAK will always be first
                OwnerSerializer(owner_2).data,
                OwnerSerializer(owner_1).data
            ]
        }
        expected_data_2 = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                OwnerSerializer(owner_3).data
            ]
        }
        self.maxDiff = None
        url = self.url + "?owner_type={}".format(owner_type_1.id)
        response_1 = self.client.get(url)

        self.assertEquals(200, response_1.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data_1, default=default)),
            json.loads(json.dumps(response_1.data, default=default)))

        url = self.url + "?owner_type={}".format(owner_type_2.id)
        response_2 = self.client.get(url)

        self.assertEquals(200, response_2.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data_2, default=default)),
            json.loads(json.dumps(response_2.data, default=default)))


class TestFacilityView(LoginMixin, APITestCase):
    def setUp(self):
        super(TestFacilityView, self).setUp()
        self.url = reverse('api:facilities:facilities_list')

    def test_facility_listing(self):
        facility_1 = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        facility_3 = mommy.make(Facility)

        response = self.client.get(self.url)
        expected_data = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                FacilitySerializer(facility_3).data,
                FacilitySerializer(facility_2).data,
                FacilitySerializer(facility_1).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_facilties_that_need_regulation(self):
        facility_1 = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        facility_3 = mommy.make(Facility)
        mommy.make(
            FacilityRegulationStatus, facility=facility_1, is_confirmed=True)
        mommy.make(
            FacilityRegulationStatus, facility=facility_1, is_confirmed=False)
        url = self.url + "?is_regulated=True"
        regulated_expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                FacilitySerializer(facility_1).data
            ]
        }
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(regulated_expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

        # get unregulated
        url = self.url + "?is_regulated=False"
        response_2 = self.client.get(url)
        unregulated_data = regulated_expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                FacilitySerializer(facility_3).data,
                FacilitySerializer(facility_2).data

            ]
        }
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(
            json.loads(json.dumps(unregulated_data, default=default)),
            json.loads(json.dumps(response_2.data, default=default)))

    def test_retrieve_facility(self):
        facility = mommy.make(Facility)
        url = self.url + "{}/".format(facility.id)
        response = self.client.get(url)
        expected_data = FacilitySerializer(facility).data
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))


class CountyAndNationalFilterBackendTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            email='tester@ehealth.or.ke',
            first_name='Test',
            username='test',
            password='mtihani',
            is_national=False
        )
        self.user_county = mommy.make(UserCounty, user=self.user)
        self.client.login(email='tester@ehealth.or.ke', password='mtihani')
        self.maxDiff = None
        self.url = reverse('api:facilities:facilities_list')
        super(CountyAndNationalFilterBackendTest, self).setUp()

    def test_facility_county_national_filter_backend(self):
        """Testing the filtered by county level"""
        mommy.make(Facility)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        # The response should be filtered out for this user; not national
        self.assertEquals(
            len(response.data["results"]),
            0
        )


class TestFacilityStatusView(LoginMixin, APITestCase):
    def setUp(self):
        super(TestFacilityStatusView, self).setUp()
        self.url = reverse("api:facilities:facility_statuses_list")

    def test_list_facility_status(self):
        status_1 = mommy.make(FacilityStatus, name='OPERTATIONAL')
        status_2 = mommy.make(FacilityStatus, name='NON_OPERATIONAL')
        status_3 = mommy.make(FacilityStatus, name='CLOSED')
        response = self.client.get(self.url)
        expected_data = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                FacilityStatusSerializer(status_3).data,
                FacilityStatusSerializer(status_2).data,
                FacilityStatusSerializer(status_1).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_retrive_facility_status(self):
        status = mommy.make(FacilityStatus, name='OPERTATIONAL')
        url = self.url + "{}/".format(status.id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, FacilityStatusSerializer(status).data)


class TestFacilityUnitView(LoginMixin, APITestCase):
    def setUp(self):
        super(TestFacilityUnitView, self).setUp()
        self.url = reverse("api:facilities:facility_units_list")

    def test_list_facility_units(self):
        unit_1 = mommy.make(FacilityUnit)
        unit_2 = mommy.make(FacilityUnit)
        response = self.client.get(self.url)
        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                FacilityUnitSerializer(unit_2).data,
                FacilityUnitSerializer(unit_1).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_retrieve_facility_unit(self):
        unit = mommy.make(FacilityUnit)
        expected_data = FacilityUnitSerializer(unit).data
        url = self.url + "{}/".format(unit.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))


class TestInspectionAndCoverReportsView(LoginMixin, APITestCase):
    def test_inspection_report(self):
        ward = mommy.make(Ward)
        facility = mommy.make(Facility, ward=ward)
        url = reverse(
            'api:facilities:facility_inspection_report',
            kwargs={'facility_id': facility.id})

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'inspection_report.txt')

    def test_cover_reports(self):
        ward = mommy.make(Ward)
        facility = mommy.make(Facility, ward=ward)
        url = reverse(
            'api:facilities:facility_cover_report',
            kwargs={'facility_id': facility.id})

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'cover_report.txt')

    def test_correction_templates(self):
        ward = mommy.make(Ward)
        facility = mommy.make(Facility, ward=ward)
        url = reverse(
            'api:facilities:facility_correction_template',
            kwargs={'facility_id': facility.id})

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'correction_template.txt')
