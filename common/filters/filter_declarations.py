from ..models import (
    ContactType, Contact, County, Constituency, Ward, UserCounties,
    PhysicalAddress, UserResidence, UserContact, Town)
from .filter_shared import CommonFieldsFilterset


class ContactTypeFilter(CommonFieldsFilterset):

    class Meta:
        model = ContactType


class ContactFilter(CommonFieldsFilterset):

    class Meta:
        model = Contact


class PhysicalAddressFilter(CommonFieldsFilterset):

    class Meta:
        model = PhysicalAddress


class CountyFilter(CommonFieldsFilterset):

    class Meta:
        model = County


class ConstituencyFilter(CommonFieldsFilterset):

    class Meta:
        model = Constituency


class WardFilter(CommonFieldsFilterset):

    class Meta:
        model = Ward


class UserCountiesFilter(CommonFieldsFilterset):
    class Meta:
        model = UserCounties


class UserResidenceFilter(CommonFieldsFilterset):
    class Meta:
        model = UserResidence


class UserContactFilter(CommonFieldsFilterset):
    class Meta:
        model = UserContact


class TownFilter(CommonFieldsFilterset):
    class Meta:
        model = Town
