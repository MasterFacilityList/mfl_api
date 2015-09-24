import django_filters

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact,
    CHUService,
    CHURating
)

from common.filters.filter_shared import CommonFieldsFilterset


class CHUServiceFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = CHUService


class StatusFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = Status


class CommunityHealthUnitContactFilter(CommonFieldsFilterset):
    health_unit = django_filters.AllValuesFilter(lookup_type='exact')
    contact = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = CommunityHealthUnitContact


class CommunityHealthUnitFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    ward = django_filters.CharFilter(name='community__ward')
    constituency = django_filters.CharFilter(
        name='community_ward__constituency')
    county = django_filters.CharFilter(
        name='community__ward__constituency__county')

    class Meta(object):
        model = CommunityHealthUnit


class CommunityHealthWorkerFilter(CommonFieldsFilterset):
    first_name = django_filters.CharFilter(lookup_type='icontains')
    last_name = django_filters.CharFilter(lookup_type='icontains')
    username = django_filters.CharFilter(lookup_type='icontains')
    id_number = django_filters.CharFilter(lookup_type='exact')
    ward = django_filters.CharFilter(name='health_unit__community__ward')
    constituency = django_filters.CharFilter(
        name='health_unit__community_ward__constituency')
    county = django_filters.CharFilter(
        name='health_unit__community__ward__constituency__county')

    class Meta(object):
        model = CommunityHealthWorker


class CommunityHealthWorkerContactFilter(CommonFieldsFilterset):
    health_worker = django_filters.AllValuesFilter(lookup_type='exact')
    contact = django_filters.AllValuesFilter(lookup_type='icontains')

    class Meta(object):
        model = CommunityHealthWorkerContact


class CHURatingFilter(CommonFieldsFilterset):
    chu = django_filters.AllValuesFilter(lookup_type='exact')
    rating = django_filters.NumberFilter(lookup_type='exact')

    class Meta(object):
        model = CHURating
