import django_filters

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact
)

from common.filters.filter_shared import CommonFieldsFilterset


class CommunityHealthUnitFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    facility = django_filters.AllValuesFilter(lookup_type='icontains')

    class Meta:
        model = CommunityHealthUnit


class CommunityHealthWorkerFilter(CommonFieldsFilterset):
    first_name = django_filters.CharFilter(lookup_type='icontains')
    last_name = django_filters.CharFilter(lookup_type='icontains')
    username = django_filters.CharFilter(lookup_type='icontains')
    id_number = django_filters.CharFilter(lookup_type='exact')

    class Meta:
        model = CommunityHealthWorker


class CommunityHealthWorkerContactFilter(CommonFieldsFilterset):
    health_worker = django_filters.AllValuesFilter(lookup_type='icontains')
    contact = django_filters.AllValuesFilter(lookup_type='icontains')

    class Meta:
        model = CommunityHealthWorkerContact
