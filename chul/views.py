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


class FilterCommunityUnitsMixin(object):
    def get_queryset(self, *args, **kwargs):
        custom_queryset = kwargs.pop('custom_queryset', None)
        if hasattr(custom_queryset, 'count'):
            self.queryset = custom_queryset

        if not self.request.user.has_perm(
                "facilities.view_unpublished_facilities"):
            self.queryset = self.queryset.filter(facility__is_published=True)

        if not self.request.user.has_perm(
                "chul.view_rejected_chus"):
            self.queryset = self.queryset.filter(is_approved=True)

        if self.request.user.is_national:
            self.queryset = self.queryset

        if self.request.user.county:
            self.queryset = self.queryset.filter(
                facility__ward__constituency__county=self.request.user.county)

        if self.request.user.constituency:
            self.queryset = self.queryset.filter(
                facility__ward__constituency=self.request.user.constituency)

        return self.queryset

    def filter_queryset(self, queryset):
        """
        Overridden in order to constrain search results to what a user should
        see.
        """
        queryset = super(FilterCommunityUnitsMixin, self).filter_queryset(
            queryset)
        return self.get_queryset(custom_queryset=queryset)


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


class CommunityHealthUnitListView(
        FilterCommunityUnitsMixin, generics.ListCreateAPIView):
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
