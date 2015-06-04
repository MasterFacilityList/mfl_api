from datetime import timedelta

from django.template import loader, Context
from django.http import HttpResponse

from django.utils import timezone

from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny

from rest_framework import generics
from common.views import AuditableDetailViewMixin
from common.models import County, Constituency

from ..models import (
    OwnerType,
    Owner,
    JobTitle,
    Officer,
    OfficerContact,
    FacilityStatus,
    FacilityType,
    RegulatingBody,
    RegulationStatus,
    Facility,
    FacilityRegulationStatus,
    FacilityContact,
    FacilityUnit,
    FacilityServiceRating,
    ServiceCategory,
    Option,
    Service,
    FacilityService,
    ServiceOption,
    FacilityApproval,
    FacilityOperationState,
    FacilityUpgrade,
    RegulatingBodyContact,

)

from ..serializers import (
    OwnerSerializer,
    FacilitySerializer,
    FacilityContactSerializer,
    FacilityStatusSerializer,
    FacilityTypeSerializer,
    JobTitleSerializer,
    OfficerSerializer,
    RegulatingBodySerializer,
    OwnerTypeSerializer,
    OfficerContactSerializer,
    FacilityRegulationStatusSerializer,
    FacilityUnitSerializer,
    ServiceCategorySerializer,
    OptionSerializer,
    ServiceSerializer,
    FacilityServiceSerializer,
    ServiceOptionSerializer,
    FacilityApprovalSerializer,
    FacilityOperationStateSerializer,
    FacilityUpgradeSerializer,
    RegulatingBodyContactSerializer,
    RegulationStatusSerializer,
    FacilityDetailSerializer,
    FacilityServiceRatingSerializer,
    FacilityListSerializer
)
from ..filters import (
    FacilityFilter,
    FacilityStatusFilter,
    OwnerFilter,
    JobTitleFilter,
    FacilityUnitFilter,
    OfficerFilter,
    RegulatingBodyFilter,
    OwnerTypeFilter,
    OfficerContactFilter,
    FacilityContactFilter,
    FacilityTypeFilter,
    FacilityRegulationStatusFilter,
    RegulationStatusFilter,
    ServiceCategoryFilter,
    OptionFilter,
    ServiceFilter,
    FacilityServiceFilter,
    ServiceOptionFilter,
    FacilityApprovalFilter,
    FacilityOperationStateFilter,
    FacilityUpgradeFilter,
    RegulatingBodyContactFilter,
)


class QuerysetFilterMixin(object):
    """
    Filter that only allows users to list facilities in their county
    if they are not a national user.

    This complements the fairly standard ( django.contrib.auth )
    permissions setup.

    It is not intended to be applied to all views ( it should be used
    only on views for resources that are directly linked to counties
    e.g. facilities ).
    """
    def get_queryset(self, *args, **kwargs):
        # The line below reflects the fact that geographic "attachment"
        # will occur at the smallest unit i.e the ward
        if not self.request.user.is_national and self.request.user.county \
                and hasattr(self.queryset.model, 'ward'):
            return self.queryset.filter(
                ward__constituency__county=self.request.user.county)

        return self.queryset


class RegulatingBodyContactListView(generics.ListCreateAPIView):
    """
    Lists and creates regulatory contact details

    contact --  A contact pk
    regulatory_body -- A regulatory bodies pk
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = RegulatingBodyContact.objects.all()
    serializer_class = RegulatingBodyContactSerializer
    filter_class = RegulatingBodyContactFilter
    ordering_fields = ('regulating_body', 'contact', )


class RegulatingBodyContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular regulatory body contact.
    """
    queryset = RegulatingBodyContact.objects.all()
    serializer_class = RegulatingBodyContactSerializer


class FacilityUpgradeListView(generics.ListCreateAPIView):
    """
    Lists and creates facility upgrades and downloads

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityUpgrade.objects.all()
    serializer_class = FacilityUpgradeSerializer
    filter_class = FacilityUpgradeFilter
    ordering_fields = ('facility', 'facility_type', 'reason', )


class FacilityUpgradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular facility upgrade or downgrade
    """
    queryset = FacilityUpgrade.objects.all()
    serializer_class = FacilityUpgradeSerializer


