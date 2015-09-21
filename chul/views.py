from rest_framework import generics
from common.views import AuditableDetailViewMixin
from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact
)

from .serializers import (
    CommunityHealthUnitSerializer,
    CommunityHealthWorkerSerializer,
    CommunityHealthWorkerContactSerializer,
    StatusSerializer,
    CommunityHealthUnitContactSerializer
)

from .filters import (
    CommunityHealthUnitFilter,
    CommunityHealthWorkerFilter,
    CommunityHealthWorkerContactFilter,
    StatusFilter,
    CommunityHealthUnitContactFilter
)


class StatusListView(generics.ListCreateAPIView):
    """
    Lists and creates statuses

    Created ---  Date the status was Created
    Updated -- Date the status was Updated
    Created_by -- User who created the status
    Updated_by -- User who updated the status
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_class = StatusFilter
    ordering_fields = ('name', 'description', )


class StatusDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular status
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class CommunityHealthUnitContactListView(generics.ListCreateAPIView):
    """
    Lists and creates community unit contacts

    health_unit -- A community health unit pk
    contact  -- A contact id
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = CommunityHealthUnitContact.objects.all()
    serializer_class = CommunityHealthUnitContactSerializer
    filter_class = CommunityHealthUnitContactFilter
    ordering_fields = ('health_unit', 'contact', )


class CommunityHealthUnitContactDetailView(
        AuditableDetailViewMixin,
        generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular community health unit contact
    """
    queryset = CommunityHealthUnitContact.objects.all()
    serializer_class = CommunityHealthUnitContactSerializer


class CommunityHealthUnitListView(generics.ListCreateAPIView):
    """
    Lists and creates community health units

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the status
    Updated_by -- User who updated the status
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = CommunityHealthUnit.objects.all()
    serializer_class = CommunityHealthUnitSerializer
    filter_class = CommunityHealthUnitFilter
    ordering_fields = ('name', 'facility',)


class CommunityHealthUnitDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular community health  unit
    """
    queryset = CommunityHealthUnit.objects.all()
    serializer_class = CommunityHealthUnitSerializer


class CommunityHealthWorkerListView(generics.ListCreateAPIView):
    """
    Lists and creates community health workers

    health_unit -- A community health  unit
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = CommunityHealthWorker.objects.all()
    serializer_class = CommunityHealthWorkerSerializer
    filter_class = CommunityHealthWorkerFilter
    ordering_fields = ('first_name', 'last_name', 'username',)


class CommunityHealthWorkerDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a particular health worker
    """
    queryset = CommunityHealthWorker.objects.all()
    serializer_class = CommunityHealthWorkerSerializer


class CommunityHealthWorkerContactListView(generics.ListCreateAPIView):
    """
    Lists and creates community health worker contacts

    health_worker -- A community health worker
    contact -- A contact
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = CommunityHealthWorkerContact.objects.all()
    serializer_class = CommunityHealthWorkerContactSerializer
    filter_class = CommunityHealthWorkerContactFilter
    ordering_fields = ('contact',)


class CommunityHealthWorkerContactDetailView(
        AuditableDetailViewMixin,
        generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a paritular community health_worker contact

    health_worker -- A community health worker
    contact -- A contact
    """
    queryset = CommunityHealthWorkerContact.objects.all()
    serializer_class = CommunityHealthWorkerContactSerializer
