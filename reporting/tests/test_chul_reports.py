from datetime import timedelta

from django.utils import timezone

from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from facilities.models import (
    Facility,)
from common.models import Ward, County, Constituency
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
        url = reverse("api:reporting:reports:chul_reports")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('total'))
        data = {
            "total": 2,
            "results": [
                {
                    "county_name": facility.ward.constituency.county.name,
                    "county_id": str(facility.ward.constituency.county.id),
                    "number_of_units": 1
                },
                {
                    "county_name": facility_2.ward.constituency.county.name,
                    "county_id": str(facility_2.ward.constituency.county.id),
                    "number_of_units": 1
                }
            ]

        }
        self.assertEquals(data, response.data)

    def test_constituency_reports(self):
        pass
