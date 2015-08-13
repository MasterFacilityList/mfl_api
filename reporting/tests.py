from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from facilities.models import Facility


class TestFacilityCountByCountyReport(APITestCase):
    def setUp(self):
        super(TestFacilityCountByCountyReport, self).setUp()

    def test_facility_count_per_county_report(self):
        mommy.make(Facility, _quantity=5)
        url = reverse("api:reporting:reports")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
