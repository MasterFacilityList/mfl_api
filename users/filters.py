import django_filters

from django.contrib.auth.models import Permission
from common.filters import CommonFieldsFilterset
from .models import MflUser


class MFLUserFilter(CommonFieldsFilterset):
    class Meta(object):
        model = MflUser


class PermissionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = Permission
