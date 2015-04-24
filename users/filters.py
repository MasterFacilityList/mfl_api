import django_filters

from .models import MflUser


class MFLUserFilter(django_filters.FilterSet):
    class Meta(object):
        model = MflUser
