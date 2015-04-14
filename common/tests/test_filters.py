from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime

from rest_framework.test import APITestCase
from rest_framework import ISO_8601
from model_mommy import mommy

from ..filters.filter_shared import IsoDateTimeField
from .test_models import BaseTestCase


class LogginMixin(object):

    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.client.force_authenticate(user=self.user)
        super(LogginMixin, self).setUp()


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
