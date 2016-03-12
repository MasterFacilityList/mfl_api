from django.template import loader, Context
from django.utils import timezone
from django.views.decorators.cache import never_cache
from rest_framework import generics
from common.views import AuditableDetailViewMixin, DownloadPDFMixin
from common.models import UserConstituency, UserCounty, UserSubCounty
from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact,
    CHUService,
    CHURating,
    ChuUpdateBuffer
)

from .serializers import (
    CommunityHealthUnitSerializer,
    CommunityHealthWorkerSerializer,
    CommunityHealthWorkerContactSerializer,
    StatusSerializer,
    CommunityHealthUnitContactSerializer,
    CHUServiceSerializer,
    CHURatingSerializer,
    ChuUpdateBufferSerializer
)

from .filters import (
    CommunityHealthUnitFilter,
    CommunityHealthWorkerFilter,
    CommunityHealthWorkerContactFilter,
    StatusFilter,
    CommunityHealthUnitContactFilter,
    CHUServiceFilter,
    CHURatingFilter,
    ChuUpdateBufferFilter
)


class FilterCommunityUnitsMixin(object):

    def get_queryset(self, *args, **kwargs):
        custom_queryset = kwargs.pop('custom_queryset', None)
        if hasattr(custom_queryset, 'count'):
            self.queryset = custom_queryset

        if not self.request.user.has_perm(
                "facilities.view_unpublished_facilities"):
            self.queryset = self.queryset.filter(facility__approved=True)

        if not self.request.user.has_perm(
                "chul.view_rejected_chus"):
            self.queryset = self.queryset.filter(is_approved=True)

        if self.request.user.is_national:
            self.queryset = self.queryset

        if self.request.user.county:
            self.queryset = self.queryset.filter(
                facility__ward__constituency__county__in=[
                    uc.county for uc in UserCounty.objects.filter(
                        user=self.request.user)
                ])

        if self.request.user.constituency:
            self.queryset = self.queryset.filter(
                facility__ward__constituency__in=[
                    uc.constituency for uc in UserConstituency.objects.filter(
                        user=self.request.user)
                ])

        if self.request.user.sub_county:
            self.queryset = self.queryset.filter(
                facility__ward__sub_county__in=[
                    us.sub_county for us in UserSubCounty.objects.filter(
                        user=self.request.user)
                ])

        return self.queryset

    def filter_queryset(self, queryset):
        """
        Overridden in order to constrain search results to what a user should
        see.
        """
        if 'search' in self.request.query_params:
            search_term = self.request.query_params.get('search')
            if search_term.isdigit():
                queryset = self.queryset.filter(code=search_term)
            else:
                queryset = super(
                    FilterCommunityUnitsMixin, self).filter_queryset(queryset)
        else:
            queryset = super(
                FilterCommunityUnitsMixin, self).filter_queryset(queryset)

        return self.get_queryset(custom_queryset=queryset)


class CHUServiceListView(generics.ListCreateAPIView):

    """
    Lists and creates statuses

    Created ---  Date the status was Created
    Updated -- Date the status was Updated
    Created_by -- User who created the status
    Updated_by -- User who updated the status
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    name  --  Name of the service
    description -- The description of the service
    """
    queryset = CHUService.objects.all()
    serializer_class = CHUServiceSerializer
    filter_class = CHUServiceFilter
    ordering_fields = ('name', 'description', )


class CHUServiceDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):

    """
    Retrieves a particular status
    """
    queryset = CHUService.objects.all()
    serializer_class = CHUServiceSerializer


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
    Retrieves a particular community health_worker contact

    health_worker -- A community health worker
    contact -- A contact
    """
    queryset = CommunityHealthWorkerContact.objects.all()
    serializer_class = CommunityHealthWorkerContactSerializer


class CHURatingListView(AuditableDetailViewMixin, generics.ListCreateAPIView):

    """Lists and creates community health unit ratings

    chu -- A community health unit
    rating -- The rating given
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = CHURating.objects.all()
    serializer_class = CHURatingSerializer
    filter_class = CHURatingFilter
    ordering_fields = ('chu', )


class CHURatingDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):

    """Retrieves, updates and deletes a community health unit's rating"""
    queryset = CHURating.objects.all()
    serializer_class = CHURatingSerializer


class ChuUpdateBufferListView(
        AuditableDetailViewMixin, generics.ListCreateAPIView):
    queryset = ChuUpdateBuffer.objects.all()
    serializer_class = ChuUpdateBufferSerializer
    filter_class = ChuUpdateBufferFilter
    ordering_fields = ('health_unit', )


class ChuUpdateBufferDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ChuUpdateBuffer.objects.all()
    serializer_class = ChuUpdateBufferSerializer


class CHUDetailReport(DownloadPDFMixin, generics.RetrieveAPIView):
    queryset = CommunityHealthUnit.objects.all()
    serializer_class = CommunityHealthUnitSerializer

    @never_cache
    def get(self, *args, **kwargs):
        report_date = timezone.now().isoformat()
        chu = self.get_object()
        context = Context({
            "chu": self.get_serializer(instance=chu).data,
            "report_date": report_date
        })
        template = loader.get_template("chu_details.html")
        return self.download_file(template.render(context), chu.name)
