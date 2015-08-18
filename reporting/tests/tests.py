from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from facilities.models import (
    Facility, FacilityType, KephLevel, FacilityUpgrade)
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

    def test_get_facility_by_facility_types(self):
        f_type = mommy.make(FacilityType)
        f_type_2 = mommy.make(FacilityType)
        mommy.make(Facility, facility_type=f_type)
        mommy.make(Facility, facility_type=f_type_2)
        url = reverse("api:reporting:reports")
        url = url + "?report_type=facility_count_by_facility_type_detailed"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_facility_by_constituencies(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        mommy.make(Facility, ward=ward)
        mommy.make(Facility)
        mommy.make(Facility)
        mommy.make(Facility)
        url = reverse("api:reporting:reports")
        url = url + "?report_type=facility_constituency_report"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_facility_by_keph_level(self):
        keph_level_1 = mommy.make(KephLevel)
        keph_level_2 = mommy.make(KephLevel)
        mommy.make(Facility, keph_level=keph_level_1)
        mommy.make(Facility, keph_level=keph_level_2)
        url = reverse("api:reporting:reports")
        url = url + "?report_type=facility_keph_level_report"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_upgrade_downgrade_report(self):
        url = reverse("api:reporting:upgrade_downgrade_report")
        mommy.make(FacilityUpgrade, _quantity=5)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
