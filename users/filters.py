import django_filters

from common.models import UserCounties
from .models import MflUser


class MFLUserFilter(django_filters.FilterSet):
    class Meta:
        model = MflUser


class UserCountiesFilter(django_filters.FilterSet):
    class Meta:
        model = UserCounties
