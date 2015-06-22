from django.template import loader, Context
from django.http import HttpResponse
from django.utils import timezone

from rest_framework import generics
from common.views import AuditableDetailViewMixin

from ..models import (
    FacilityApproval,
    FacilityUpgrade,
    Facility,
    FacilityType,
    FacilityRegulationStatus,
    RegulationStatus,
    RegulatoryBodyUser,
    FacilityOperationState,
    FacilityUpdates
)

from ..serializers import (
    FacilityApprovalSerializer,
    FacilityUpgradeSerializer,
    FacilityTypeSerializer,
    FacilityRegulationStatusSerializer,
    RegulationStatusSerializer,
    RegulatoryBodyUserSerializer,
    FacilityOperationStateSerializer,
    FacilityUpdatesSerializer
)

from ..filters import (
    FacilityTypeFilter,
    FacilityUpgradeFilter,
    FacilityApprovalFilter,
    FacilityRegulationStatusFilter,
    RegulationStatusFilter,
    RegulatoryBodyUserFilter,
    FacilityOperationStateFilter,
    FacilityUpdatesFilter
)


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


class RegulatoryBodyUserListView(generics.ListCreateAPIView):
    """
    Lists and creates a regulatory body's users
    """
    queryset = RegulatoryBodyUser.objects.all()
    serializer_class = RegulatoryBodyUserSerializer
    filter_class = RegulatoryBodyUserFilter
    ordering_fields = ('regulatory_body', 'user')


class RegulatoryBodyUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a single regulatory body user
    """
    serializer_class = RegulatoryBodyUserSerializer
    queryset = RegulatoryBodyUser.objects.all()


class FacilityUpdatesListView(generics.ListCreateAPIView):
    """
    Lists and creates facility updates
    """
    queryset = FacilityUpdates.objects.all()
    serializer_class = FacilityUpdatesSerializer
    filter_class = FacilityUpdatesFilter
    ordering_fields = ('facility', 'approved')


class FacilityUpdatesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a single facility update
    """
    queryset = FacilityUpdates.objects.all()
    serializer_class = FacilityUpdatesSerializer
