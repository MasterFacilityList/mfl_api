from ..models import ContactType, Contact, Constituency, Ward, UserCounties
from .filter_shared import CommonFieldsFilterset


class ContactTypeFilter(CommonFieldsFilterset):

    class Meta:
        model = ContactType


class ContactFilter(CommonFieldsFilterset):

    class Meta:
        model = Contact


class ConstituencyFilter(CommonFieldsFilterset):

    class Meta:
        model = Constituency


class WardFilter(CommonFieldsFilterset):

    class Meta:
        model = Ward


class UserCountiesFilter(CommonFieldsFilterset):
    class Meta:
        model = UserCounties
