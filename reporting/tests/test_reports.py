from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from facilities.models import (
    Facility, FacilityType, KephLevel, FacilityUpgrade)
from common.models import Ward, County, Constituency
from common.tests.test_views import LoginMixin


class TestFacilityCountByCountyReport(LoginMixin, APITestCase):
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
        keph_level = mommy.make(KephLevel)
        facility = mommy.make(Facility, keph_level=keph_level)
        mommy.make(FacilityUpgrade, facility=facility)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_upgrade_downgrade_report_by_county(self):
        main_url = reverse("api:reporting:upgrade_downgrade_report")
        keph_level = mommy.make(KephLevel)
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        facility = mommy.make(Facility, ward=ward, keph_level=keph_level)
        facility_upgrade = mommy.make(FacilityUpgrade, facility=facility)

        county_1 = mommy.make(County)
        constituency_1 = mommy.make(Constituency, county=county_1)
        ward_1 = mommy.make(Ward, constituency=constituency_1)
        facility_1 = mommy.make(Facility, ward=ward_1, keph_level=keph_level)
        facility_upgrade_2 = mommy.make(FacilityUpgrade, facility=facility_1)

        url = main_url + "?county={}".format(county.id)
        expected_data = {
            "total_facilities_changed": 1,
            "facilities": [
                {
                    "name": facility.name,
                    "code": facility.code,
                    "current_keph_level": facility_upgrade.keph_level,
                    "previous_keph_level":
                        facility_upgrade.current_keph_level_name,
                    "previous_facility_type":
                        facility_upgrade.current_facility_type_name,
                    "current_facility_type":
                        facility_upgrade.current_facility_type_name
                }
            ]
        }
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(expected_data, response.data)

        url = main_url + "?county={}".format(county_1.id)
        expected_data_2 = {
            "total_facilities_changed": 1,
            "facilities": [
                {
                    "name": facility_1.name,
                    "code": facility_1.code,
                    "current_keph_level": facility_upgrade_2.keph_level,
                    "previous_keph_level":
                        facility_upgrade_2.current_keph_level_name,
                    "previous_facility_type":
                        facility_upgrade_2.current_facility_type_name,
                    "current_facility_type":
                        facility_upgrade_2.current_facility_type_name
                }
            ]
        }
        response_2 = self.client.get(url)
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(expected_data_2, response_2.data)
