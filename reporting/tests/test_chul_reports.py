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

    def test_ward_reports(self):
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        mommy.make(CommunityHealthUnit, facility=facility)
        mommy.make(CommunityHealthUnit, facility=facility_2)
        url = reverse("api:reporting:chul_reports")
        url = url + "?report_type=ward"
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

    def test_last_quater_report(self):
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        mommy.make(CommunityHealthUnit, facility=facility)
        long_ago = timezone.now() - timedelta(days=417)
        mommy.make(CommunityHealthUnit, facility=facility_2, created=long_ago)
        url = reverse("api:reporting:chul_reports")
        url = url + "?last_quarter=true"
        response = self.client.get(url)
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
