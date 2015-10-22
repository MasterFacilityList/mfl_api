from .models import AdminOffice, AdminOfficeContact

from common.filters import CommonFieldsFilterset


class AdminOfficeFilter(CommonFieldsFilterset):

    class Meta(object):
        model = AdminOffice


class AdminOfficeContactFilter(CommonFieldsFilterset):

    class Meta(object):
        model = AdminOfficeContact
