from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework import response

from ..models import (
    Contact,
    PhysicalAddress,
    County,
    Ward,
    Constituency,
    ContactType,
    UserCounty,
    UserContact,
    Town,
    UserConstituency
)
from facilities.models import(
    FacilityStatus,
    ServiceCategory,
    FacilityType,
    OwnerType,
    Owner
)
from ..serializers import (
    ContactSerializer,
    CountySerializer,
    CountyDetailSerializer,
    WardSerializer,
    WardDetailSerializer,
    PhysicalAddressSerializer,
    ConstituencySerializer,
    ConstituencyDetailSerializer,
    ConstituencySlimDetailSerializer,
    CountySlimDetailSerializer,
    WardSlimDetailSerializer,
    ContactTypeSerializer,
    UserCountySerializer,
    UserContactSerializer,
    TownSerializer,
    FilteringSummariesSerializer,
    UserConstituencySerializer
)
from ..filters import (
    ContactTypeFilter,
    ContactFilter,
    PhysicalAddressFilter,
    CountyFilter,
    ConstituencyFilter,
    WardFilter,
    UserCountyFilter,
    UserContactFilter,
    TownFilter,
    UserConstituencyFilter
)
from .shared_views import AuditableDetailViewMixin
from ..utilities import CustomRetrieveUpdateDestroyView


class ContactView(generics.ListCreateAPIView):
    """
    Lists and creates contacts

    contact_type  --  A contact type pk
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    ordering_fields = ('contact_type', 'contact',)
    filter_class = ContactFilter


class ContactDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a patricular contact
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class PhysicalAddressView(generics.ListCreateAPIView):
    """
    Lists and creaates physical addresses

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = PhysicalAddress.objects.all()
    serializer_class = PhysicalAddressSerializer
    ordering_fields = ('town', )
    filter_class = PhysicalAddressFilter


class PhysicalAddressDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a patricular physical address
    """
    queryset = PhysicalAddress.objects.all()
    serializer_class = PhysicalAddressSerializer


class CountyView(generics.ListCreateAPIView):
    """
    Lists and creates counties

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = County.objects.all()
    serializer_class = CountySerializer
    ordering_fields = ('name', 'code',)
    filter_class = CountyFilter


class CountyDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a patricular county including the county boundary
    and its facility coordinates
    """
    queryset = County.objects.all()
    serializer_class = CountyDetailSerializer


class CountySlimDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves the primary details of a county
    """
    queryset = County.objects.all()
    serializer_class = CountySlimDetailSerializer


class WardView(generics.ListCreateAPIView):
    """
    Lists and creates wards

    county  -- A county pk
    constituency --  A constituency pk
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    filter_class = WardFilter
    ordering_fields = ('name', 'code', 'constituency',)


class WardDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a patricular ward details including ward boundaries
    and facility coordinates
    """
    queryset = Ward.objects.all()
    serializer_class = WardDetailSerializer


class WardSlimDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a patricular ward primary details
    """
    queryset = Ward.objects.all()
    serializer_class = WardSlimDetailSerializer


class ConstituencyView(generics.ListCreateAPIView):
    """
    Lists and creates constituencies

    county  -- A county pk
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    filter_class = ConstituencyFilter
    ordering_fields = ('name', 'code', 'county',)


class ConstituencyDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a  patricular constituency
    """
    queryset = Constituency.objects.all()
    serializer_class = ConstituencyDetailSerializer


class ConstituencySlimDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySlimDetailSerializer


class ContactTypeListView(generics.ListCreateAPIView):
    """
    Lists and creates contact types

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    ordering_fields = ('name', )
    filter_class = ContactTypeFilter


class ContactTypeDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a patricular contact type
    """
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer


class UserCountyView(generics.ListCreateAPIView):
    """
    Lists and creates links between users and counties

    user -- A user pk
    county --  A county pk

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = UserCounty.objects.all()
    serializer_class = UserCountySerializer
    filter_class = UserCountyFilter
    ordering_fields = ('user', 'county',)


class UserCountyDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a patricular link between a user and a county
    """
    queryset = UserCounty.objects.all()
    serializer_class = UserCountySerializer


class UserContactListView(generics.ListCreateAPIView):
    """
    Lists and creates user contacts

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer
    filter_class = UserContactFilter
    ordering_fields = ('user', 'contact',)


class UserContactDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a patricular user contact
    """
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer


class TownListView(generics.ListCreateAPIView):
    """
    Lists and creates towns

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    filter_class = TownFilter
    ordering_fields = ('name', )


class TownDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a patricular town detail
    """
    queryset = Town.objects.all()
    serializer_class = TownSerializer


class FilteringSummariesView(views.APIView):
    """
        Retrieves filtering summaries
    """
    serializer_cls = FilteringSummariesSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        fields = request.query_params.get('fields', None)
        fields_model_mapping = {
            'county': County,
            'facility_type': FacilityType,
            'constituency': Constituency,
            'ward': Ward,
            'operation_status': FacilityStatus,
            'service_category': ServiceCategory,
            'owner_type': OwnerType,
            'owner': Owner
        }
        if fields:
            resp = {}
            for key in fields.split(","):
                if key in fields_model_mapping:
                    resp[key] = fields_model_mapping[key].objects.values(
                        'id', 'name').distinct()
            res = self.serializer_cls(data=resp).initial_data
        else:
            res = {}
        return response.Response(res)


class UserConstituencyListView(generics.ListCreateAPIView):
    serializer_class = UserConstituencySerializer
    filter_class = UserConstituencyFilter
    queryset = UserConstituency.objects.all()
    ordering_fields = ('user', 'constituency')


class UserConstituencyDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserConstituencySerializer
    queryset = UserConstituency.objects.all()
