import django_filters

from ..models import (
    Owner,
    Facility,
    FacilityCoordinates,
    JobTitle,
    FacilityUnit,
    FacilityStatus,
    Officer,
    RegulatingBody,
    GeoCodeSource,
    OwnerType,
    OfficerContact,
    GeoCodeMethod,
    FacilityContact,
    FacilityRegulationStatus,
    FacilityType,
    RegulationStatus,
    ServiceCategory,
    Option,
    Service,
    FacilityService,
    ServiceOption,
    ServiceRating
)
from common.filters.filter_shared import CommonFieldsFilterset


class ServiceRatingFilter(CommonFieldsFilterset):
    facility_service = django_filters.AllValuesFilter(lookup_type='exact')
    cleanliness = django_filters.BooleanFilter(lookup_type='exact')
    attitude = django_filters.BooleanFilter(lookup_type='exact')
    will_return = django_filters.BooleanFilter(lookup_type='exact')
    occupation = django_filters.CharFilter(lookup_type='icontains')
    comment = django_filters.CharFilter(lookup_type='icontains')
    service = django_filters.AllValuesFilter(
        name='facility_service__service', lookup_type='exact')
    facility = django_filters.AllValuesFilter(
        name='facility_service__facility', lookup_type='exact')

    class Meta:
        model = ServiceRating


class ServiceCategoryFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = ServiceCategory


class OptionFilter(CommonFieldsFilterset):
    value = django_filters.CharFilter(lookup_type='icontains')
    display_text = django_filters.CharFilter(lookup_type='icontains')
    option_type = django_filters.CharFilter(lookup_type='icontains')
    is_exclusive_option = django_filters.BooleanFilter(lookup_type='exact')

    class Meta:
        model = Option


class ServiceFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    category = django_filters.AllValuesFilter(lookup_type='exact')
    code = django_filters.CharFilter(lookup_type='exact')

    class Meta:
        model = Service


class FacilityServiceFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    selected_option = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = FacilityService


class ServiceOptionFilter(CommonFieldsFilterset):
    service = django_filters.AllValuesFilter(lookup_type='exact')
    option = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = ServiceOption


class OwnerTypeFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = OwnerType


class OwnerFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    abbreviation = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.NumberFilter(lookup_type='exact')
    owner_type = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = Owner


class JobTitleFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = JobTitle


class OfficerContactFilter(CommonFieldsFilterset):
    officer = django_filters.AllValuesFilter(lookup_type='icontains')
    contact = django_filters.AllValuesFilter(lookup_type='icontains')

    class Meta:
        model = OfficerContact


class OfficerFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    registration_number = django_filters.CharFilter(lookup_type='icontains')
    job_title = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = Officer


class FacilityStatusFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = FacilityStatus


class FacilityTypeFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    sub_division = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = FacilityType


class RegulatingBodyFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    abbreviation = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = RegulatingBody


class RegulationStatusFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = RegulationStatus


class FacilityRegulationStatusFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    regulating_body = django_filters.AllValuesFilter(lookup_type='exact')
    regulation_status = django_filters.AllValuesFilter(lookup_type='exact')
    reason = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = FacilityRegulationStatus


class FacilityContactFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    contact = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = FacilityContact


class FacilityFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.NumberFilter(lookup_type='exact')
    description = django_filters.CharFilter(lookup_type='icontains')

    facility_type = django_filters.AllValuesFilter(lookup_type='exact')
    operation_status = django_filters.AllValuesFilter(lookup_type='exact')
    ward = django_filters.AllValuesFilter(lookup_type='exact')
    owner = django_filters.AllValuesFilter(lookup_type='exact')
    officer_in_charge = django_filters.AllValuesFilter(lookup_type='exact')

    number_of_beds = django_filters.NumberFilter(lookup_type='exact')
    number_of_cots = django_filters.NumberFilter(lookup_type='exact')

    open_whole_day = django_filters.BooleanFilter(lookup_type='exact')
    open_whole_week = django_filters.BooleanFilter(lookup_type='exact')
    is_classified = django_filters.BooleanFilter(lookup_type='exact')
    is_published = django_filters.BooleanFilter(lookup_type='exact')

    class Meta:
        model = Facility


class GeoCodeSourceFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    abbreviation = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = GeoCodeSource


class GeoCodeMethodFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = GeoCodeMethod


class FacilityCoordinatesFilter(CommonFieldsFilterset):
    latitude = django_filters.CharFilter(lookup_type='icontains')
    longitude = django_filters.CharFilter(lookup_type='icontains')
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    source = django_filters.AllValuesFilter(lookup_type='exact')
    method = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = FacilityCoordinates


class FacilityUnitFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    facility = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = FacilityUnit
