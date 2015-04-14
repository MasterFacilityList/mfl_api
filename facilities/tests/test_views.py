import json

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import LogginMixin, default

from ..models import (
    OwnerType, Owner, JobTitle, OfficerIncharge,
    OfficerInchargeContact, ServiceCategory,
    Service, FacilityStatus, FacilityType,
    RegulatingBody, RegulationStatus, Facility,
    FacilityRegulationStatus, GeoCodeSource,
    GeoCodeMethod, FacilityGPS,
    FacilityService, FacilityContact
)


class TestOnwersView(LogginMixin, APITestCase):
    def setUp(self):
        super(TestOnwersView, self).setUp()
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
                {
                    "id": owner_1.id,
                    "name": owner_1.name,
                    "code": owner_1.code,
                    "description": owner_1.description,
                    "abbreviation": owner_1.abbreviation,
                    "owner_type": owner_1.owner_type.id,
                    "active": True
                },
                {
                    "id": owner_2.id,
                    "name": owner_2.name,
                    "code": owner_2.code,
                    "description": owner_2.description,
                    "abbreviation": owner_2.abbreviation,
                    "owner_type": owner_2.owner_type.id,
                    "active": True
                }
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
        expected_data = {
            "id": owner.id,
            "name": owner.name,
            "code": owner.code,
            "description": owner.description,
            "abbreviation": owner.abbreviation,
            "owner_type": owner.owner_type.id,
            "active": True

        }
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
                {
                    "id": owner_2.id,
                    "name": owner_2.name,
                    "code": owner_2.code,
                    "description": owner_2.description,
                    "abbreviation": owner_2.abbreviation,
                    "owner_type": owner_2.owner_type.id,
                    "active": True
                },
                {
                    "id": owner_1.id,
                    "name": owner_1.name,
                    "code": owner_1.code,
                    "description": owner_1.description,
                    "abbreviation": owner_1.abbreviation,
                    "owner_type": owner_1.owner_type.id,
                    "active": True
                }
            ]
        }
        expected_data_2 = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": owner_3.id,
                    "name": owner_3.name,
                    "code": owner_3.code,
                    "description": owner_3.description,
                    "abbreviation": owner_3.abbreviation,
                    "owner_type": owner_3.owner_type.id,
                    "active": True
                }
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
        service_cat = mommy.make(ServiceCategory)
        service_1 = mommy.make(Service, category=service_cat)
        service_2 = mommy.make(Service, category=service_cat)
        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": service_1.id,
                    "name": service_1.name,
                    "code": service_1.code,
                    "description": service_1.description,
                    "category": service_1.category.id,
                    "active": True
                },
                {
                    "id": service_2.id,
                    "name": service_2.name,
                    "code": service_2.code,
                    "description": service_2.description,
                    "category": service_2.category.id,
                    "active": True
                }
            ]
        }
        self.maxDiff = None
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_post(self):
        service_cat = mommy.make(ServiceCategory)
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
        service = mommy.make(Service)
        url = self.url + "{}/".format(service.id)
        response = self.client.get(url)
        expected_data = {
            "id": service.id,
            "name": service.name,
            "code": service.code,
            "description": service.description,
            "category": service.category.id,
            "active": True
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data, default=default)),
            json.loads(json.dumps(response.data, default=default)))

    def test_filtering(self):
        service_cat = mommy.make(ServiceCategory)
        service_cat_2 = mommy.make(ServiceCategory)
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
                {
                    "id": service_2.id,
                    "name": service_2.name,
                    "code": service_2.code,
                    "description": service_2.description,
                    "category": service_2.category.id,
                    "active": True
                },
                {
                    "id": service_1.id,
                    "name": service_1.name,
                    "code": service_1.code,
                    "description": service_1.description,
                    "category": service_1.category.id,
                    "active": True
                }
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
                {
                    "id": service_3.id,
                    "name": service_3.name,
                    "code": service_3.code,
                    "description": service_3.description,
                    "category": service_3.category.id,
                    "active": True
                }
            ]
        }
        url = self.url + "?category={}".format(service_cat_2.id)
        response_2 = self.client.get(url)
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(
            json.loads(json.dumps(expected_data_2, default=default)),
            json.loads(json.dumps(response_2.data, default=default)))
