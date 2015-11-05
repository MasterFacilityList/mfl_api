from django.template import loader, Context

from django.utils import timezone
from django.views.decorators.cache import never_cache

from rest_framework import generics

from common.views import AuditableDetailViewMixin, DownloadPDFMixin
from common.utilities import CustomRetrieveUpdateDestroyView
from chul.models import CommunityHealthUnit

from ..models import (
    FacilityApproval,
    FacilityUpgrade,
    Facility,
    FacilityType,
    FacilityRegulationStatus,
    RegulationStatus,
    RegulatoryBodyUser,
    FacilityOperationState,
    FacilityUpdates,
    FacilityService,
    FacilityContact,
    FacilityOfficer
)

from ..serializers import (
    FacilityApprovalSerializer,
    FacilityUpgradeSerializer,
    FacilityTypeSerializer,
    FacilityRegulationStatusSerializer,
    RegulationStatusSerializer,
    RegulatoryBodyUserSerializer,
    FacilityOperationStateSerializer,
    FacilityUpdatesSerializer,
    FacilitySerializer
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
        CustomRetrieveUpdateDestroyView):

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
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

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
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular regulation status
    """
    queryset = RegulationStatus.objects.all()
    serializer_class = RegulationStatusSerializer


class FacilityPDFDownloadView(DownloadPDFMixin, generics.RetrieveAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    @never_cache
    def get(self, request, *args, **kwargs):
        facility = self.get_object()
        template = loader.get_template(self.report_tpl)
        report_date = timezone.now().isoformat()
        services = FacilityService.objects.filter(facility=facility)
        contacts = FacilityContact.objects.filter(facility=facility)
        officers = FacilityOfficer.objects.filter(facility=facility)
        chus = CommunityHealthUnit.objects.filter(facility=facility)
        regulating_bodies = FacilityRegulationStatus.objects.filter(
            facility=facility)
        regulating_body = regulating_bodies[0] if regulating_bodies else None

        ctx_data = {
            "report_date": report_date,
            "facility": facility,
            "services": services,
            "contacts": contacts,
            "officers": officers,
            "chus": chus,
            "regulating_body": regulating_body
        }

        if request.user.has_perm('facilities.view_facility_coordinates'):
            try:
                facility_coordinates = facility.facility_coordinates_through
            except:
                facility_coordinates = None

            ctx_data["longitude"] = (
                facility_coordinates.simplify_coordinates.get('coordinates')[0]
                if facility_coordinates else None
            )
            ctx_data["latitude"] = (
                facility_coordinates.simplify_coordinates.get('coordinates')[1]
                if facility_coordinates else None
            )
            ctx_data["facility_coordinates"] = facility_coordinates

        file_name = '{} ({})'.format(
            facility.name.lower(), self.filename_padding
        )
        return self.download_file(
            template.render(Context(ctx_data)), file_name
        )


class FacilityCoverTemplate(FacilityPDFDownloadView):
    report_tpl = 'cover_report.html'
    filename_padding = 'cover report'


class FacilityInspectionReport(FacilityPDFDownloadView):
    report_tpl = 'inspection_report.txt'
    filename_padding = 'inspection report'


class FacilityDetailTemplate(FacilityPDFDownloadView):
    report_tpl = 'facility_details.html'
    filename_padding = 'facility details'


class FacilityCorrectionTemplate(FacilityPDFDownloadView):
    report_tpl = 'correction_template.html'
    filename_padding = 'correction template'


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


class FacilityUpgradeDetailView(CustomRetrieveUpdateDestroyView):

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


class FacilityOperationStateDetailView(CustomRetrieveUpdateDestroyView):

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


class FacilityApprovalDetailView(CustomRetrieveUpdateDestroyView):

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


class RegulatoryBodyUserDetailView(CustomRetrieveUpdateDestroyView):

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


class FacilityUpdatesDetailView(CustomRetrieveUpdateDestroyView):

    """
    Retrieves a single facility update
    """
    queryset = FacilityUpdates.objects.all()
    serializer_class = FacilityUpdatesSerializer
