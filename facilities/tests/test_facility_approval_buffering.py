from django.core.urlresolvers import reverse
from django.test import override_settings
from django.core.cache import cache
from rest_framework.test import APITestCase

from facilities.models import (
    Facility, FacilityUpdates, FacilityApproval,
    Service, FacilityService, FacilityContact)

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

    def test_update_facility_units(self):
        pass

    def test_update_facility_units_invali(self):
        pass

    def test_officer_incharge(self):
        pass

    def test_facility_officer_incharge_invalid(self):
        pass
