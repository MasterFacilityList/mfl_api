import django_filters

from django.contrib.auth.models import Permission, Group
from common.filters import CommonFieldsFilterset
from common.constants import TRUTH_NESS
from .models import MflUser, ProxyGroup, CustomGroup


class MFLUserFilter(CommonFieldsFilterset):
    class Meta(object):
        model = MflUser


class PermissionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = Permission


class GroupFilter(django_filters.FilterSet):

    def get_by_name(self, value):
        return Group.objects.filter(name__icontains=value)

    def get_county_level(self, value):
        if value in TRUTH_NESS:
            cgs = [cg.group.id for cg in CustomGroup.objects.filter(
                county_level=True)]
        else:
            cgs = [cg.group.id for cg in CustomGroup.objects.filter(
                county_level=False)]
        return Group.objects.filter(id__in=cgs)

    def get_national_level(self, value):
        if value in TRUTH_NESS:
            cgs = [cg.group.id for cg in CustomGroup.objects.filter(
                national=True)]
        else:
            cgs = [cg.group.id for cg in CustomGroup.objects.filter(
                national=False)]
        return Group.objects.filter(id__in=cgs)

    def get_sub_county_level(self, value):
        if value in TRUTH_NESS:
            cgs = [cg.group.id for cg in CustomGroup.objects.filter(
                sub_county_level=True)]
        else:
            cgs = [cg.group.id for cg in CustomGroup.objects.filter(
                sub_county_level=False)]
        return Group.objects.filter(id__in=cgs)

    def get_regulator(self, value):
        if value in TRUTH_NESS:
            cgs = [cg.group.id for cg in CustomGroup.objects.filter(
                regulator=True)]
        else:
            cgs = [cg.group.id for cg in CustomGroup.objects.filter(
                regulator=False)]
        return Group.objects.filter(id__in=cgs)

    name = django_filters.MethodFilter(action=get_by_name)
    is_county_level = django_filters.MethodFilter(action=get_county_level)
    is_national_level = django_filters.MethodFilter(action=get_national_level)
    is_sub_county_level = django_filters.MethodFilter(
        action=get_sub_county_level)
    is_regulator = django_filters.MethodFilter(action=get_regulator)

    class Meta(object):
        model = ProxyGroup
