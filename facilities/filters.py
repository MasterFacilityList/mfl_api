import django_filters

from .models import (
    Owner, Service, Facility, FacilityGPS, JobTitle, FacilityUnit,
    FacilityStatus, OfficerIncharge, RegulatingBody, GeoCodeSource,
    ServiceCategory, OwnerType, OfficerInchargeContact, GeoCodeMethod,
    FacilityService, FacilityContact, FacilityRegulationStatus,
    FacilityType, RegulationStatus
)
from common.filters.filter_shared import CommonFieldsFilterset


class JobTitleFilter(CommonFieldsFilterset):
    class Meta:
        model = JobTitle


class OwnerFilter(CommonFieldsFilterset):
    class Meta:
        model = Owner


class ServiceFilter(CommonFieldsFilterset):
    class Meta:
        model = Service


class FacilityGPSFilter(CommonFieldsFilterset):
    class Meta:
        model = FacilityGPS


class FacilityStatusFilter(CommonFieldsFilterset):
    class Meta:
        model = FacilityStatus


class FacilityServiceFilter(CommonFieldsFilterset):
    class Meta:
        model = FacilityService


class FacilityContactFilter(CommonFieldsFilterset):
    class Meta:
        model = FacilityContact


class FacilityRegulationStatusFilter(CommonFieldsFilterset):
    class Meta:
        model = FacilityRegulationStatus


class FacilityTypeFilter(CommonFieldsFilterset):
    class Meta:
        model = FacilityType


class OfficerInchargeFilter(CommonFieldsFilterset):
    class Meta:
        model = OfficerIncharge


class RegulatingBodyFilter(CommonFieldsFilterset):
    class Meta:
        model = RegulatingBody


class GeoCodeSourceFilter(CommonFieldsFilterset):
    class Meta:
        model = GeoCodeSource


class GeoCodeMethodFilter(CommonFieldsFilterset):
    class Meta:
        model = GeoCodeMethod


class ServiceCategoryFilter(CommonFieldsFilterset):
    class Meta:
        model = ServiceCategory


class OwnerTypeFilter(CommonFieldsFilterset):
    class Meta:
        model = OwnerType


class OfficerInchargeContactFilter(CommonFieldsFilterset):
    class Meta:
        model = OfficerInchargeContact


class RegulationStatusFilter(CommonFieldsFilterset):
    class Meta:
        model = RegulationStatus


class FacilityFilter(CommonFieldsFilterset):
    beds = django_filters.NumberFilter(name='number_of_beds')
    cots = django_filters.NumberFilter(name='number_of_cots')
    open_whole_day = django_filters.BooleanFilter(name='open_whole_day')
    open_whole_week = django_filters.BooleanFilter(name='open_whole_week')
    is_classified = django_filters.BooleanFilter(name='is_classified')
    is_published = django_filters.BooleanFilter(name='is_published')

    class Meta:
        model = Facility


class FacilityUnitFilter(CommonFieldsFilterset):
    class Meta:
        model = FacilityUnit


# TODO Facility contact list view should filter by facility and contact
# TODO Facility service list view should filter by facility and service
