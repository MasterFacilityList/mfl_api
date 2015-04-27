import django_filters
from datetime import timedelta

from django import forms
from django.utils.encoding import force_str
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from rest_framework import ISO_8601


class IsoDateTimeField(forms.DateTimeField):
    """
    It support 'iso-8601' date format too which is out the scope of
    the ``datetime.strptime`` standard library

    # ISO 8601: ``http://www.w3.org/TR/NOTE-datetime``
    """
    def strptime(self, value, format):
        value = force_str(value)
        if format == ISO_8601:
            parsed = parse_datetime(value)
            if parsed is None:  # Continue with other formats if doesn't match
                raise ValueError
            return parsed
        return super(IsoDateTimeField, self).strptime(value, format)


class IsoDateTimeFilter(django_filters.DateTimeFilter):
    """ Extend ``DateTimeFilter`` to filter by ISO 8601 formated dates too"""
    field_class = IsoDateTimeField


class TimeRangeFilter(django_filters.filters.Filter):
    """
    Filters a queryset based on the number of days needed. eg a week, a month
    or a quarter (3 months)

    It is a very naive implementation as it does not cater for the fact that
    months do not have equal number of days
    """

    def __init__(self, *args, **kwargs):
        self.alias = kwargs.get('alias')
        self.last_one_week = True if self.alias == 'last_one_week' else False
        self.last_one_quarter = True if self.alias == 'last_one_quarter' \
            else False
        self.last_one_month = True if self.alias == 'last_one_month' else False
        kwargs.pop('alias')
        super(TimeRangeFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        super(TimeRangeFilter, self).filter(qs, value)
        today = timezone.now()
        if self.last_one_week:
            week_start = today - timedelta(days=6)
            return qs.filter(created__gte=week_start, created__lte=today)
        if self.last_one_quarter:
            quarter_start = today - timedelta(days=90)
            return qs.filter(created__gte=quarter_start, created__lte=today)

        if self.last_one_month:
            month_start = today - timedelta(days=30)
            return qs.filter(created__gte=month_start, created__lte=today)

        return qs


class CommonFieldsFilterset(django_filters.FilterSet):
    """Every model that descends from AbstractBase should have this

    The usage pattern for this is presently simplistic; mix it in, then add to
    the `fields` in the filter's `Meta` `'updated', 'created',
    updated_before', 'created_before', 'updated_after', 'created_after'' and
    any other applicable / extra fields.

    When you inherit this, DO NOT add a `fields` declaration. Let the implicit
    filter fields ( every model field gets one ) stay in place.
    """
    updated_before = IsoDateTimeFilter(
        name='updated', lookup_type='lte',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))
    created_before = IsoDateTimeFilter(
        name='created', lookup_type='lte',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))

    updated_after = IsoDateTimeFilter(
        name='updated', lookup_type='gte',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))
    created_after = IsoDateTimeFilter(
        name='created', lookup_type='gte',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))

    updated_on = IsoDateTimeFilter(
        name='updated', lookup_type='exact',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))
    created_on = IsoDateTimeFilter(
        name='created', lookup_type='exact',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))

    is_deleted = django_filters.BooleanFilter(
        name='deleted', lookup_type='exact')
    is_active = django_filters.BooleanFilter(
        name='active', lookup_type='exact')
    last_one_week = TimeRangeFilter(
        name='created', alias='last_one_week')
    last_one_quarter = TimeRangeFilter(
        name='created', alias='last_one_quarter')
    last_one_month = TimeRangeFilter(
        name='created', alias='last_one_month')
