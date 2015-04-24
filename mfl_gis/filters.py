import django_filters

from .models import (
    GeoCodeSource,
    GeoCodeMethod,
    FacilityCoordinates
)

from common.filters.filter_shared import CommonFieldsFilterset


class GeoCodeSourceFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    abbreviation = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = GeoCodeSource


class GeoCodeMethodFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = GeoCodeMethod


class FacilityCoordinatesFilter(CommonFieldsFilterset):

    class Meta(object):
        model = FacilityCoordinates
