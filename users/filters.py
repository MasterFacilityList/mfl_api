# import django_filters
from common.filters import CommonFieldsFilterset
from .models import MflUser


class MFLUserFilter(CommonFieldsFilterset):
    class Meta(object):
        model = MflUser
