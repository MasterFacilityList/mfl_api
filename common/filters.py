import django_filters

from .models import Contact, Constituency, Ward

from django import forms
from django.utils.encoding import force_str
from django.utils.dateparse import parse_datetime
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


class PreciseDateTimeField(IsoDateTimeField):
    """ Only support ISO 8601 """
    def __init__(self, *args, **kwargs):
        kwargs['input_formats'] = (ISO_8601, )
        super(PreciseDateTimeField, self).__init__(*args, **kwargs)


class IsoDateTimeFilter(django_filters.DateTimeFilter):
    """ Extend ``DateTimeFilter`` to filter by ISO 8601 formated dates too"""
    field_class = IsoDateTimeField


class PreciseDateTimeFilter(django_filters.DateTimeFilter):
    """ Extend ``DateTimeFilter`` to filter only by ISO 8601 formated dates """
    field_class = PreciseDateTimeField


class ContactFilter(django_filters.FilterSet):
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

    updated = IsoDateTimeFilter(
        name='updated', lookup_type='eq',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))
    created = IsoDateTimeFilter(
        name='created', lookup_type='eq',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))

    class Meta:
        model = Contact
        fields = (
            'updated', 'created',
            'updated_before', 'created_before',
            'updated_after', 'created_after',
        )


class ConstituencyFilter(django_filters.FilterSet):
    class Meta:
        model = Constituency


class WardFilter(django_filters.FilterSet):
    class Meta:
        model = Ward
