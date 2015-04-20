import django_filters

from common.filters.filter_shared import CommonFieldsFilterset
from ..models import (
    PracticeType,
    Speciality,
    Qualification,
    Practitioner,
    PractitionerQualification,
    PractitionerContact,
    PractitionerFacility
)


class PracticeTypeFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = PracticeType


class SpecialityFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    practice_type = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = Speciality


class QualificationFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Qualification


class PractitionerFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    registration_number = django_filters.CharFilter(lookup_type='exact')
    qualifications = django_filters.AllValuesFilter(lookup_type='icontains')
    contacts = django_filters.AllValuesFilter(lookup_type='icontains')
    ward = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = Practitioner


class PractitionerQualificationFilter(CommonFieldsFilterset):
    practitioner = django_filters.AllValuesFilter(lookup_type='exact')
    qualification = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = PractitionerQualification


class PractitionerContactFilter(CommonFieldsFilterset):
    practitioner = django_filters.AllValuesFilter(lookup_type='exact')
    contact = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = PractitionerContact


class PractitionerFacilityFilter(CommonFieldsFilterset):
    practitioner = django_filters.AllValuesFilter(lookup_type='exact')
    facility = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = PractitionerFacility
