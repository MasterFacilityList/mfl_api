from rest_framework import generics
from common.views import AuditableDetailViewMixin
from common.utilities import CustomRetrieveUpdateDestroyView

from ..models import (
    FacilityStatus,
    OwnerType,
    Officer,
    JobTitle,
    RegulatingBodyContact,
    RegulatingBody
)

from ..serializers import (
    FacilityStatusSerializer,
    OwnerTypeSerializer,
    OfficerSerializer,
    RegulatingBodyContactSerializer,
    JobTitleSerializer,
    RegulatingBodySerializer

)

from ..filters import (
    FacilityStatusFilter,
    OwnerTypeFilter,
    OfficerFilter,
    JobTitleFilter,
    RegulatingBodyContactFilter,
    RegulatingBodyFilter

)


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
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
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
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
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
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
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
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
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
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular owner type
    """
    queryset = OwnerType.objects.all()
    serializer_class = OwnerTypeSerializer


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


class RegulatingBodyContactDetailView(CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular regulatory body contact.
    """
    queryset = RegulatingBodyContact.objects.all()
    serializer_class = RegulatingBodyContactSerializer