class FacilityOperationStateListView(generics.ListCreateAPIView):
    """
    Lists and creates operation statuses for facilities

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityOperationState.objects.all()
    serializer_class = FacilityOperationStateSerializer
    filter_class = FacilityOperationStateFilter
    ordering_fields = ('facility', 'operation_status', 'reason')


class FacilityOperationStateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular operation status
    """
    queryset = FacilityOperationState.objects.all()
    serializer_class = FacilityOperationStateSerializer


class FacilityApprovalListView(generics.ListCreateAPIView):
    """
    Lists and creates facility approvals

    facility -- A pk of the facility
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityApproval.objects.all()
    serializer_class = FacilityApprovalSerializer
    filter_class = FacilityApprovalFilter
    ordering_fields = ('facility', 'comment', )


class FacilityApprovalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular facility approval
    """
    queryset = FacilityApproval.objects.all()
    serializer_class = FacilityApprovalSerializer


class ServiceCategoryListView(generics.ListCreateAPIView):
    """
    Lists and creates service categories

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    filter_class = ServiceCategoryFilter
    ordering_fields = ('name', 'description', )


class ServiceCategoryDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular service category
    """
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class OptionListView(generics.ListCreateAPIView):
    """
    Lists and Creates options

    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    filter_class = OptionFilter
    ordering_fields = ('option_type', 'display_text', 'value', )


class OptionDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a a particular option
    """
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class ServiceListView(generics.ListCreateAPIView):
    """
    Lists and creates services

    category -- Service category pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_class = ServiceFilter
    ordering_fields = ('name', 'category', 'code',)


class ServiceDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular service
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class FacilityServiceListView(generics.ListCreateAPIView):
    """
    Lists and creates links between facilities and services

    facility -- A facility's pk
    selected_option -- A service selected_option's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityService.objects.all()
    serializer_class = FacilityServiceSerializer
    filter_class = FacilityServiceFilter
    ordering_fields = ('facility', 'service')


class FacilityServiceDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular facility service detail
    """
    queryset = FacilityService.objects.all()
    serializer_class = FacilityServiceSerializer


class FacilityServiceRatingListView(generics.ListCreateAPIView):
    """
    Lists and creates facility's services ratings
    """
    throttle_scope = 'rating'
    queryset = FacilityServiceRating.objects.all()
    serializer_class = FacilityServiceRatingSerializer
    ordering_fields = ('rating', )


class FacilityServiceRatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular facility service rating
    """
    queryset = FacilityServiceRating.objects.all()
    serializer_class = FacilityServiceRatingSerializer


class ServiceOptionListView(generics.ListCreateAPIView):
    """
    Lists and creates service options

    service -- A service's pk
    option -- An option's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = ServiceOption.objects.all()
    serializer_class = ServiceOptionSerializer
    filter_class = ServiceOptionFilter
    ordering_fields = ('service', 'option',)


class ServiceOptionDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular service option
    """
    queryset = ServiceOption.objects.all()
    serializer_class = ServiceOptionSerializer


class FacilityUnitsListView(generics.ListCreateAPIView):
    """
    Lists and creates facility units

    facility -- A facility's pk
    name -- Name of a facility unit
    description -- Description of a facility unit
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityUnit.objects.all()
    serializer_class = FacilityUnitSerializer
    ordering_fields = ('name', 'facility', 'regulating_body',)
    filter_class = FacilityUnitFilter


class FacilityUnitDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular facility unit's detail
    """
    queryset = FacilityUnit.objects.all()
    serializer_class = FacilityUnitSerializer


class FacilityStatusListView(generics.ListCreateAPIView):
    """
    Lists and creates facility operation statuses

    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityStatus.objects.all()
    serializer_class = FacilityStatusSerializer
    ordering_fields = ('name',)
    filter_class = FacilityStatusFilter


class FacilityStatusDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular operation status
    """
    queryset = FacilityStatus.objects.all()
    serializer_class = FacilityStatusSerializer


