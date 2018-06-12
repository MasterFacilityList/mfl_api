from datetime import timedelta

from django.utils import timezone

from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from facilities.models import (
    Facility,)

from chul.models import CommunityHealthUnit
from common.tests.test_views import LoginMixin


class TestFacilityCountByCountyReport(LoginMixin, APITestCase):

    def setUp(self):
        super(TestFacilityCountByCountyReport, self).setUp()

    def test_get_county_reports(self):
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        mommy.make(CommunityHealthUnit, facility=facility)
        mommy.make(CommunityHealthUnit, facility=facility_2)
        url = reverse("api:reporting:chul_reports")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('total'))
        data = {
            "total": 2,
            "results": [
                {
                    "county_name": facility_2.ward.constituency.county.name,
                    "county_id": facility_2.ward.constituency.county.id,
                    "number_of_units": 1
                },
                {
                    "county_name": facility.ward.constituency.county.name,
                    "county_id": facility.ward.constituency.county.id,
                    "number_of_units": 1
                }

            ]

        }
        self.assertEquals(data, response.data)

    def test_constituency_reports(self):
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        mommy.make(CommunityHealthUnit, facility=facility)
        mommy.make(CommunityHealthUnit, facility=facility_2)
        url = reverse("api:reporting:chul_reports")
        url = url + "?report_type=constituency"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('total'))
        data = {
            "total": 2,
            "results": [
                {
                    "constituency_name": facility_2.ward.constituency.name,
                    "constituency_id": facility_2.ward.constituency.id,
                    "number_of_units": 1
                },
                {
                    "constituency_name": facility.ward.constituency.name,
                    "constituency_id": facility.ward.constituency.id,
                    "number_of_units": 1
                }

            ]

        }
        self.assertEquals(data, response.data)

        # test filter consituency report by county
        county = str(facility.ward.constituency.county.id)
        # url = url + "?report_type=constituency&county={}".format(county)
        url = reverse("api:reporting:chul_reports")
        url = url + "?county={}&report_type=constituency".format(county)

        response_2 = self.client.get(url)
        self.assertEquals(1, response_2.data.get('total'))

    def test_ward_reports(self):
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        mommy.make(CommunityHealthUnit, facility=facility)
        mommy.make(CommunityHealthUnit, facility=facility_2)
        ward_url = reverse("api:reporting:chul_reports")
        url = ward_url + "?report_type=ward"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('total'))
        data = {
            "total": 2,
            "results": [

                {
                    "ward_name": facility_2.ward.name,
                    "ward_id": facility_2.ward.id,
                    "number_of_units": 1
                },
                {
                    "ward_name": facility.ward.name,
                    "ward_id": facility.ward.id,
                    "number_of_units": 1
                }
            ]

        }
        self.assertEquals(data, response.data)
        constituency = facility.ward.constituency.id
        url = url + "&constituency={}".format(constituency)
        response_2 = self.client.get(url)
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(1, response_2.data.get('total'))

    def test_last_quater_report(self):
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        mommy.make(CommunityHealthUnit, facility=facility)
        long_ago = timezone.now() - timedelta(days=417)
        mommy.make(CommunityHealthUnit, facility=facility_2, created=long_ago)
        report_url = reverse("api:reporting:chul_reports")
        last_quarter_url = report_url + "?last_quarter=true"
        response = self.client.get(last_quarter_url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('total'))
        data = {
            "total": 1,
            "results": [
                {
                    "county_name": facility_2.ward.constituency.county.name,
                    "county_id": facility_2.ward.constituency.county.id,
                    "number_of_units": 0
                },
                {
                    "county_name": facility.ward.constituency.county.name,
                    "county_id": facility.ward.constituency.county.id,
                    "number_of_units": 1
                }
            ]

        }
        self.assertEquals(data, response.data)
        county_url = last_quarter_url + "&county={}".format(
            facility.ward.constituency.county.id)
        response_2 = self.client.get(county_url)
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(1, response.data.get('total'))

        const_url = last_quarter_url + "&constituency={}".format(
            facility.ward.constituency.id)
        response_2 = self.client.get(const_url)
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(1, response.data.get('total'))

    def test_status_report(self):
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        chu_1 = mommy.make(CommunityHealthUnit, facility=facility)
        chu_2 = mommy.make(CommunityHealthUnit, facility=facility_2)
        status_url = reverse("api:reporting:chul_reports")
        report_url = status_url + "?report_type=status"
        response = self.client.get(report_url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('total'))
        data = {
            "total": 2,
            "results": [
                {
                    "status_name": chu_2.status.name,
                    "number_of_units": 1
                },
                {
                    "status_name": chu_1.status.name,
                    "number_of_units": 1
                }
            ]

        }
        self.assertEquals(data, response.data)
        url = report_url + '&county={}'.format(
            facility.ward.constituency.county.id)
        response_2 = self.client.get(url)
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(1, response_2.data.get('total'))

        url = report_url + '&constituency={}'.format(
            facility.ward.constituency.id)
        response_2 = self.client.get(url)
        self.assertEquals(200, response_2.status_code)
        self.assertEquals(1, response_2.data.get('total'))
