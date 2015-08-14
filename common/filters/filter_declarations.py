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
    Town,
    UserConstituency,
    SubCounty

)
from .filter_shared import (
    CommonFieldsFilterset,
    ListCharFilter,
    ListIntegerFilter
)


class SubCountyFilter(CommonFieldsFilterset):
    class Meta(object):
        model = SubCounty


class UserConstituencyFilter(CommonFieldsFilterset):
    county = django_filters.CharFilter(
        lookup_type='exact', name='constituency__county')
    constituency = ListCharFilter(lookup_type='exact')

    class Meta(object):
        model = UserConstituency


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
    town = django_filters.CharFilter(lookup_type='exact')
    postal_code = django_filters.CharFilter(lookup_type='icontains')
    address = django_filters.CharFilter(lookup_type='icontains')
    nearest_landmark = django_filters.CharFilter(lookup_type='icontains')
    plot_number = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = PhysicalAddress


class CountyFilter(CommonFieldsFilterset):
    name = ListCharFilter(lookup_type='icontains')
    code = ListIntegerFilter(lookup_type='exact')
    county_id = ListCharFilter(name='id', lookup_type='icontains')

    class Meta(object):
        model = County


class ConstituencyFilter(CommonFieldsFilterset):
    name = ListCharFilter(lookup_type='icontains')
    code = ListIntegerFilter(lookup_type='exact')
    county = ListCharFilter(lookup_type='icontains')
    constituency_id = ListCharFilter(name='id', lookup_type='icontains')

    class Meta(object):
        model = Constituency


class WardFilter(CommonFieldsFilterset):
    ward_id = ListCharFilter(name='id', lookup_type='icontains')
    name = ListCharFilter(lookup_type='icontains')
    code = ListIntegerFilter(lookup_type='exact')
    constituency = ListCharFilter(lookup_type='icontains')
    county = ListCharFilter(
        lookup_type='exact', name='constituency__county')

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