class JobTitleListView(generics.ListCreateAPIView):
    """
    Lists and creates job titles

    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    ordering_fields = ('name',)
    filter_class = JobTitleFilter


class JobTitleDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular job title
    """
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer


class OfficerListView(generics.ListCreateAPIView):
    """
    Lists and creates officers

    name  -- name of an officer
    registration_number -- The official registration  number of an officer
    job_title --  A job title's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Officer.objects.all()
    serializer_class = OfficerSerializer
    ordering_fields = ('name', 'job_title', 'registration_number',)
    filter_class = OfficerFilter


class OfficerDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular officer
    """
    queryset = Officer.objects.all()
    serializer_class = OfficerSerializer


class RegulatingBodyListView(generics.ListCreateAPIView):
    """
    Lists and creates regulatory bodies

    name -- Name of a regulatory body
    abbreviation -- The abbreviation of a regulatory body
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = RegulatingBody.objects.all()
    serializer_class = RegulatingBodySerializer
    ordering_fields = ('name', 'abbreviation',)
    filter_class = RegulatingBodyFilter


class RegulatingBodyDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular regulatory body details
    """
    queryset = RegulatingBody.objects.all()
    serializer_class = RegulatingBodySerializer


class OwnerTypeListView(generics.ListCreateAPIView):
    """
    Lists and creates a owners

    name --  The name of an owner type
    description --  Description of an owner type
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = OwnerType.objects.all()
    serializer_class = OwnerTypeSerializer
    ordering_fields = ('name', )
    filter_class = OwnerTypeFilter


class OwnerTypeDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular owner type
    """
    queryset = OwnerType.objects.all()
    serializer_class = OwnerTypeSerializer


class OfficerContactListView(generics.ListCreateAPIView):
    """
    Lists and creates officer contacts

    officer -- An officer's pk
    contact --  A contacts pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = OfficerContact.objects.all()
    serializer_class = OfficerContactSerializer
    ordering_fields = ('officer', 'contact',)
    filter_class = OfficerContactFilter


class OfficerContactDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular officer contact detail
    """
    queryset = OfficerContact.objects.all()
    serializer_class = OfficerContactSerializer


class OwnerListView(generics.ListCreateAPIView):
    """
    List and creates a list of owners

    name -- The name of an owner
    description -- The description of an owner
    abbreviation -- The abbreviation of an owner
    code --  The code of an owner
    owner_type -- An owner-type's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_class = OwnerFilter
    ordering_fields = ('name', 'code', 'owner_type',)


class OwnerDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular owner's details
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class FacilityListView(QuerysetFilterMixin, generics.ListCreateAPIView):
    """
    Lists and creates facilities

    name -- The name of the facility
    code -- A list of comma separated facility codes (one or more)
    description -- The description of the facility
    facility_type -- A list of comma separated facility type's pk
    operation_status -- A list of comma separated operation statuses pks
    ward -- A list of comma separated ward pks (one or more)
    ward_code -- A list of comma separated ward codes
    county_code -- A list of comma separated county codes
    constituency_code -- A list of comma separated constituency codes
    county -- A list of comma separated county pks
    constituency -- A list of comma separated constituency pks
    owner -- A list of comma separated owner pks
    officer_in_charge -- A list of comma separated officer pks
    number_of_beds -- A list of comma separated integers
    number_of_cots -- A list of comma separated integers
    open_whole_day -- Boolean True/False
    is_classified -- Boolean True/False
    is_published -- Boolean True/False
    is_regulated -- Boolean True/False
    service_category -- A service category's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_class = FacilityFilter
    ordering_fields = (
        'name', 'code', 'number_of_beds', 'number_of_cots', 'operation_status',
        'ward', 'owner',
    )


class FacilityListReadOnlyView(
        QuerysetFilterMixin, AuditableDetailViewMixin, generics.ListAPIView):
    """
    Returns a slimmed payload of the facility.
    """
    queryset = Facility.objects.all()
    serializer_class = FacilityListSerializer
    filter_class = FacilityFilter
    ordering_fields = (
        'code', 'name', 'county', 'constituency', 'facility_type_name',
        'owner_type_name'
    )


