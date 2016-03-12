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
    SubCounty,
    DocumentUpload,
    ErrorQueue,
    UserSubCounty
)
from .filter_shared import (
    CommonFieldsFilterset,
    ListCharFilter,
    ListIntegerFilter
)


class UserSubCountyFilter(CommonFieldsFilterset):
    class Meta(object):
        model = UserSubCounty


class ErrorQueueFilter(django_filters.FilterSet):
    """
    ErrorQueue model does not descend from abtractbase thus the FilterSet.
    """

    class Meta(object):
        model = ErrorQueue


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
    county = ListCharFilter(lookup_type='exact')
    constituency_id = ListCharFilter(name='id', lookup_type='exact')

    class Meta(object):
        model = Constituency


class WardFilter(CommonFieldsFilterset):
    ward_id = ListCharFilter(name='id', lookup_type='exact')
    name = ListCharFilter(lookup_type='icontains')
    code = ListIntegerFilter(lookup_type='exact')
    constituency = ListCharFilter(lookup_type='exact')
    sub_county = ListCharFilter(lookup_type='exact')
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


class DocumentUploadFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = DocumentUpload
