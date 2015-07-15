from django.contrib.auth.models import AnonymousUser

from rest_framework import generics
from rest_framework import status
from rest_framework.views import Response, APIView

from common.views import AuditableDetailViewMixin
from common.utilities import CustomRetrieveUpdateDestroyView
from common.models import Contact, ContactType


from ..models import (
    Facility,
    FacilityUnit,
    OfficerContact,
    Owner,
    FacilityContact,
    FacilityOfficer,
    FacilityUnitRegulation,
    JobTitle,
    Officer
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
            elif self.request.user.constituency and hasattr(
                    self.queryset.model, 'ward'):
                return self.queryset.filter(
                    ward__constituency=self.request.user.constituency)
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
        'name', 'code', 'number_of_beds', 'number_of_cots',
        'operation_status', 'ward', 'owner',
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


class CustomFacilityOfficerView(APIView):
    """
    A custom view for creating facility officers.
    Make it less painful to create facility officers via the frontend.
    """
    def _validate_required_fields(self, data):
        facility_id = data.get('facility_id', None)
        name = data.get('name', None)
        title = data.get('title', None)
        id_number = data.get('id_no', None)
        if not facility_id or not name or not title or not id_number:
            error_message = "Facility id , name, ID number and"\
                            "job title of the officer are "\
                            "required"
            return error_message

    def _validate_facility(self, data):
        try:
            Facility.objects.get(id=data.get('facility_id', None))
        except Facility.DoesNotExist:
            error_message = {
                "facility": "Facility provided does not exist"
            }
            return error_message

    def _validate_job_titles(self, data):
        try:
            JobTitle.objects.get(id=data['title'])
        except JobTitle.DoesNotExist:
            error_message = {
                "job title": "JobTitle with id {} does not exist".format(
                    data['title'])
            }
            return error_message

    def data_is_valid(self, data):
        errors = [
            self._validate_required_fields(data),
            self._validate_facility(data),
            self._validate_job_titles(data)
        ]
        errors = [error for error in errors if error is not None]
        if errors:
            return errors
        else:
            return True

    def _inject_creating_user(self, attributes_dict):
        attributes_dict['created_by'] = self.request.user
        attributes_dict['updated_by'] = self.request.user
        return attributes_dict

    def _create_contacts(self, data):
        contacts = data.get('contacts', None)
        created_contacts = []
        if contacts:
            for contact in contacts:

                contact_type = ContactType.objects.get(
                    id=contact.get('type'))
                contact_dict = {
                    "contact_type": contact_type,
                    "contact": contact.get('contact')
                }
                contact_dict = self._inject_creating_user(contact_dict)
                created_contacts.append(Contact.objects.create(**contact_dict))
        return created_contacts

    def _create_facility_officer(self, data):
        facility = Facility.objects.get(id=data['facility_id'])
        job_title = JobTitle.objects.get(id=data['title'])

        officer_dict = {
            "name": data['name'],
            "job_title": job_title,
        }
        officer_dict = self._inject_creating_user(officer_dict)

        id_no = data.get('id_no', None)
        reg_no = data.get('reg_no', None)
        officer_dict['id_number'] = id_no if id_no else None
        officer_dict['registration_number'] = reg_no if reg_no else None

        officer = Officer.objects.create(**officer_dict)
        facility_officer_dict = {
            "facility": facility,
            "officer": officer
        }
        facility_officer_dict = self._inject_creating_user(
            facility_officer_dict)
        facility_officer = FacilityOfficer.objects.create(
            **facility_officer_dict)

        # link the officer to the contacts
        created_contacts = self._create_contacts(data)
        for contact in created_contacts:
            contact_dict = {
                "officer": officer,
                "contact": contact
            }
            contact_dict = self._inject_creating_user(contact_dict)
            OfficerContact.objects.create(**contact_dict)
        return facility_officer

    def post(self, *args, **kwargs):
        data = self.request.DATA
        valid_data = self.data_is_valid(data)

        if valid_data is not True:

            return Response(
                {"detail": valid_data}, status=status.HTTP_400_BAD_REQUEST)
        else:
            facility_officer = self._create_facility_officer(data)
            serialized_officer = FacilityOfficerSerializer(
                facility_officer).data
            return Response(serialized_officer, status=status.HTTP_201_CREATED)

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
