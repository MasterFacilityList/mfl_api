from django.template import loader, Context
from django.http import HttpResponse

from django.utils import timezone

from rest_framework import generics
from common.views import AuditableDetailViewMixin

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
    ServiceRatingSerializer,
    FacilityApprovalSerializer,
    FacilityOperationStateSerializer,
    FacilityUpgradeSerializer,
    RegulatingBodyContactSerializer
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
    ServiceRatingFilter,
    FacilityApprovalFilter,
    FacilityOperationStateFilter,
    FacilityUpgradeFilter,
    RegulatingBodyContactFilter
)


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


class ServiceRatingListView(generics.ListCreateAPIView):
    queryset = ServiceRating.objects.all()
    serializer_class = ServiceRatingSerializer
    filter_class = ServiceRatingFilter
    ordering_fields = ('facility_service')


class ServiceRatingDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRating.objects.all()
    serializer_class = ServiceRatingSerializer


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


class FacilityListView(generics.ListCreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_class = FacilityFilter
    ordering_fields = (
        'name', 'code', 'number_of_beds', 'number_of_cots', 'operation_status',
        'ward', 'owner',
    )


class FacilityDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


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
    serializer_class = FacilityRegulationStatusSerializer
    filter_class = RegulationStatusFilter
    ordering_fields = ('name', )


class RegulationStatusDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = RegulationStatus.objects.all()
    serializer_class = FacilityRegulationStatusSerializer


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
