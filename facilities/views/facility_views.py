from django.contrib.auth.models import AnonymousUser

from rest_framework import generics
from rest_framework import status
from rest_framework.views import Response, APIView

from common.views import AuditableDetailViewMixin
from common.utilities import CustomRetrieveUpdateDestroyView


from ..models import (
    Facility,
    FacilityUnit,
    OfficerContact,
    Owner,
    FacilityContact,
    FacilityOfficer,
    FacilityUnitRegulation,
    KephLevel,
    OptionGroup,
    FacilityLevelChangeReason
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
    FacilityUnitRegulationSerializer,
    KephLevelSerializer,
    OptionGroupSerializer,
    CreateFacilityOfficerMixin,
    FacilityLevelChangeReasonSerializer
)

from ..filters import (
    FacilityFilter,
    FacilityUnitFilter,
    OfficerContactFilter,
    OwnerFilter,
    FacilityContactFilter,
    FacilityOfficerFilter,
    FacilityUnitRegulationFilter,
    KephLevelFilter,
    OptionGroupFilter,
    FacilityLevelChangeReasonFilter

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
                self.queryset = self.queryset.filter(
                    ward__constituency__county=self.request.user.county)

            elif self.request.user.regulator and hasattr(
                    self.queryset.model, 'regulatory_body'):
                self.queryset = self.queryset.filter(
                    regulatory_body=self.request.user.regulator)
            elif self.request.user.is_national and not \
                    self.request.user.county:
                self.queryset = self.queryset
            elif self.request.user.constituency and hasattr(
                    self.queryset.model, 'ward'):
                self.queryset = self.queryset.filter(
                    ward__constituency=self.request.user.constituency)
            else:
                self.queryset = self.queryset
        else:
            self.queryset = self.queryset

        if self.request.user.has_perm("facilities.view_unpublished_facilities") is False and \
                'is_published' in [
                    field.name for field in
                    self.queryset.model._meta.get_fields()]:

            self.queryset = self.queryset.filter(is_published=True)

        if self.request.user.has_perm("facilities.view_unapproved_facilities") \
            is False and 'approved' in [
                field.name for field in
                self.queryset.model._meta.get_fields()]:
            self.queryset = self.queryset.filter(approved=True)

        if self.request.user.has_perm("facilities.view_classified_facilities") is False and \
            'is_classified' in [
                field.name for field in
                self.queryset.model._meta.get_fields()]:
            self.queryset = self.queryset.filter(is_classified=False)

        if self.request.user.has_perm("facilities.view_rejected_facilities") \
            is False and ('rejected' in [
                field.name for field in
                self.queryset.model._meta.get_fields()]):
            self.queryset = self.queryset.filter(rejected=False)

        if self.request.user.has_perm("facilities.view_closed_facilities") is False and \
            'closed' in [
                field.name for field in
                self.queryset.model._meta.get_fields()]:
            self.queryset = self.queryset.filter(closed=False)

        return self.queryset


class FacilityLevelChangeReasonListView(generics.ListCreateAPIView):
    """
    Lists and creates the  generic upgrade and down grade reasons
    reason --   A reason for  upgrade or downgrade
    description -- Description the reason
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityLevelChangeReason.objects.all()
    filter_class = FacilityLevelChangeReasonFilter
    serializer_class = FacilityLevelChangeReasonSerializer
    ordering_fields = ('reason', 'description', 'is_upgrade_reason')


class FacilityLevelChangeReasonDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a single facility level change reason
    """
    queryset = FacilityLevelChangeReason.objects.all()
    serializer_class = FacilityLevelChangeReasonSerializer


class KephLevelListView(generics.ListCreateAPIView):
    """
    Lists and creates the  Kenya Essential Package for health (KEPH)
    name -- Name of a level 1
    description -- Description the KEPH
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = KephLevel.objects.all()
    filter_class = KephLevelFilter
    serializer_class = KephLevelSerializer
    ordering_fields = ('name', 'value', 'description')


class KephLevelDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a single KEPH level
    """
    queryset = KephLevel.objects.all()
    serializer_class = KephLevelSerializer


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
        'name', 'code', 'number_of_beds', 'number_of_cots',
        'operation_status', 'ward', 'owner',
    )


class FacilityListReadOnlyView(QuerysetFilterMixin, generics.ListAPIView):
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
        user_id = request.user
        del user_id
        request.data['updated_by_id'] = request.user.id
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


class FacilityOfficerListView(generics.ListCreateAPIView):
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


class FacilityUnitRegulationListView(generics.ListCreateAPIView):
    queryset = FacilityUnitRegulation.objects.all()
    serializer_class = FacilityUnitRegulationSerializer
    filter_class = FacilityUnitRegulationFilter
    ordering_fields = ('facility_unit', 'regulation_status')


class FacilityUnitRegulationDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    queryset = FacilityUnitRegulation.objects.all()
    serializer_class = FacilityUnitRegulationSerializer


class CustomFacilityOfficerView(CreateFacilityOfficerMixin, APIView):
    """
    A custom view for creating facility officers.
    Make it less painful to create facility officers via the frontend.
    """

    def post(self, *args, **kwargs):
        data = self.request.data
        self.user = self.request.user
        created_officer = self.create_officer(data)

        if created_officer.get("created") is not True:

            return Response(
                {"detail": created_officer.get("detail")},
                status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response(
                created_officer.get("detail"), status=status.HTTP_201_CREATED)

    def get(self, *args, **kwargs):
        facility = Facility.objects.get(id=kwargs['facility_id'])
        facility_officers = FacilityOfficer.objects.filter(facility=facility)
        serialized_officers = FacilityOfficerSerializer(
            facility_officers, many=True).data
        return Response(serialized_officers)

    def delete(self, *args, **kwargs):
        officer = FacilityOfficer.objects.get(id=kwargs['pk'])
        officer.deleted = True
        officer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OptionGroupListView(generics.ListCreateAPIView):
    queryset = OptionGroup.objects.all()
    serializer_class = OptionGroupSerializer
    filter_class = OptionGroupFilter
    ordering_fields = ('name', )


class OptionGroupDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    queryset = OptionGroup.objects.all()
    serializer_class = OptionGroupSerializer
