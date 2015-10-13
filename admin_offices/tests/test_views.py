from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from model_mommy import mommy

from facilities.models import JobTitle
from common.models import County
from common.tests.test_views import LoginMixin

from ..models import AdminOffice, AdminOfficeContact


class TestAdminOfficeView(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:admin_offices:admin_offices_list")
        super(TestAdminOfficeView, self).setUp()

    def test_list(self):
        mommy.make(AdminOffice)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

    def test_get_single(self):
        admin_office = mommy.make(AdminOffice)
        admin_office_url = self.url + "{}/".format(admin_office.id)
        response = self.client.get(admin_office_url)
        self.assertEquals(200, response.status_code)

    def test_post(self):
        county = mommy.make(County)
        job_title = mommy.make(JobTitle)
        data = {
            "county": str(county.id),
            "job_title": str(job_title.id),
            "first_name": "jina",
            "last_name": "Nyingine"

        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, AdminOffice.objects.count())

    def test_patch(self):
        admin_office = mommy.make(AdminOffice)
        county_name = "Kaunti"
        county = mommy.make(County, name=county_name)
        admin_office_url = self.url + "{}/".format(admin_office.id)
        data = {
            "county": str(county.id)
        }
        response = self.client.patch(admin_office_url, data)
        self.assertEquals(200, response.status_code)
        admin_office_refetched = AdminOffice.objects.get(
            id=admin_office.id)
        self.assertEquals(county_name, admin_office_refetched.county.name)
        self.assertEquals(1, AdminOffice.objects.count())


class TestAdminOfficeContact(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:admin_offices:admin_office_contacts_list")
        super(TestAdminOfficeContact, self).setUp()

    def test_list(self):
        mommy.make(AdminOfficeContact)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
