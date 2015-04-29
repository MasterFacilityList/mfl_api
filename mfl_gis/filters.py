import django_filters

from .models import (
    GeoCodeSource,
    GeoCodeMethod,
    FacilityCoordinates,
    WorldBorder,
    CountyBoundary,
    ConstituencyBoundary,
    WardBoundary
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


class WorldBorderFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = WorldBorder


class CountyBoundaryFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.CharFilter(lookup_type='icontains')
    area = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = CountyBoundary


class ConstituencyBoundaryFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.CharFilter(lookup_type='icontains')
    area = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = ConstituencyBoundary


class WardBoundaryFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.CharFilter(lookup_type='icontains')
    area = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = WardBoundary
