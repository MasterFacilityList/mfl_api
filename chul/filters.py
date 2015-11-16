import django_filters
from django.db.models import Q
from distutils.util import strtobool


from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact,
    CHUService,
    CHURating,
    ChuUpdateBuffer
)


from common.filters.filter_shared import (
    CommonFieldsFilterset,
    ListCharFilter)

from common.constants import BOOLEAN_CHOICES, TRUTH_NESS


class ChuUpdateBufferFilter(CommonFieldsFilterset):

    class Meta(object):
        model = ChuUpdateBuffer


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

    def chu_pending_approval(self, value):
        if value in TRUTH_NESS:
            return self.filter(
                Q(is_approved=False, is_rejected=False, has_edits=False) |
                Q(is_approved=True, is_rejected=False, has_edits=True) |
                Q(is_approved=False, is_rejected=True, has_edits=True)
            )
        else:
            return self.filter(
                Q(is_approved=True, is_rejected=False, has_edits=False) |
                Q(is_approved=False, is_rejected=True, has_edits=False)
            )
    name = django_filters.CharFilter(lookup_type='icontains')
    ward = ListCharFilter(name='facility__ward')
    constituency = ListCharFilter(
        name='facility__ward__constituency')
    county = ListCharFilter(
        name='facility__ward__constituency__county')

    is_approved = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=strtobool
    )
    is_rejected = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=strtobool
    )
    has_edits = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=strtobool
    )
    pending_approval = django_filters.MethodFilter(
        action=chu_pending_approval)

    class Meta(object):
        model = CommunityHealthUnit


class CommunityHealthWorkerFilter(CommonFieldsFilterset):
    first_name = django_filters.CharFilter(lookup_type='icontains')
    last_name = django_filters.CharFilter(lookup_type='icontains')
    username = django_filters.CharFilter(lookup_type='icontains')
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