class FacilityDetailView(
        QuerysetFilterMixin, AuditableDetailViewMixin,
        generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular facility
    """
    queryset = Facility.objects.all()
    serializer_class = FacilityDetailSerializer


class FacilityContactListView(generics.ListCreateAPIView):
    """
    Lists and creates facility contacts

    facility -- A facility's pk
    contact -- A contact's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityContact.objects.all()
    serializer_class = FacilityContactSerializer
    filter_class = FacilityContactFilter
    ordering_fields = ('facility', 'contact',)


class FacilityContactDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular facility contact
    """
    queryset = FacilityContact.objects.all()
    serializer_class = FacilityContactSerializer


class FacilityRegulationStatusListView(generics.ListCreateAPIView):
    """
    Lists and creates facilities regulation statuses

    facility -- A facility's pk
    regulating_body -- A regulating body's pk
    regulation_status -- A regulation status's pk
    reason -- A reason for a certain regulation status
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityRegulationStatus.objects.all()
    serializer_class = FacilityRegulationStatusSerializer
    filter_class = FacilityRegulationStatusFilter
    ordering_fields = (
        'facility', 'regulating_body', 'regulation_status',)


class FacilityRegulationStatusDetailView(
        AuditableDetailViewMixin,
        generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular facility's regulation status
    """
    queryset = FacilityRegulationStatus.objects.all()
    serializer_class = FacilityRegulationStatusSerializer


class FacilityTypeListView(generics.ListCreateAPIView):
    """
    Lists and creates facility types

    name -- Name of a facility type
    sub_division -- A sub-division in a facility type
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer
    filter_class = FacilityTypeFilter
    ordering_fields = ('name', )


class FacilityTypeDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular facility types detail
    """
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer


class RegulationStatusListView(
        AuditableDetailViewMixin, generics.ListCreateAPIView):
    """
    Lists and creates regulation statuses

    name -- name of a regulation status
    description -- description of a regulation status
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = RegulationStatus.objects.all()
    serializer_class = RegulationStatusSerializer
    filter_class = RegulationStatusFilter
    ordering_fields = ('name', )


class RegulationStatusDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular regulation status
    """
    queryset = RegulationStatus.objects.all()
    serializer_class = RegulationStatusSerializer


class FacilityInspectionReport(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, facility_id, *args, **kwargs):
        return self.get_inspection_report(facility_id)

    def get_inspection_report(self, facility_id):
        facility = Facility.objects.get(pk=facility_id)
        template = loader.get_template('inspection_report.txt')
        report_date = timezone.now().isoformat()
        regulating_bodies = FacilityRegulationStatus.objects.filter(
            facility=facility)
        regulating_body = regulating_bodies[0] if regulating_bodies else None

        context = Context(
            {
                "report_date": report_date,
                "facility": facility,
                "regulating_body": regulating_body
            }
        )
        return HttpResponse(template.render(context))


class FacilityCoverTemplate(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, facility_id, *args, **kwargs):
        return self.get_cover_report(facility_id)

    def get_cover_report(self, facility_id):
        facility = Facility.objects.get(pk=facility_id)
        template = loader.get_template('cover_report.txt')
        report_date = timezone.now().isoformat()
        context = Context(
            {
                "report_date": report_date,
                "facility": facility
            }
        )
        return HttpResponse(template.render(context))


class FacilityCorrectionTemplate(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, facility_id, *args, **kwargs):
        return self.get_correction_template(facility_id)

    def get_correction_template(self, facility_id):
        facility = Facility.objects.get(pk=facility_id)
        template = loader.get_template('correction_template.txt')
        request_date = timezone.now().isoformat()
        context = Context(
            {
                "request_date": request_date,
                "facility": facility
            }
        )
        return HttpResponse(template.render(context))


class DashBoard(APIView):
    queryset = Facility.objects.all()
    filter_class = FacilityFilter

    def get_facility_county_summary(self):
        counties = County.objects.all()
        facility_county_summary = {}
        for county in counties:
            facility_county_count = self.queryset.filter(
                ward__constituency__county=county).count()
            facility_county_summary[county.name] = facility_county_count
        top_10_counties = sorted(
            facility_county_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        facility_county_summary
        top_10_counties_summary = []
        for item in top_10_counties:
            top_10_counties_summary.append(
                {
                    "name": item[0],
                    "count": item[1]
                })
        if self.request.user.is_national:
            return top_10_counties_summary
        else:
            return []

    def get_facility_constituency_summary(self):
        constituencies = Constituency.objects.filter(
            county=self.request.user.county)
        facility_constituency_summary = {}
        for const in constituencies:
            facility_const_count = self.queryset.filter(
                ward__constituency=const).count()
            facility_constituency_summary[const.name] = facility_const_count
        top_10_consts = sorted(
            facility_constituency_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        top_10_consts_summary = []
        for item in top_10_consts:
            top_10_consts_summary.append(
                {
                    "name": item[0],
                    "count": item[1]
                })
        return top_10_consts_summary

    def get_facility_type_summary(self):
        facility_types = FacilityType.objects.all()
        facility_type_summary = []
        for facility_type in facility_types:
            facility_type_count = self.queryset.filter(
                facility_type=facility_type).count()
            facility_type_summary.append(
                {
                    "name": facility_type.name,
                    "count": facility_type_count
                })
        return facility_type_summary

    def get_facility_owner_summary(self):
        owners = Owner.objects.all()
        facility_owners_summary = []
        for owner in owners:
            owner_count = self.queryset.filter(owner=owner).count()
            facility_owners_summary.append(
                {
                    "name": owner.name,
                    "count": owner_count
                })
        return facility_owners_summary

    def get_facility_status_summary(self):
        statuses = FacilityStatus.objects.all()
        status_summary = []
        for status in statuses:
            if not self.request.user.is_national:
                status_count = Facility.objects.filter(
                    operation_status=status,
                    ward__constituency__county=self.request.user.county
                ).count()
                status_summary.append(
                    {
                        "name": status.name,
                        "count": status_count

                    })
            else:
                status_count = Facility.objects.filter(
                    operation_status=status).count()
                status_summary.append(
                    {
                        "name": status.name,
                        "count": status_count
                    })
        return status_summary

    def get_facility_owner_types_summary(self):
        owner_types = OwnerType.objects.all()
        owner_types_summary = []
        for owner_type in owner_types:
            if self.request.user.is_national:
                owner_types_count = Facility.objects.filter(
                    owner__owner_type=owner_type).count()
                owner_types_summary.append(
                    {
                        "name": owner_type.name,
                        "count": owner_types_count
                    })
            else:
                owner_types_count = Facility.objects.filter(
                    owner__owner_type=owner_type,
                    ward__constituency__county=self.request.user.county
                ).count()
                owner_types_summary.append(
                    {
                        "name": owner_type.name,
                        "count": owner_types_count
                    })
        return owner_types_summary

    def get_recently_created_facilities(self):
        right_now = timezone.now()
        three_months_ago = right_now - timedelta(days=90)
        recent_facilities_count = 0
        if self.request.user.is_national:
            recent_facilities_count = Facility.objects.filter(
                created__gte=three_months_ago).count()
        else:
            recent_facilities_count = Facility.objects.filter(
                created__gte=three_months_ago,
                ward__constituency__county=self.request.user.county).count()
        return recent_facilities_count

    def get(self, *args, **kwargs):
        total_facilities = 0
        if self.request.user.is_national:
            total_facilities = Facility.objects.count()
        else:
            total_facilities = Facility.objects.filter(
                ward__constituency__county=self.request.user.county
            ).count()

        data = {
            "total_facilities": total_facilities,
            "county_summary": self.get_facility_county_summary(),
            "constituencies_summary": self.get_facility_constituency_summary(),
            "owners_summary": self.get_facility_owner_summary(),
            "types_summary": self.get_facility_type_summary(),
            "status_summary": self.get_facility_status_summary(),
            "owner_types": self.get_facility_owner_types_summary(),
            "recently_created": self.get_recently_created_facilities()
        }

        return Response(data)
