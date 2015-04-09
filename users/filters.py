import django_filters
from .models import MFLUser, UserCounties


class MFLUserFilter(django_filters.FilterSet):
    class Meta:
        model = MFLUser


class UserCountyFilter(django_filters):
    class Meta:
        model = UserCounties
