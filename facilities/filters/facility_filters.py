from django.db.models import Q

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
    FacilityApproval,
    FacilityOperationState,
    FacilityUpgrade,
    RegulatingBodyContact,
    FacilityServiceRating,
    FacilityOfficer,
    RegulatoryBodyUser,
    FacilityUnitRegulation,
    FacilityUpdates,
    KephLevel,
    OptionGroup,
    FacilityLevelChangeReason,
    FacilityDepartment,
    RegulatorSync,
    FacilityExportExcelMaterialView
)
from common.filters.filter_shared import (
    CommonFieldsFilterset,
    ListIntegerFilter,
    ListCharFilter,
    NullFilter,
    SearchFilter, ListUUIDFilter
)

from common.constants import BOOLEAN_CHOICES, TRUTH_NESS


class FacilityExportExcelMaterialViewFilter(django_filters.FilterSet):

    search = SearchFilter(name='search')
    county = ListCharFilter(lookup_type='exact')
    code = ListCharFilter(lookup_type='exact')
    constituency = ListCharFilter(lookup_type='exact')
    ward = ListCharFilter(lookup_type='exact')
    owner = ListCharFilter(lookup_type='exact')
    owner_type = ListCharFilter(lookup_type='exact')
    number_of_beds = ListIntegerFilter(lookup_type='exact')
    number_of_cots = ListIntegerFilter(lookup_type='exact')
    open_whole_day = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    open_late_night = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    open_weekends = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    open_public_holidays = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    keph_level = ListCharFilter(lookup_type='exact')
    facility_type = ListCharFilter(lookup_type='exact')
    operation_status = ListCharFilter(lookup_type='exact')
    service = ListUUIDFilter(lookup_type='exact', name='services')
    service_category = ListUUIDFilter(lookup_type='exact', name='categories')

    class Meta(object):
        model = FacilityExportExcelMaterialView


class RegulatorSyncFilter(CommonFieldsFilterset):
    mfl_code_null = NullFilter(name='mfl_code')
    county = ListCharFilter(lookup_type='exact')

    class Meta(object):
        model = RegulatorSync


class OptionGroupFilter(CommonFieldsFilterset):

    class Meta(object):
        model = OptionGroup


class FacilityLevelChangeReasonFilter(CommonFieldsFilterset):

    class Meta(object):
        model = FacilityLevelChangeReason


class KephLevelFilter(CommonFieldsFilterset):

    class Meta(object):
        model = KephLevel


class FacilityUpdatesFilter(CommonFieldsFilterset):

    class Meta(object):
        model = FacilityUpdates


class RegulatoryBodyUserFilter(CommonFieldsFilterset):

    class Meta(object):
        model = RegulatoryBodyUser


class FacilityOfficerFilter(CommonFieldsFilterset):

    class Meta(object):
        model = FacilityOfficer


class FacilityServiceRatingFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(
        name='facility_service__facility',
        lookup_type='exact')
    service = django_filters.AllValuesFilter(
        name="facility_service__service", lookup_type='exact')
    county = django_filters.AllValuesFilter(
        name="facility_service__facility__ward__constituency__county",
        lookup_type='exact')
    constituency = django_filters.AllValuesFilter(
        name="facility_service__facility__ward__constituency",
        lookup_type='exact')
    ward = django_filters.AllValuesFilter(
        name="facility_service__facility__ward", lookup_type='exact')

    class Meta(object):
        model = FacilityServiceRating


class RegulatingBodyContactFilter(CommonFieldsFilterset):

    class Meta(object):
        model = RegulatingBodyContact


class FacilityUpgradeFilter(CommonFieldsFilterset):
    is_confirmed = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    is_cancelled = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)

    class Meta(object):
        model = FacilityUpgrade


class FacilityOperationStateFilter(CommonFieldsFilterset):
    operation_status = django_filters.AllValuesFilter(lookup_type='exact')
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    reason = django_filters.CharFilter(lookup_type='exact')

    class Meta(object):
        model = FacilityOperationState


