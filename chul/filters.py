import django_filters

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact
)

from common.filters.filter_shared import CommonFieldsFilterset


class CommunityHealthUnit(CommonFieldsFilterset):
    name = django_filters.CharFieldFilter(look_type='icontains')
    facility = django_filters.AllValuesFilter(look_type='icontains')

    class Meta:
        model = CommunityHealthUnit



class CommunityHealthWorkerFilter(CommonFieldsFilterset):
    first_name = django_filters.CharFieldFilter(look_type='icontains')
    last_name = django_filters.CharFieldFilter(look_type='icontains')
    username = django_filters.CharFieldFilter(look_type='icontains')

    class Meta:
        model = CommunityHealthWorker


class CommunityHealthWorkerContact(CommonFieldsFilterset):
    health_worker = django_filters.AllValuesFilter(lookup_type='icontains')
    contact = django_filters.AllValuesFilter(lookup_type='icontains')

    class Meta:
        model = CommunityHealthWorkerContact

