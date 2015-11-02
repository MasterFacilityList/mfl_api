import json

from datetime import timedelta
from django.utils.dateparse import parse_datetime
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import ISO_8601
from model_mommy import mommy

from ..filters.filter_shared import IsoDateTimeField, NullFilter
from ..models import County, ContactType
from ..serializers import CountySerializer
from .test_views import LoginMixin, default


def _dict(ordered_dict_val):
    """A hack that converts pesky nested OrderedDicts to nice dicts"""
    return json.loads(json.dumps(ordered_dict_val, default=default))


class TestNullFilter(APITestCase):

    def test_null_filter(self):
        ContactType.objects.create(name="a", description="desc")
        ContactType.objects.create(name="b")

        nf = NullFilter(name='description')
        qs = nf.filter(ContactType.objects.all(), 'true')
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].name, "b")

        qs = nf.filter(ContactType.objects.all(), 'false')
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].name, "a")


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
            _dict(self.client.get(url_with_no_filter).data['results']),
            _dict([
                CountySerializer(
                    inactive_county,
                    context={
                        'request': {
                            "REQUEST_METHOD": "None"
                        }
                    }
                ).data,
                CountySerializer(
                    active_county,
                    context={
                        'request': {
                            "REQUEST_METHOD": "None"
                        }
                    }
                ).data
            ])
        )

        url_with_active_filter = self.url + '?is_active=True'
        self.assertEquals(
            _dict(self.client.get(url_with_active_filter).data['results']),
            _dict([
                CountySerializer(
                    active_county,
                    context={
                        'request': {
                            "REQUEST_METHOD": "None"
                        }
                    }
                ).data
            ])
        )

        url_with_inactive_filter = self.url + '?is_active=False'
        self.assertEquals(
            _dict(self.client.get(url_with_inactive_filter).data['results']),
            _dict([
                CountySerializer(
                    inactive_county,
                    context={
                        'request': {
                            "REQUEST_METHOD": "None"
                        }
                    }
                ).data
            ])
        )

    def test_is_deleted_filter(self):
        # Deleted is a special cookie;
        # AbstractBase overrides the default manager and filters out deleted
        # This covers overrides of the queryset ( using .everything )
        not_deleted_county = mommy.make(County, deleted=False)

        url_with_inactive_filter = self.url + '?is_deleted=False'
        self.assertEquals(
            _dict(self.client.get(url_with_inactive_filter).data['results']),
            _dict([
                CountySerializer(
                    not_deleted_county,
                    context={
                        'request': {
                            "REQUEST_METHOD": "None"
                        }
                    }
                ).data
            ])
        )
