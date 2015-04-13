import django_filters
from .models import MflUser, UserCounties


class MFLUserFilter(django_filters.FilterSet):
    class Meta:
        model = MflUser


class UserCountiesFilter(django_filters.FilterSet):
    class Meta:
        model = UserCounties
