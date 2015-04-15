import json

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import LogginMixin, default

from ..serializers import (
    OwnerSerializer, ServiceSerializer, FacilitySerializer,
    FacilityStatusSerializer, FacilityUnitSerializer
)

from ..models import (
    OwnerType, Owner, ServiceCategory,
    Service, FacilityStatus,
    Facility, FacilityUnit
)


class TestOwnersView(LogginMixin, APITestCase):
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


class TestServiceView(LogginMixin, APITestCase):
    def setUp(self):
        super(TestServiceView, self).setUp()
        self.url = reverse("api:facilities:services_list")

    def test_list_services(self):
        service_cat = mommy.make(ServiceCategory, b_c_service=True)
        service_1 = mommy.make(Service, category=service_cat)
        service_2 = mommy.make(Service, category=service_cat)
        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                ServiceSerializer(service_2).data,
                ServiceSerializer(service_1).data
            ]
        }
        self.maxDiff = None
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_post(self):
        service_cat = mommy.make(ServiceCategory, b_c_service=True)
        data = {
            "name": "Diabetes screening",
            "description": "This is a description of the service",
            "category": service_cat.id
        }
        response = self.client.post(self.url, data)
        response_data = json.dumps(response.data, default=default)
        self.assertEquals(201, response.status_code)
        self.assertIn("id", response_data)
        self.assertIn("name", response_data)
        self.assertIn("code", response_data)
        self.assertIn("description", response_data)
        self.assertIn("category", response_data)
        self.assertIn("active", response_data)
        self.assertEquals(1, Service.objects.count())

    def test_retrive_single_service(self):
        service_cat = mommy.make(ServiceCategory, b_c_service=True)
        service = mommy.make(Service, category=service_cat)
        url = self.url + "{}/".format(service.id)
        response = self.client.get(url)
        expected_data = ServiceSerializer(service).data
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_filtering(self):
        service_cat = mommy.make(ServiceCategory, b_c_service=True)
        service_cat_2 = mommy.make(ServiceCategory, b_c_service=True)
        service_1 = mommy.make(
            Service, name='Cancer screening', category=service_cat)
        service_2 = mommy.make(
            Service, name='Diabetes screening', category=service_cat)
        service_3 = mommy.make(
            Service, name='Malaria screening', category=service_cat_2)
        expected_data_1 = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                ServiceSerializer(service_2).data,
                ServiceSerializer(service_1).data
            ]
        }
        url = self.url + "?category={}".format(service_cat.id)
        response_1 = self.client.get(url)
        self.assertEquals(200, response_1.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data_1, default=default)),
            json.loads(json.dumps(response_1.data, default=default)))
        expected_data_2 = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                ServiceSerializer(service_3).data
            ]
        }
        url = self.url + "?category={}".format(service_cat_2.id)
        response_2 = self.client.get(url)
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data_2, default=default)),
            json.loads(json.dumps(response_2.data, default=default)))


class TestFacilityView(LogginMixin, APITestCase):
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

    def test_retrieve_facility(self):
        facility = mommy.make(Facility)
        url = self.url + "{}/".format(facility.id)
        response = self.client.get(url)
        expected_data = FacilitySerializer(facility).data
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))


class TestFacilityStatusView(LogginMixin, APITestCase):
    def setUp(self):
        super(TestFacilityStatusView, self).setUp()
        self.url = reverse("api:facilities:facility_statuses_list")

    def test_list_facility_status(self):
        status_1 = mommy.make(FacilityStatus)
        status_2 = mommy.make(FacilityStatus)
        status_3 = mommy.make(FacilityStatus)
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
        status = mommy.make(FacilityStatus)
        url = self.url + "{}/".format(status.id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, FacilityStatusSerializer(status).data)


class TestFacilityUnitView(LogginMixin, APITestCase):
    def setUp(self):
        super(TestFacilityUnitView)
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

    def test_retrive_facility_unit(self):
        unit = mommy.make(FacilityUnit)
        expected_data = FacilityUnitSerializer(unit).data
        url = self.url + "{}/".format(unit.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))
