import django_filters

from ..models import (
    Owner, Service, Facility, FacilityGPS, JobTitle, FacilityUnit,
    FacilityStatus, OfficerIncharge, RegulatingBody, GeoCodeSource,
    ServiceCategory, OwnerType, OfficerInchargeContact, GeoCodeMethod,
    FacilityService, FacilityContact, FacilityRegulationStatus,
    FacilityType, RegulationStatus, ChoiceService,
    KEHPLevelService, BasicComprehensiveService
)
from common.filters.filter_shared import CommonFieldsFilterset


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


class OfficerInchargeContactFilter(CommonFieldsFilterset):
    officer = django_filters.AllValuesFilter(lookup_type='icontains')
    contact = django_filters.AllValuesFilter(lookup_type='icontains')

    class Meta:
        model = OfficerInchargeContact


class OfficerInchargeFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    registration_number = django_filters.CharFilter(lookup_type='icontains')
    job_title = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = OfficerIncharge


class ServiceCategoryFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = ServiceCategory


class ServiceFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.NumberFilter(lookup_type='exact')
    category = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = Service


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


class FacilityServiceFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    service = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = FacilityService


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


class FacilityGPSFilter(CommonFieldsFilterset):
    latitude = django_filters.CharFilter(lookup_type='icontains')
    longitude = django_filters.CharFilter(lookup_type='icontains')
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    source = django_filters.AllValuesFilter(lookup_type='exact')
    method = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = FacilityGPS


class FacilityUnitFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    regulating_body = django_filters.AllValuesFilter(lookup_type='exact')
    is_approved = django_filters.BooleanFilter(lookup_type='exact')

    class Meta:
        model = FacilityUnit


class ChoiceServiceFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = ChoiceService


class KEHPLevelServiceFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = KEHPLevelService


class BasicComprehensiveServiceFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = BasicComprehensiveService
