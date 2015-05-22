from django.template import loader, Context
from django.http import HttpResponse

from django.utils import timezone

from rest_framework.views import APIView, Response
from rest_framework import generics
from common.views import AuditableDetailViewMixin
from common.models import Ward, County, Constituency

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
    queryset = RegulatingBodyContact.objects.all()
    serializer_class = RegulatingBodyContactSerializer
    filter_class = RegulatingBodyContactFilter
    ordering_fields = ('regulating_body', 'contact', )


class RegulatingBodyContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegulatingBodyContact.objects.all()
    serializer_class = RegulatingBodyContactSerializer


class FacilityUpgradeListView(generics.ListCreateAPIView):
    queryset = FacilityUpgrade.objects.all()
    serializer_class = FacilityUpgradeSerializer
    filter_class = FacilityUpgradeFilter
    ordering_fields = ('facility', 'facility_type', 'reason', )


class FacilityUpgradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityUpgrade.objects.all()
    serializer_class = FacilityUpgradeSerializer


class FacilityOperationStateListView(generics.ListCreateAPIView):
    queryset = FacilityOperationState.objects.all()
    serializer_class = FacilityOperationStateSerializer
    filter_class = FacilityOperationStateFilter
    ordering_fields = ('facility', 'operation_status', 'reason')


class FacilityOperationStateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityOperationState.objects.all()
    serializer_class = FacilityOperationStateSerializer


class FacilityApprovalListView(generics.ListCreateAPIView):
    queryset = FacilityApproval.objects.all()
    serializer_class = FacilityApprovalSerializer
    filter_class = FacilityApprovalFilter
    ordering_fields = ('facility', 'comment', )


class FacilityApprovalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityApproval.objects.all()
    serializer_class = FacilityApprovalSerializer


class ServiceCategoryListView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    filter_class = ServiceCategoryFilter
    ordering_fields = ('name', 'description', )


class ServiceCategoryDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class OptionListView(generics.ListCreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    filter_class = OptionFilter
    ordering_fields = ('option_type', 'display_text', 'value', )


class OptionDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class ServiceListView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_class = ServiceFilter
    ordering_fields = ('name', 'category', 'code',)


class ServiceDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class FacilityServiceListView(generics.ListCreateAPIView):
    queryset = FacilityService.objects.all()
    serializer_class = FacilityServiceSerializer
    filter_class = FacilityServiceFilter
    ordering_fields = ('facility', 'service')


class FacilityServiceDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityService.objects.all()
    serializer_class = FacilityServiceSerializer


class FacilityServiceRatingListView(generics.ListCreateAPIView):
    queryset = FacilityServiceRating.objects.all()
    serializer_class = FacilityServiceRatingSerializer
    ordering_fields = ('rating', )


class FacilityServiceRatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityServiceRating.objects.all()
    serializer_class = FacilityServiceRatingSerializer


class ServiceOptionListView(generics.ListCreateAPIView):
    queryset = ServiceOption.objects.all()
    serializer_class = ServiceOptionSerializer
    filter_class = ServiceOptionFilter
    ordering_fields = ('service', 'option',)


class ServiceOptionDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceOption.objects.all()
    serializer_class = ServiceOptionSerializer


class FacilityUnitsListView(generics.ListCreateAPIView):
    queryset = FacilityUnit.objects.all()
    serializer_class = FacilityUnitSerializer
    ordering_fields = ('name', 'facility', 'regulating_body',)
    filter_class = FacilityUnitFilter


class FacilityUnitDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityUnit.objects.all()
    serializer_class = FacilityUnitSerializer


class FacilityStatusListView(generics.ListCreateAPIView):
    queryset = FacilityStatus.objects.all()
    serializer_class = FacilityStatusSerializer
    ordering_fields = ('name',)
    filter_class = FacilityStatusFilter


class FacilityStatusDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityStatus.objects.all()
    serializer_class = FacilityStatusSerializer


class JobTitleListView(generics.ListCreateAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    ordering_fields = ('name',)
    filter_class = JobTitleFilter


class JobTitleDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer


class OfficerListView(generics.ListCreateAPIView):
    queryset = Officer.objects.all()
    serializer_class = OfficerSerializer
    ordering_fields = ('name', 'job_title', 'registration_number',)
    filter_class = OfficerFilter


class OfficerDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Officer.objects.all()
    serializer_class = OfficerSerializer


class RegulatingBodyListView(generics.ListCreateAPIView):
    queryset = RegulatingBody.objects.all()
    serializer_class = RegulatingBodySerializer
    ordering_fields = ('name', 'abbreviation',)
    filter_class = RegulatingBodyFilter


class RegulatingBodyDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = RegulatingBody.objects.all()
    serializer_class = RegulatingBodySerializer


class OwnerTypeListView(generics.ListCreateAPIView):
    queryset = OwnerType.objects.all()
    serializer_class = OwnerTypeSerializer
    ordering_fields = ('name', )
    filter_class = OwnerTypeFilter


class OwnerTypeDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = OwnerType.objects.all()
    serializer_class = OwnerTypeSerializer


class OfficerContactListView(generics.ListCreateAPIView):
    queryset = OfficerContact.objects.all()
    serializer_class = OfficerContactSerializer
    ordering_fields = ('officer', 'contact',)
    filter_class = OfficerContactFilter


class OfficerContactDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = OfficerContact.objects.all()
    serializer_class = OfficerContactSerializer


class OwnerListView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_class = OwnerFilter
    ordering_fields = ('name', 'code', 'owner_type',)


class OwnerDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class FacilityListView(QuerysetFilterMixin, generics.ListCreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_class = FacilityFilter
    ordering_fields = (
        'name', 'code', 'number_of_beds', 'number_of_cots', 'operation_status',
        'ward', 'owner',
    )


class FacilityDetailView(
        QuerysetFilterMixin, AuditableDetailViewMixin,
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilityDetailSerializer


class FacilityContactListView(generics.ListCreateAPIView):
    queryset = FacilityContact.objects.all()
    serializer_class = FacilityContactSerializer
    filter_class = FacilityContactFilter
    ordering_fields = ('facility', 'contact',)


class FacilityContactDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityContact.objects.all()
    serializer_class = FacilityContactSerializer


class FacilityRegulationStatusListView(generics.ListCreateAPIView):
    queryset = FacilityRegulationStatus.objects.all()
    serializer_class = FacilityRegulationStatusSerializer
    filter_class = FacilityRegulationStatusFilter
    ordering_fields = (
        'facility', 'regulating_body', 'regulation_status',)


class FacilityRegulationStatusDetailView(
        AuditableDetailViewMixin,
        generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityRegulationStatus.objects.all()
    serializer_class = FacilityRegulationStatusSerializer


class FacilityTypeListView(generics.ListCreateAPIView):
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer
    filter_class = FacilityTypeFilter
    ordering_fields = ('name', )


class FacilityTypeDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer


class RegulationStatusListView(
        AuditableDetailViewMixin, generics.ListCreateAPIView):
    queryset = RegulationStatus.objects.all()
    serializer_class = RegulationStatusSerializer
    filter_class = RegulationStatusFilter
    ordering_fields = ('name', )


class RegulationStatusDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = RegulationStatus.objects.all()
    serializer_class = RegulationStatusSerializer


def get_inspection_report(request, facility_id):
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


def get_cover_report(request, facility_id):
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


def get_correction_template(request, facility_id):
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

    def get_facility_wards_summary(self):
        wards = Ward.objects.all()
        facility_wards_summary = {}
        for ward in wards:
            ward_facility_count = self.queryset.filter(ward=ward).count()
            facility_wards_summary[ward.name] = ward_facility_count
        return facility_wards_summary

    def get_facility_county_summary(self):
        counties = County.objects.all()
        facility_county_summary = {}
        for county in counties:
            facility_county_count = self.queryset.filter(
                ward__constituency__county=county).count()
            facility_county_summary[county.name] = facility_county_count
        return facility_county_summary

    def get_facility_constituency_summary(self):
        constituencies = Constituency.objects.all()
        facility_constituency_summary = {}
        for const in constituencies:
            facility_const_count = self.queryset.filter(
                ward__constituency=const).count()
            facility_constituency_summary[const.name] = facility_const_count
        return facility_constituency_summary

    def get_facility_type_summary(self):
        facility_types = FacilityType.objects.all()
        facility_type_summary = {}
        for facility_type in facility_types:
            facility_type_count = self.queryset.filter(
                facility_type=facility_type).count()
            facility_type_summary[facility_type.name] = facility_type_count
        return facility_type_summary

    def get_facility_owner_summary(self):
        owners = Owner.objects.all()
        facility_owners_summary = {}
        for owner in owners:
            owner_count = self.queryset.filter(owner=owner).count()
            facility_owners_summary[owner.name] = owner_count
        return facility_owners_summary

    def get_facility_regulators_summary(self):
        regulation_status = FacilityRegulationStatus.objects.all()
        regulatory_bodies = RegulatingBody.objects.all()
        regulator_summary = {}
        facility_units = FacilityUnit.objects.all()

        for body in regulatory_bodies:
            facility_regulator_count = regulation_status.filter(
                regulating_body=body).count()
            regulator_summary[body.name] = {}
            regulator_summary[body.name]['facilities'] = \
                facility_regulator_count
            facility_units_count = facility_units.filter(
                regulating_body=body).count()
            regulator_summary[body.name]['units'] = facility_units_count
        return regulator_summary

    def get(self, *args, **kwargs):

        data = {
            "total_facilities": Facility.objects.count(),
            "wards_summary": self.get_facility_wards_summary(),
            "county_summary": self.get_facility_county_summary(),
            "constituencies_summary": self.get_facility_constituency_summary(),
            "owners_summary": self.get_facility_owner_summary(),
            "types_summary": self.get_facility_type_summary(),
            "regulator_summry": self.get_facility_regulators_summary()
        }

        return Response(data)
