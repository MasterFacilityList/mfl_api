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

from common.filters.filter_shared import (
    CommonFieldsFilterset,
    ListCharFilter
)


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
    name = ListCharFilter(lookup_type='icontains')
    code = ListCharFilter(lookup_type='icontains')

    class Meta(object):
        model = WorldBorder


class CountyBoundaryFilter(CommonFieldsFilterset):
    id = ListCharFilter(lookup_type='icontains')
    name = ListCharFilter(lookup_type='icontains')
    code = ListCharFilter(lookup_type='icontains')
    area = ListCharFilter(lookup_type='icontains')

    class Meta(object):
        model = CountyBoundary


class ConstituencyBoundaryFilter(CommonFieldsFilterset):
    id = ListCharFilter(lookup_type='icontains')
    name = ListCharFilter(lookup_type='icontains')
    code = ListCharFilter(lookup_type='icontains')
    area = ListCharFilter(lookup_type='icontains')

    class Meta(object):
        model = ConstituencyBoundary


class WardBoundaryFilter(CommonFieldsFilterset):
    id = ListCharFilter(lookup_type='icontains')
    name = ListCharFilter(lookup_type='icontains')
    code = ListCharFilter(lookup_type='icontains')
    area = ListCharFilter(lookup_type='icontains')

    class Meta(object):
        model = WardBoundary
