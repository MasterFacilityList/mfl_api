from django.contrib.auth.models import AnonymousUser

from rest_framework import generics
from rest_framework import status
from rest_framework.views import Response

from common.views import AuditableDetailViewMixin
from common.utilities import CustomRetrieveUpdateDestroyView


from ..models import (
    Facility,
    FacilityUnit,
    OfficerContact,
    Owner,
    FacilityContact,
    FacilityOfficer,
    FacilityUnitRegulation
)

from ..serializers import (
    FacilitySerializer,
    FacilityUnitSerializer,
    OfficerContactSerializer,
    OwnerSerializer,
    FacilityListSerializer,
    FacilityDetailSerializer,
    FacilityContactSerializer,
    FacilityOfficerSerializer,
    FacilityUnitRegulationSerializer
)

from ..filters import (
    FacilityFilter,
    FacilityUnitFilter,
    OfficerContactFilter,
    OwnerFilter,
    FacilityContactFilter,
    FacilityOfficerFilter,
    FacilityUnitRegulationFilter

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
        if not isinstance(self.request.user, AnonymousUser):
            if not self.request.user.is_national and self.request.user.county \
                    and hasattr(self.queryset.model, 'ward'):
                return self.queryset.filter(
                    ward__constituency__county=self.request.user.county)

            elif self.request.user.regulator and hasattr(
                    self.queryset.model, 'regulatory_body'):
                return self.queryset.filter(
                    regulatory_body=self.request.user.regulator)
            elif self.request.user.is_national and not \
                    self.request.user.county:
                return self.queryset
            else:
                return self.queryset
        else:
            return self.queryset


class FacilityUnitsListView(generics.ListCreateAPIView):
    """
    Lists and creates facility units

    facility -- A facility's pk
    name -- Name of a facility unit
    description -- Description of a facility unit
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityUnit.objects.all()
    serializer_class = FacilityUnitSerializer
    ordering_fields = ('name', 'facility', 'regulating_body',)
    filter_class = FacilityUnitFilter


class FacilityUnitDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular facility unit's detail
    """
    queryset = FacilityUnit.objects.all()
    serializer_class = FacilityUnitSerializer


class OfficerContactListView(generics.ListCreateAPIView):
    """
    Lists and creates officer contacts

    officer -- An officer's pk
    contact --  A contacts pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = OfficerContact.objects.all()
    serializer_class = OfficerContactSerializer
    ordering_fields = ('officer', 'contact',)
    filter_class = OfficerContactFilter


class OfficerContactDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular officer contact detail
    """
    queryset = OfficerContact.objects.all()
    serializer_class = OfficerContactSerializer


class OwnerListView(generics.ListCreateAPIView):
    """
    List and creates a list of owners

    name -- The name of an owner
    description -- The description of an owner
    abbreviation -- The abbreviation of an owner
    code --  The code of an owner
    owner_type -- An owner-type's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_class = OwnerFilter
    ordering_fields = ('name', 'code', 'owner_type',)


class OwnerDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular owner's details
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class FacilityListView(QuerysetFilterMixin, generics.ListCreateAPIView):
    """
    Lists and creates facilities

    name -- The name of the facility
    code -- A list of comma separated facility codes (one or more)
    description -- The description of the facility
    facility_type -- A list of comma separated facility type's pk
    operation_status -- A list of comma separated operation statuses pks
    ward -- A list of comma separated ward pks (one or more)
    ward_code -- A list of comma separated ward codes
    county_code -- A list of comma separated county codes
    constituency_code -- A list of comma separated constituency codes
    county -- A list of comma separated county pks
    constituency -- A list of comma separated constituency pks
    owner -- A list of comma separated owner pks
    number_of_beds -- A list of comma separated integers
    number_of_cots -- A list of comma separated integers
    open_whole_day -- Boolean True/False
    is_classified -- Boolean True/False
    is_published -- Boolean True/False
    is_regulated -- Boolean True/False
    service_category -- A service category's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_class = FacilityFilter
    ordering_fields = (
        'name', 'code', 'number_of_beds', 'number_of_cots', 'operation_status',
        'ward', 'owner',
    )


class FacilityListReadOnlyView(
        QuerysetFilterMixin, AuditableDetailViewMixin, generics.ListAPIView):
    """
    Returns a slimmed payload of the facility.
    """
    queryset = Facility.objects.all()
    serializer_class = FacilityListSerializer
    filter_class = FacilityFilter
    ordering_fields = (
        'code', 'name', 'county', 'constituency', 'facility_type_name',
        'owner_type_name', 'is_published'
    )


class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class FacilityDetailView(
        QuerysetFilterMixin,
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular facility
    """
    queryset = Facility.objects.all()
    serializer_class = FacilityDetailSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FacilityContactListView(generics.ListCreateAPIView):
    """
    Lists and creates facility contacts

    facility -- A facility's pk
    contact -- A contact's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityContact.objects.all()
    serializer_class = FacilityContactSerializer
    filter_class = FacilityContactFilter
    ordering_fields = ('facility', 'contact',)


class FacilityContactDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular facility contact
    """
    queryset = FacilityContact.objects.all()
    serializer_class = FacilityContactSerializer


class FacilityOfficerListView(
        AuditableDetailViewMixin, generics.ListCreateAPIView):
    serializer_class = FacilityOfficerSerializer
    queryset = FacilityOfficer.objects.all()
    filter_class = FacilityOfficerFilter
    ordering_fields = (
        'name', 'id_number', 'registration_number',
        'facility_name')


class FacilityOfficerDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    serializer_class = FacilityOfficerSerializer
    queryset = FacilityOfficer.objects.all()


class FacilityUnitRegulationListView(
        AuditableDetailViewMixin, generics.ListCreateAPIView):
    queryset = FacilityUnitRegulation.objects.all()
    serializer_class = FacilityUnitRegulationSerializer
    filter_class = FacilityUnitRegulationFilter
    ordering_fields = ('facility_unit', 'regulation_status')


class FacilityUnitRegulationDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    queryset = FacilityUnitRegulation.objects.all()
    serializer_class = FacilityUnitRegulationSerializer
