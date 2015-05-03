import json

from datetime import timedelta
from django.utils.dateparse import parse_datetime
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import ISO_8601
from model_mommy import mommy

from ..filters.filter_shared import IsoDateTimeField, TimeRangeFilter
from ..models import County
from ..serializers import CountySerializer
from .test_views import LoginMixin, default


def _dict(ordered_dict_val):
    """A hack that converts pesky nested OrderedDicts to nice dicts"""
    return json.loads(json.dumps(ordered_dict_val, default=default))


class TestIsoDateTimeField(LoginMixin, APITestCase):
    def test_strp_time_valid_iso_date(self):
        fl = IsoDateTimeField()
        valid_iso_date = '2015-04-14T06:46:32.709388Z'
        self.assertTrue(fl.strptime(valid_iso_date, ISO_8601))
        self.assertEquals(
            fl.strptime(value=valid_iso_date, format=ISO_8601),
            parse_datetime(valid_iso_date)
        )

    def test_strp_time_invalid_iso_date(self):
        fl = IsoDateTimeField()
        invalid_iso_date = 'random stuff'
        with self.assertRaises(ValueError):
            fl.strptime(value=invalid_iso_date, format=ISO_8601)

    def test_strp_time_fallback(self):
        fl = IsoDateTimeField()
        # Should fall back uneventfully
        fl.strptime(
            value='2006-10-25 14:30:59', format='%Y-%m-%d %H:%M:%S')


class TestCommonFieldsFilterset(LoginMixin, APITestCase):
    def setUp(self):
        super(TestCommonFieldsFilterset, self).setUp()
        self.url = reverse('api:common:counties_list')
        self.boundary_date = timezone.now()
        self.date_after = self.boundary_date + timedelta(days=7)
        self.date_before = self.boundary_date - timedelta(days=7)
        self.maxDiff = None

    def test_is_active_filter(self):
        active_county = mommy.make(County, active=True)
        inactive_county = mommy.make(County, active=False)

        url_with_no_filter = self.url
        self.assertEquals(
            _dict(self.client.get(url_with_no_filter).data),
            _dict({
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    CountySerializer(inactive_county).data,
                    CountySerializer(active_county).data
                ]
            })
        )

        url_with_active_filter = self.url + '?is_active=True'
        self.assertEquals(
            _dict(self.client.get(url_with_active_filter).data),
            _dict({
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    CountySerializer(active_county).data
                ]
            })
        )

        url_with_inactive_filter = self.url + '?is_active=False'
        self.assertEquals(
            _dict(self.client.get(url_with_inactive_filter).data),
            _dict({
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    CountySerializer(inactive_county).data
                ]
            })
        )

    def test_is_deleted_filter(self):
        # Deleted is a special cookie;
        # AbstractBase overrides the default manager and filters out deleted
        # This covers overrides of the queryset ( using .everything )
        not_deleted_county = mommy.make(County, deleted=False)

        url_with_inactive_filter = self.url + '?is_deleted=False'
        self.assertEquals(
            _dict(self.client.get(url_with_inactive_filter).data),
            _dict({
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    CountySerializer(not_deleted_county).data
                ]
            })
        )


class TestTimeRangeFilter(LoginMixin, APITestCase):
    def setUp(self):
        super(TestTimeRangeFilter, self).setUp()
        self.url = reverse('api:common:counties_list')

    def sanitize_time(self, date_obj):
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        return "{}-{}-{} 23:59:59.999999Z".format(year, month, day)

    def test_last_one_week(self):
        three_days_ago = timezone.now() - timedelta(days=3)
        last_month = timezone.now() - timedelta(days=34)
        county_1 = mommy.make(County, created=three_days_ago)
        mommy.make(County, created=last_month)
        url = self.url + "?last_one_week={}".format(
            self.sanitize_time(timezone.now()))
        response = self.client.get(url)
        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                CountySerializer(county_1).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            _dict(response.data),
            _dict(expected_data)
        )

    def test_last_one_week_days_closely_together(self):
        right_now = timezone.now()
        just_before_week_start = right_now - timedelta(days=8)
        week_start = right_now - timedelta(days=7)
        mid_week = right_now - timedelta(days=3)
        mommy.make(County, created=just_before_week_start)
        county_2 = mommy.make(County, created=week_start)
        county_3 = mommy.make(County, created=mid_week)
        county_4 = mommy.make(County, created=right_now)
        url = self.url + "?last_one_week={}".format(
            self.sanitize_time(timezone.now()))
        response = self.client.get(url)
        expected_data = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                CountySerializer(county_4).data,
                CountySerializer(county_3).data,
                CountySerializer(county_2).data
            ]
        }

        self.assertEquals(200, response.status_code)

        import pprint
        print('=' * 80)
        print(url)
        print('=' * 80)
        pprint.pprint(_dict(expected_data))
        print('=' * 80)
        pprint.pprint(_dict(response.data))
        print('=' * 80)

        self.assertEquals(
            _dict(response.data),
            _dict(expected_data)
        )

    def test_last_one_quater(self):
        seventy_days_ago = timezone.now() - timedelta(days=70)
        last_five_months = timezone.now() - timedelta(days=150)
        county_1 = mommy.make(County, created=seventy_days_ago)
        mommy.make(County, created=last_five_months)

        url = self.url + "?last_one_quarter={}".format(
            self.sanitize_time(timezone.now()))
        response = self.client.get(url)
        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                CountySerializer(county_1).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            _dict(response.data),
            _dict(expected_data)
        )

    def test_one_month(self):
        two_weeks_ago = timezone.now() - timedelta(days=14)
        last_two_months = timezone.now() - timedelta(days=40)
        county_1 = mommy.make(County, created=two_weeks_ago)
        mommy.make(County, created=last_two_months)

        url = self.url + "?last_one_month={}".format(
            self.sanitize_time(timezone.now()))
        response = self.client.get(url)
        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                CountySerializer(county_1).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            _dict(response.data),
            _dict(expected_data)
        )

    def test_no_filter(self):
        mommy.make(County)
        mommy.make(County)
        qs = County.objects.all()

        time_filter = TimeRangeFilter(name='created', alias='not_supported')
        result = time_filter.filter(qs, '2015-04-26T13:17:18.975021Z')
        self.assertEquals(result, qs)
