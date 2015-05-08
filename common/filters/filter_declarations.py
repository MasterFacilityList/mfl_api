import django_filters

from ..models import (
    ContactType,
    Contact,
    County,
    Constituency,
    Ward,
    UserCounty,
    PhysicalAddress,
    UserContact,
    Town
)
from .filter_shared import (
    CommonFieldsFilterset,
    ListCharFilter,
    ListIntegerFilter
)


class ContactTypeFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = ContactType


class ContactFilter(CommonFieldsFilterset):
    contact = django_filters.CharFilter(lookup_type='icontains')
    contact_type = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = Contact


class PhysicalAddressFilter(CommonFieldsFilterset):
    town = django_filters.AllValuesFilter(lookup_type='exact')
    postal_code = django_filters.CharFilter(lookup_type='icontains')
    address = django_filters.CharFilter(lookup_type='icontains')
    nearest_landmark = django_filters.CharFilter(lookup_type='icontains')
    plot_number = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = PhysicalAddress


class CountyFilter(CommonFieldsFilterset):
    name = ListCharFilter(lookup_type='icontains')
    code = ListIntegerFilter(lookup_type='exact')

    class Meta(object):
        model = County


class ConstituencyFilter(CommonFieldsFilterset):
    name = ListCharFilter(lookup_type='icontains')
    code = ListIntegerFilter(lookup_type='exact')

    class Meta(object):
        model = Constituency


class WardFilter(CommonFieldsFilterset):
    name = ListCharFilter(lookup_type='icontains')
    code = ListIntegerFilter(lookup_type='exact')

    class Meta(object):
        model = Ward


class UserCountyFilter(CommonFieldsFilterset):
    user = django_filters.AllValuesFilter(lookup_type='exact')
    county = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = UserCounty


class UserContactFilter(CommonFieldsFilterset):
    user = django_filters.AllValuesFilter(lookup_type='exact')
    contact = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = UserContact


class TownFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = Town
