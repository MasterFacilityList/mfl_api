from datetime import timedelta

from django.utils import timezone

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

    def test_get_undefined_report(self):
        mommy.make(Facility, _quantity=5)
        url = reverse("api:reporting:reports")
        response = self.client.get(url+"?report_type=hakuna_kitu")
        self.assertEquals(404, response.status_code)

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
        facility_upgrade = mommy.make(
            FacilityUpgrade, keph_level=keph_level, facility=facility)
        county_1 = mommy.make(County)
        constituency_1 = mommy.make(Constituency, county=county_1)
        ward_1 = mommy.make(Ward, constituency=constituency_1)
        facility_1 = mommy.make(Facility, ward=ward_1, keph_level=keph_level)
        facility_upgrade_2 = mommy.make(
            FacilityUpgrade, keph_level=keph_level, facility=facility_1)

        url = main_url + "?county={}".format(county.id)
        expected_data = {
            "total_facilities_changed": 1,
            "results": [
                {
                    "name": facility.name,
                    "code": facility.code,
                    "current_keph_level":
                    facility_upgrade.facility.keph_level.name,
                    "previous_keph_level":
                        facility_upgrade.current_keph_level_name,
                    "previous_facility_type":
                        facility_upgrade.current_facility_type_name,
                    "current_facility_type":
                        facility_upgrade.facility_type.name,
                    "reason": facility_upgrade.reason.reason
                }
            ]
        }
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(expected_data, response.data)

        url = main_url + "?county={}".format(county_1.id)
        expected_data_2 = {
            "total_facilities_changed": 1,
            "results": [
                {
                    "name": facility_1.name,
                    "code": facility_1.code,
                    "current_keph_level": facility_upgrade_2.keph_level.name,
                    "previous_keph_level":
                        facility_upgrade_2.current_keph_level_name,
                    "previous_facility_type":
                        facility_upgrade_2.current_facility_type_name,
                    "current_facility_type":
                        facility_upgrade_2.facility_type.name,
                    "reason": facility_upgrade_2.reason.reason
                }
            ]
        }
        response_2 = self.client.get(url)
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(expected_data_2, response_2.data)

    def test_facility_upgrade_downgrade_report_filter_by_upgrade(self):
        keph_level = mommy.make(KephLevel)
        keph_level_1 = mommy.make(KephLevel)
        facility = mommy.make(Facility, keph_level=keph_level)
        facility_2 = mommy.make(Facility, keph_level=keph_level_1)
        facility_3 = mommy.make(Facility, keph_level=keph_level_1)
        mommy.make(FacilityUpgrade, facility=facility, is_upgrade=True)
        mommy.make(FacilityUpgrade, facility=facility_2, is_upgrade=True)
        mommy.make(FacilityUpgrade, facility=facility_3, is_upgrade=False)

        url = reverse("api:reporting:upgrade_downgrade_report")

        upgrade_url = url + "?upgrade=true"
        response = self.client.get(upgrade_url)
        self.assertEquals(2, response.data.get("total_number_of_changes"))

        downgrade_url = url + "?upgrade=false"
        response = self.client.get(downgrade_url)
        self.assertEquals(1, response.data.get("total_number_of_changes"))

    def test_facility_upgrade_downgrade_report_filter_by_dates(self):
        keph_level = mommy.make(KephLevel)
        keph_level_1 = mommy.make(KephLevel)
        facility = mommy.make(Facility, keph_level=keph_level)
        facility_2 = mommy.make(Facility, keph_level=keph_level_1)
        facility_3 = mommy.make(Facility, keph_level=keph_level_1)
        facility_4 = mommy.make(Facility, keph_level=keph_level_1)

        within_this_week = timezone.now() - timedelta(days=5)
        within_this_month = timezone.now() - timedelta(days=20)
        within_last_three_months = timezone.now() - timedelta(days=80)
        long_ago = timezone.now() - timedelta(days=1000)

        mommy.make(
            FacilityUpgrade, facility=facility, created=within_this_week)
        mommy.make(
            FacilityUpgrade, facility=facility_2,
            created=within_this_month)
        mommy.make(
            FacilityUpgrade, facility=facility_3,
            created=within_last_three_months)
        mommy.make(
            FacilityUpgrade, facility=facility_4,
            created=long_ago)

        url = reverse("api:reporting:upgrade_downgrade_report")

        this_week_url = url + "?last_week=true"
        response = self.client.get(this_week_url)
        self.assertEquals(1, response.data.get("total_number_of_changes"))

        this_month_url = url + "?last_month=true"
        response = self.client.get(this_month_url)
        self.assertEquals(2, response.data.get("total_number_of_changes"))

        last_3_months_url = url + "?last_three_months=true"
        response = self.client.get(last_3_months_url)
        self.assertEquals(3, response.data.get("total_number_of_changes"))

        # all changes
        response = self.client.get(url)
        self.assertEquals(4, response.data.get("total_number_of_changes"))


class TestBedsAndCots(LoginMixin, APITestCase):

    def setUp(self):
        super(TestBedsAndCots, self).setUp()
        self.base_url = reverse("api:reporting:reports")
        self.coun1 = mommy.make(County)
        self.coun2 = mommy.make(County)
        self.coun3 = mommy.make(County)

        self.cons1 = mommy.make(Constituency, county=self.coun1)
        self.cons2 = mommy.make(Constituency, county=self.coun1)
        self.cons3 = mommy.make(Constituency, county=self.coun2)

        self.ward1 = mommy.make(Ward, constituency=self.cons1)
        self.ward2 = mommy.make(Ward, constituency=self.cons1)
        self.ward3 = mommy.make(Ward, constituency=self.cons2)

        mommy.make(
            Facility, ward=self.ward1, number_of_cots=2, number_of_beds=5,
            _quantity=2
        )
        mommy.make(Facility, ward=self.ward1)

        mommy.make(
            Facility, ward=self.ward2, number_of_cots=2, number_of_beds=5
        )
        mommy.make(
            Facility, _quantity=3, number_of_beds=2, number_of_cots=4,
            ward=self.ward3
        )

    def test_beds_and_cots_without_filter(self):
        params = [
            "beds_and_cots_by_county", "beds_and_cots_by_constituency",
            "beds_and_cots_by_ward"
        ]
        for i in params:
            response = self.client.get("{}?report_type={}".format(
                self.base_url, i
            ))
            self.assertEquals(200, response.status_code)

    def test_constituency_with_county_filter(self):
        response = self.client.get("{}?report_type={}&county={}".format(
            self.base_url, "beds_and_cots_by_constituency", str(self.coun1.pk)
        ))
        self.assertEquals(200, response.status_code)

    def test_constituency_with_county_filter_empty_county(self):
        response = self.client.get("{}?report_type={}&county={}".format(
            self.base_url, "beds_and_cots_by_constituency", str(self.coun3.pk)
        ))
        self.assertEquals(200, response.status_code)

    def test_ward_with_constituency_filter(self):
        response = self.client.get("{}?report_type={}&constituency={}".format(
            self.base_url, "beds_and_cots_by_ward", str(self.cons1.pk)
        ))
        self.assertEquals(200, response.status_code)

    def test_ward_with_constituency_filter_empty_constituency(self):
        response = self.client.get("{}?report_type={}&constituency={}".format(
            self.base_url, "beds_and_cots_by_ward", str(self.cons3.pk)
        ))
        self.assertEquals(200, response.status_code)
