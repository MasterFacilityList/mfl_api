from django.template import loader, Context
from django.http import HttpResponse
from django.utils import timezone
import os
from django.core.servers.basehttp import FileWrapper
from django.utils.encoding import smart_str
from django.views.decorators.cache import never_cache
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import generics

from weasyprint import HTML

from common.views import AuditableDetailViewMixin
from common.utilities import CustomRetrieveUpdateDestroyView

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


class DownloadPDFMixin(object):
    def download_file(self, doc, file_name):
        doc_file_name = 'temp'
        file_path = os.path.join(settings.BASE_DIR, file_name)
        doc_file_path = os.path.join(settings.BASE_DIR, doc_file_name)
        writting_file = open(doc_file_path, 'w')
        writting_file.write(doc)
        writting_file.close()
        HTML(doc_file_path).write_pdf(file_path)
        download_file = open(file_path)
        response = HttpResponse(
            FileWrapper(download_file), content_type='application/pdf')
        response[
            'Content-Disposition'] = 'attachment; filename='.format(
            os.path.basename(file_path)
        )
        response['X-Sendfile'] = smart_str(file_path)
        os.remove(file_path)
        os.remove(doc_file_path)
        return response


class FacilityInspectionReport(DownloadPDFMixin, APIView):
    queryset = Facility.objects.all()

    @never_cache
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
        file_name = '{}_inspection_report'.format(facility.name)
        return self.download_file(template.render(context), file_name)


class FacilityCoverTemplate(DownloadPDFMixin, APIView):
    queryset = Facility.objects.all()

    def get(self, request, facility_id, *args, **kwargs):
        return self.get_cover_report(facility_id)

    @never_cache
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
        file_name = '{}_cover_report'.format(facility.name)
        return self.download_file(template.render(context), file_name)


class FacilityCorrectionTemplate(DownloadPDFMixin, APIView):
    queryset = Facility.objects.all()

    @never_cache
    def get(self, request, facility_id, *args, **kwargs):
        facility = Facility.objects.get(pk=facility_id)
        template = loader.get_template('correction_template.txt')
        request_date = timezone.now().isoformat()
        context = Context(
            {
                "request_date": request_date,
                "facility": facility
            }
        )
        doc = template.render(context)
        file_name = '{}_correction_template.pdf'.format(facility.name)
        return self.download_file(doc, file_name)


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
