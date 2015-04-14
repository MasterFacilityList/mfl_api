import json

from datetime import timedelta
from django.utils.dateparse import parse_datetime
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import ISO_8601
from model_mommy import mommy

from ..filters.filter_shared import IsoDateTimeField
from ..models import County
from ..serializers import CountySerializer
from .test_models import BaseTestCase
from .test_views import LogginMixin, default


def _dict(ordered_dict_val):
    """A hack that converts pesky nested OrderedDicts to nice dicts"""
    return json.loads(json.dumps(ordered_dict_val, default=default))


class TestIsoDateTimeField(BaseTestCase):
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


class TestCommonFieldsFilterset(LogginMixin, BaseTestCase, APITestCase):
    def setUp(self):
        super(TestCommonFieldsFilterset, self).setUp()
        self.url = reverse('api:common:counties_list')
        self.boundary_date = timezone.now()
        self.date_after = self.boundary_date + timedelta(days=7)
        self.date_before = self.boundary_date - timedelta(days=7)
        self.maxDiff = None

    def test_updated_before_filter(self):
        pass

    def test_created_before_filter(self):
        pass

    def test_updated_after_filter(self):
        pass

    def test_created_after_filter(self):
        pass

    def test_updated_on_filter(self):
        pass

    def test_created_on_filter(self):
        pass

    def test_is_deleted_filter(self):
        pass

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
                    CountySerializer(active_county).data,
                    CountySerializer(inactive_county).data
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