class FacilityApprovalFilter(CommonFieldsFilterset):
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    comment = django_filters.CharFilter(lookup_type='icontains')
    is_cancelled = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)

    class Meta(object):
        model = FacilityApproval


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
    option = django_filters.AllValuesFilter(lookup_type='exact')
    is_confirmed = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=strtobool
    )
    is_cancelled = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=strtobool
    )

    class Meta(object):
        model = FacilityService


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
    officer = django_filters.AllValuesFilter(lookup_type='exact')
    contact = django_filters.AllValuesFilter(lookup_type='exact')

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
    facility = django_filters.CharFilter(lookup_type='exact')
    contact = django_filters.CharFilter(lookup_type='exact')

    class Meta(object):
        model = FacilityContact


class FacilityFilter(CommonFieldsFilterset):

    def service_filter(self, value):
        categories = value.split(',')
        facility_ids = []

        for facility in self.filter():
            for cat in categories:
                service_count = FacilityService.objects.filter(
                    service__category=cat,
                    facility=facility).count()
                if service_count > 0:
                    facility_ids.append(facility.id)

        return self.filter(id__in=list(set(facility_ids)))

    def filter_approved_facilities(self, value):

        if value in TRUTH_NESS:
            return self.filter(Q(approved=True) | Q(rejected=True))
        else:
            return self.filter(rejected=False, approved=False)

    def facilities_pending_approval(self, value):
        if value in TRUTH_NESS:
            return self.filter(
                Q(rejected=False),
                Q(has_edits=True) | Q(approved=False)
            )
        else:
            return self.filter(
                Q(rejected=True) |
                Q(has_edits=False) & Q(approved=True))

    id = ListCharFilter(lookup_type='icontains')
    name = django_filters.CharFilter(lookup_type='icontains')
    code = ListIntegerFilter(lookup_type='exact')
    description = ListCharFilter(lookup_type='icontains')

    facility_type = ListCharFilter(lookup_type='icontains')
    keph_level = ListCharFilter(lookup_type='exact')
    operation_status = ListCharFilter(lookup_type='icontains')
    ward = ListCharFilter(lookup_type='icontains')
    sub_county = ListCharFilter(lookup_type='exact', name='ward__sub_county')
    sub_county_code = ListCharFilter(
        name="ward__sub_county__code", lookup_type='exact')
    ward_code = ListCharFilter(name="ward__code", lookup_type='icontains')
    county_code = ListCharFilter(
        name='ward__constituency__county__code',
        lookup_type='icontains')
    constituency_code = ListCharFilter(
        name='ward__constituency__code', lookup_type='icontains')
    county = ListCharFilter(
        name='ward__constituency__county',
        lookup_type='exact')
    constituency = ListCharFilter(
        name='ward__constituency', lookup_type='icontains')
    owner = ListCharFilter(lookup_type='icontains')
    owner_type = ListCharFilter(name='owner__owner_type', lookup_type='exact')
    officer_in_charge = ListCharFilter(lookup_type='icontains')
    number_of_beds = ListIntegerFilter(lookup_type='exact')
    number_of_cots = ListIntegerFilter(lookup_type='exact')
    open_whole_day = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    open_late_night = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    open_weekends = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    open_public_holidays = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    is_classified = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    is_published = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    is_approved = django_filters.MethodFilter(
        action=filter_approved_facilities)
    service_category = django_filters.MethodFilter(
        action=service_filter)
    has_edits = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    rejected = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    regulated = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    approved = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES,
        coerce=strtobool)
    closed = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=strtobool)
    pending_approval = django_filters.MethodFilter(
        action=facilities_pending_approval)

    class Meta(object):
        model = Facility


class FacilityUnitFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')
    facility = django_filters.CharFilter(lookup_type='exact')

    class Meta(object):
        model = FacilityUnit


class FacilityUnitRegulationFilter(CommonFieldsFilterset):

    class Meta(object):
        model = FacilityUnitRegulation


class FacilityDepartmentFilter(CommonFieldsFilterset):

    class Meta(object):
        model = FacilityDepartment
