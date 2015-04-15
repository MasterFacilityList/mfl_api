import django_filters

from ..models import (
    ContactType, Contact, County, Constituency, Ward, UserCounties,
    PhysicalAddress, UserResidence, UserContact, Town)
from .filter_shared import CommonFieldsFilterset


class ContactTypeFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = ContactType


class ContactFilter(CommonFieldsFilterset):
    contact = django_filters.CharFilter(lookup_type='icontains')
    contact_type = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = Contact


class PhysicalAddressFilter(CommonFieldsFilterset):
    town = django_filters.AllValuesFilter(lookup_type='exact')
    postal_code = django_filters.CharFilter(lookup_type='icontains')
    address = django_filters.CharFilter(lookup_type='icontains')
    nearest_landmark = django_filters.CharFilter(lookup_type='icontains')
    plot_number = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = PhysicalAddress


class CountyFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.NumberFilter(lookup_type='exact')

    class Meta:
        model = County


class ConstituencyFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.NumberFilter(lookup_type='exact')

    class Meta:
        model = Constituency


class WardFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.NumberFilter(lookup_type='exact')

    class Meta:
        model = Ward


class UserCountiesFilter(CommonFieldsFilterset):
    user = django_filters.AllValuesFilter(lookup_type='exact')
    county = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = UserCounties


class UserResidenceFilter(CommonFieldsFilterset):
    user = django_filters.AllValuesFilter(lookup_type='exact')
    ward = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = UserResidence


class UserContactFilter(CommonFieldsFilterset):
    user = django_filters.AllValuesFilter(lookup_type='exact')
    contact = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = UserContact


class TownFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Town
