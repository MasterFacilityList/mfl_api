from django.core.urlresolvers import reverse
from django.test import override_settings
from django.core.cache import cache
from rest_framework.test import APITestCase

from facilities.models import (
    Facility, FacilityUpdates, FacilityApproval,
    Service, FacilityService, FacilityContact,
    RegulatingBody, FacilityUnit)

from model_mommy import mommy

from common.tests.test_views import LoginMixin
from common.models import Contact, ContactType


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
})
class TestFacilityUdpatesBuffering(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:facilities:facilities_list")
        super(TestFacilityUdpatesBuffering, self).setUp()

    def tearDown(self):
        cache.clear()
        super(TestFacilityUdpatesBuffering, self).tearDown()

    def test_facility_updates_facility_not_approved(self):
        facility = mommy.make(Facility)
        url = self.url + "{}/".format(facility.id)
        data = {
            "name": "A new name"
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertEquals('A new name', facility_refetched.name)
        self.assertEquals(0, FacilityUpdates.objects.count())

    def test_facility_updates_facility_approved(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        data = {
            "name": "Editted name"
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertEquals(facility_refetched.name, facility.name)
        self.assertEquals(1, FacilityUpdates.objects.count())
        self.assertIsNotNone(FacilityUpdates.objects.all()[0].facility_updates)

    def test_update_facility_services_facility_not_approved(self):
        facility = mommy.make(Facility)
        url = self.url + "{}/".format(facility.id)
        service_1 = mommy.make(Service)
        service_2 = mommy.make(Service)
        service_3 = mommy.make(Service)

        services = [
            {
                "service": str(service_1.id)
            },
            {
                "service": str(service_2.id)
            },
            {
                "service": str(service_3.id)
            }
        ]
        data = {
            "services": services
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(3, FacilityService.objects.count())
        self.assertEquals(0, FacilityUpdates.objects.count())

    def test_update_facility_service_not_invalid(self):
        facility = mommy.make(Facility)
        url = self.url + "{}/".format(facility.id)
        service = mommy.make(Service)
        service_id = service.id
        service.delete()
        service_2 = mommy.make(Service)
        services = [
            {
                "service": 'afaflafasl'
            },
            {
                "service": service_id
            },
            {
                "non_service": str(service_2.id)
            }
        ]
        data = {
            "services": services
        }
        response = self.client.patch(url, data)

        self.assertEquals(400, response.status_code)
        self.assertEquals(0, FacilityService.objects.count())
        self.assertEquals(0, FacilityUpdates.objects.count())

    def test_update_facility_contacts_when_facility_is_not_approved(self):
        facility = mommy.make(Facility)
        contact_type = mommy.make(ContactType)
        contacts = [
            {
                "contact": "email@test.com",
                "contact_type": str(contact_type.id)
            }
        ]
        data = {
            "contacts": contacts
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, FacilityUpdates.objects.count())
        self.assertEquals(1, FacilityContact.objects.count())
        self.assertEquals(1, Contact.objects.count())

    def test_update_facility_contacts_when_facility_is_approved(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        contact_type = mommy.make(ContactType)
        contacts = [
            {
                "contact": "email@test.com",
                "contact_type": str(contact_type.id)
            }
        ]
        data = {
            "contacts": contacts
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUpdates.objects.count())
        self.assertEquals(0, FacilityContact.objects.count())
        self.assertEquals(0, Contact.objects.count())

    def test_update_contacts_invalid_data(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        contact_type = mommy.make(ContactType)
        contact_type.delete()
        contacts = [
            {
                "contact": "email@test.com",
                "contact_type": str(contact_type.id)
            },
            {
                "contact": "email@test.com",
                "contact_type": 'asfasfasfasfasf'
            },
            {
                "not_contact_key": "email@test.com",
                "not_contact_type_key": str(contact_type.id)
            }
        ]
        data = {
            "contacts": contacts
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(0, FacilityUpdates.objects.count())
        self.assertEquals(0, FacilityContact.objects.count())
        self.assertEquals(0, Contact.objects.count())

    def test_update_facility_units_facility_not_approved(self):
        facility = mommy.make(Facility)
        url = self.url + "{}/".format(facility.id)
        regulating_body = mommy.make(RegulatingBody)
        facility_units = [
            {
                "name": "The Facilities Pharmacy",
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "regulating_body": regulating_body.id
            }
        ]
        data = {
            "units": facility_units
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUnit.objects.count())

    def test_update_facility_units_invalid_facility_approved(self):
        facility = mommy.make(Facility)
        url = self.url + "{}/".format(facility.id)
        mommy.make(FacilityApproval, facility=facility)
        regulating_body = mommy.make(RegulatingBody)
        facility_units = [
            {
                "name": "The Facilities Pharmacy",
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "regulating_body": regulating_body.id
            }
        ]
        data = {
            "units": facility_units
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, FacilityUnit.objects.count())

    def test_add_more_facility_services_to_updates(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        service = mommy.make(Service)
        service_1 = mommy.make(Service)
        services = [
            {
                "service": str(service.id)
            }
        ]
        data = {
            "services": services
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUpdates.objects.count())

        services_2 = [
            {
                "service": str(service_1.id)
            }
        ]
        data_2 = {
            "services": services_2
        }
        response = self.client.patch(url, data_2)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUpdates.objects.count())

    def test_add_more_facility_contacts_to_updates(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        contact_type = mommy.make(ContactType)
        contacts = [
            {
                "contact": "test@mail.com",
                "contact_type": str(contact_type.id)
            }
        ]
        data = {
            "contacts": contacts
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUpdates.objects.count())

        contact_type_2 = mommy.make(ContactType)
        contacts = [
            {
                "contact": "Some other contact",
                "contact_type": str(contact_type_2.id)
            }
        ]
        data_2 = {
            "contacts": contacts
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data_2)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUpdates.objects.count())

    def test_add_more_facility_units_on_updates(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        regulating_body = mommy.make(RegulatingBody)
        units = [
            {

                "name": "The Facilities Pharmacy",
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "regulating_body": regulating_body.id

            }
        ]
        data = {
            "units": units
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUpdates.objects.count())

        regulating_body_2 = mommy.make(RegulatingBody)
        units = [
            {
                "name": "The is another ",
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "regulating_body": regulating_body_2.id
            }
        ]
        data_2 = {
            "units": units
        }
        response = self.client.patch(url, data_2)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUpdates.objects.count())

    def test_update_facility_unit_update_invalid_data(self):
        facility = mommy.make(Facility)
        units = [
            {
                "name": "The is another ",
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "notregulating_body": ""
            }
        ]
        data = {
            "units": units
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(0, FacilityUpdates.objects.count())

    def test_update_facility_unit_update_reg_body_does_not_exist(self):
        facility = mommy.make(Facility)
        regulating_body = mommy.make(RegulatingBody)
        units = [
            {
                "name": "The is another ",
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "regulating_body": str(regulating_body.id)
            }
        ]
        regulating_body.delete()
        data = {
            "units": units
        }
        url = self.url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(0, FacilityUpdates.objects.count())


class TestFacilityUpdatesApproval(LoginMixin, APITestCase):
    def setUp(self):
        self.facilities_url = reverse("api:facilities:facilities_list")
        super(TestFacilityUpdatesApproval, self).setUp()

    def test_approve_requested_updates(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        url = self.facilities_url + "{}/".format(facility.id)

        service_1 = mommy.make(Service)
        services = [
            {
                "service": str(service_1.id)
            }
        ]
        contact_type = mommy.make(ContactType)
        contacts = [
            {
                "contact_type": str(contact_type.id),
                "contact": "Some contact"
            }
        ]
        regulating_body = mommy.make(RegulatingBody)
        units = [
            {
                "name": "some unit name",
                "description": "The description of the unit",
                "regulating_body": str(regulating_body.id)
            }
        ]
        data = {
            "name": "The name has been Editted",
            "units": units,
            "services": services,
            "contacts": contacts
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUpdates.objects.count())
        update = FacilityUpdates.objects.all()[0]
        self.assertIsNotNone(update.facility_updates)
        self.assertIsNotNone(update.services)
        self.assertIsNotNone(update.contacts)
        self.assertIsNotNone(update.units)
        self.assertEquals(0, FacilityContact.objects.count())
        self.assertEquals(0, FacilityUnit.objects.count())
        self.assertEquals(0, FacilityService.objects.count())

        # approve the facility updates
        approval_url = reverse(
            "api:facilities:facility_updates_detail",
            kwargs={'pk': str(update.id)})
        approve_payload = {
            "approved": True
        }
        approval_response = self.client.patch(approval_url, approve_payload)
        self.assertEquals(200, approval_response.status_code)
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertEquals(data.get('name'), facility_refetched.name)
        self.assertEquals(1, FacilityService.objects.count())
        self.assertEquals(1, FacilityContact.objects.count())
        self.assertEquals(1, FacilityUnit.objects.count())

    def test_reject_requested_updates(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        url = self.facilities_url + "{}/".format(facility.id)

        service_1 = mommy.make(Service)
        services = [
            {
                "service": str(service_1.id)
            }
        ]
        contact_type = mommy.make(ContactType)
        contacts = [
            {
                "contact_type": str(contact_type.id),
                "contact": "Some contact"
            }
        ]
        regulating_body = mommy.make(RegulatingBody)
        units = [
            {
                "name": "some unit name",
                "description": "The description of the unit",
                "regulating_body": str(regulating_body.id)
            }
        ]
        data = {
            "name": "The name has been Editted",
            "units": units,
            "services": services,
            "contacts": contacts
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, FacilityUpdates.objects.count())
        update = FacilityUpdates.objects.all()[0]
        self.assertIsNotNone(update.facility_updates)
        self.assertIsNotNone(update.services)
        self.assertIsNotNone(update.contacts)
        self.assertIsNotNone(update.units)
        self.assertEquals(0, FacilityContact.objects.count())
        self.assertEquals(0, FacilityUnit.objects.count())
        self.assertEquals(0, FacilityService.objects.count())

        # approve the facility updates
        approval_url = reverse(
            "api:facilities:facility_updates_detail",
            kwargs={'pk': str(update.id)})
        rejection_payload = {
            "cancelled": True
        }
        approval_response = self.client.patch(approval_url, rejection_payload)
        self.assertEquals(200, approval_response.status_code)
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertNotEquals(data.get('name'), facility_refetched.name)
        self.assertEquals(0, FacilityService.objects.count())
        self.assertEquals(0, FacilityContact.objects.count())
        self.assertEquals(0, FacilityUnit.objects.count())
