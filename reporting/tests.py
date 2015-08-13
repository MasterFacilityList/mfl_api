from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from facilities.models import Facility
from common.models import Ward, County, Constituency


class TestFacilityCountByCountyReport(APITestCase):
    def setUp(self):
        super(TestFacilityCountByCountyReport, self).setUp()

    def test_get_reports(self):
        mommy.make(Facility, _quantity=5)
        url = reverse("api:reporting:reports")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_reports_with_extra_filtering(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        mommy.make(Facility, ward=ward)
        mommy.make(Facility)
        mommy.make(Facility)
        mommy.make(Facility)
        url = reverse("api:reporting:reports")
        url = url + ("?report_type=facility_count_by_consituency"
                     "&filters=county={}".format(county.id))
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
