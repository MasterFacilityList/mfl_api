from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import (
    LoginMixin
)

from common.models import (
    Contact,
    ContactType
)

from ..models import (
    Facility,
    FacilityOfficer,
    OfficerContact,
    JobTitle,
    OptionGroup
)


class TestFacilityOfficerFacade(LoginMixin, APITestCase):
    def test_listing(self):
        facility = mommy.make(Facility)
        url = reverse(
            "api:facilities:officer_facade_list",
            kwargs={"facility_id": str(facility.id)})
        mommy.make(FacilityOfficer, facility=facility)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, len(response.data))

    def test_delete(self):
        facility = mommy.make(Facility)
        officer = mommy.make(FacilityOfficer, facility=facility)
        url = reverse(
            "api:facilities:officer_facade_delete",
            kwargs={"pk": str(officer.id)})
        self.client.delete(url)
        self.assertEquals(0, FacilityOfficer.objects.count())

    def test_post_officer(self):
        facility = mommy.make(Facility)
        job_title = mommy.make(JobTitle)
        contact_type = mommy.make(ContactType)

        data = {
            "facility_id": str(facility.id),
            "name": "Brenda Makena",
            "id_no": "545454545",
            "reg_no": "DEN/90/2000",
            "title": str(job_title.id),
            "contacts": [
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                },
                {
                    "type": str(contact_type.id),
                    "contact": "0823583941"
                }
            ]
        }
        url = reverse("api:facilities:officer_facade_create")
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(1, FacilityOfficer.objects.count())
        self.assertEquals(2, OfficerContact.objects.count())
        self.assertEquals(2, Contact.objects.count())

    def test_post_officer_facility_does_not_exist(self):
        job_title = mommy.make(JobTitle)
        contact_type = mommy.make(ContactType)

        data = {
            "facility_id": "2a5b6f8b-6992-4c12-8fe0-64de82df8fb1",
            "name": "Brenda Makena",
            "id_no": "545454545",
            "reg_no": "DEN/90/2000",
            "title": str(job_title.id),
            "contacts": [
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                },
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                }
            ]
        }
        url = reverse("api:facilities:officer_facade_create")
        response = self.client.post(url, data)
        self.assertEquals(400, response.status_code)

    def test_post_officer_facility_no_required_fields(self):
        job_title = mommy.make(JobTitle)
        contact_type = mommy.make(ContactType)

        data = {
            "reg_no": "DEN/90/2000",
            "title": str(job_title.id),
            "contacts": [
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                },
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                }
            ]
        }
        url = reverse("api:facilities:officer_facade_create")
        response = self.client.post(url, data)
        self.assertEquals(400, response.status_code)

    def test_post_officer_facility_job_title_does_not_exist(self):
        contact_type = mommy.make(ContactType)

        data = {
            "reg_no": "DEN/90/2000",
            "title": "2a5b6f8b-6992-4c12-8fe0-64de82df8fb1",
            "contacts": [
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                },
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                }
            ]
        }
        url = reverse("api:facilities:officer_facade_create")
        response = self.client.post(url, data)
        self.assertEquals(400, response.status_code)

    def test_post_officer_facility_no_job_title(self):
        contact_type = mommy.make(ContactType)

        data = {
            "reg_no": "DEN/90/2000",
            "contacts": [
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                },
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                }
            ]
        }
        url = reverse("api:facilities:officer_facade_create")
        response = self.client.post(url, data)
        self.assertEquals(400, response.status_code)

    def test_post_officer_no_contacts(self):
        facility = mommy.make(Facility)
        job_title = mommy.make(JobTitle)

        data = {
            "facility_id": str(facility.id),
            "name": "Brenda Makena",
            "id_no": "545454545",
            "reg_no": "DEN/90/2000",
            "title": str(job_title.id)

        }
        url = reverse("api:facilities:officer_facade_create")
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(1, FacilityOfficer.objects.count())


class TestOptionGroupsView(LoginMixin, APITestCase):
    def setUp(self):
        super(TestOptionGroupsView, self).setUp()
        self.url = reverse("api:facilities:option_groups_list")

    def test_post(self):
        data = {
            "name": "Option group name"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, OptionGroup.objects.count())

    def test_listing(self):
        mommy.make(OptionGroup)
        mommy.make(OptionGroup)
        mommy.make(OptionGroup)
        mommy.make(OptionGroup)
        mommy.make(OptionGroup)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(5, response.data.get("count"))
        self.assertEquals(5, len(response.data.get("results")))

    def test_retrieving_a_single_record(self):
        mommy.make(OptionGroup)
        option_group = mommy.make(OptionGroup)
        url = self.url + "{}/".format(option_group.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(str(option_group.id), response.data.get("id"))

    def test_updating(self):
        option_group = mommy.make(OptionGroup)
        data = {
            "name": "editted"
        }
        url = self.url + "{}/".format(option_group.id)
        response = self.client.patch(url, data)
        option_group_refetched = OptionGroup.objects.get(id=option_group.id)
        self.assertEquals(200, response.status_code)
        self.assertEquals(option_group_refetched.name, data.get("name"))
