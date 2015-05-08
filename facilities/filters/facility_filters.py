from distutils.util import strtobool

import django_filters


from ..models import (
    Owner,
    Facility,
    JobTitle,
    FacilityUnit,
    FacilityStatus,
    Officer,
    RegulatingBody,
    OwnerType,
    OfficerContact,
    FacilityContact,
    FacilityRegulationStatus,
    FacilityType,
    RegulationStatus,
    ServiceCategory,
    Option,
    Service,
    FacilityService,
    ServiceOption,
    ServiceRating,
    FacilityApproval,
    FacilityOperationState,
    FacilityUpgrade,
    RegulatingBodyContact
)
from common.filters.filter_shared import CommonFieldsFilterset

BOOLEAN_CHOICES = (
    ('false', 'False'),
    ('true', 'True'),
    ('yes', 'True'),
    ('no', 'False'),
    ('Yes', 'True'),
    ('No', 'False'),
    ('y', 'True'),
    ('n', 'False'),
    ('Y', 'True'),
    ('N', 'False')
)


class RegulatingBodyContactFilter(CommonFieldsFilterset):
    class Meta(object):
        model = RegulatingBodyContact


class FacilityUpgradeFilter(CommonFieldsFilterset):
    class Meta(object):
        model = FacilityUpgrade


class FacilityOperationStateFilter(CommonFieldsFilterset):
    operation_status = django_filters.AllValuesFilter(lookup_type='exact')
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    reason = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = FacilityOperationState


class FacilityApprovalFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    comment = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = FacilityApproval


class ServiceRatingFilter(CommonFieldsFilterset):
    facility_service = django_filters.AllValuesFilter(lookup_type='exact')
    cleanliness = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    attitude = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    will_return = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    occupation = django_filters.CharFilter(lookup_type='icontains')
    comment = django_filters.CharFilter(lookup_type='icontains')
    service = django_filters.AllValuesFilter(
        name='facility_service__service', lookup_type='exact')
    facility = django_filters.AllValuesFilter(
        name='facility_service__facility', lookup_type='exact')

    class Meta(object):
        model = ServiceRating


class ServiceCategoryFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = ServiceCategory


class OptionFilter(CommonFieldsFilterset):
    value = django_filters.CharFilter(lookup_type='icontains')
    display_text = django_filters.CharFilter(lookup_type='icontains')
    option_type = django_filters.CharFilter(lookup_type='icontains')
    is_exclusive_option = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)

    class Meta(object):
        model = Option


class ServiceFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    category = django_filters.AllValuesFilter(lookup_type='exact')
    code = django_filters.CharFilter(lookup_type='exact')

    class Meta(object):
        model = Service


class FacilityServiceFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    selected_option = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = FacilityService


class ServiceOptionFilter(CommonFieldsFilterset):
    service = django_filters.AllValuesFilter(lookup_type='exact')
    option = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = ServiceOption


class OwnerTypeFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = OwnerType


class OwnerFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    abbreviation = django_filters.CharFilter(lookup_type='icontains')
    code = django_filters.NumberFilter(lookup_type='exact')
    owner_type = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = Owner


class JobTitleFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = JobTitle


class OfficerContactFilter(CommonFieldsFilterset):
    officer = django_filters.AllValuesFilter(lookup_type='icontains')
    contact = django_filters.AllValuesFilter(lookup_type='icontains')

    class Meta(object):
        model = OfficerContact


class OfficerFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    registration_number = django_filters.CharFilter(lookup_type='icontains')
    job_title = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = Officer


class FacilityStatusFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = FacilityStatus


class FacilityTypeFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    sub_division = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = FacilityType


class RegulatingBodyFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    abbreviation = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = RegulatingBody


class RegulationStatusFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = RegulationStatus


class FacilityRegulationStatusFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    regulating_body = django_filters.AllValuesFilter(lookup_type='exact')
    regulation_status = django_filters.AllValuesFilter(lookup_type='exact')
    reason = django_filters.CharFilter(lookup_type='icontains')

    class Meta(object):
        model = FacilityRegulationStatus


class FacilityContactFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    contact = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = FacilityContact


class FacilityFilter(CommonFieldsFilterset):
    def filter_regulated_facilities(self, value):
        matching_facilities = []
        for obj in Facility.objects.all():

            # bool is operating in reverse
            if obj.is_regulated is not bool(value):
                matching_facilities.append(obj)
        return matching_facilities

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

    open_whole_day = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    open_whole_week = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    is_classified = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    is_published = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    is_regulated = django_filters.MethodFilter(
        action=filter_regulated_facilities)

    class Meta(object):
        model = Facility


class FacilityUnitFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    facility = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta(object):
        model = FacilityUnit
