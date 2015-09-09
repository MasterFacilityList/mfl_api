import json

from django.utils import timezone
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.models import Contact, ContactType

from common.serializers import (
    AbstractFieldsMixin,
    ContactSerializer
)


from ..models import (
    OwnerType,
    Owner,
    JobTitle,
    Officer,
    OfficerContact,
    FacilityStatus,
    FacilityType,
    RegulatingBody,
    RegulationStatus,
    Facility,
    FacilityRegulationStatus,
    FacilityContact,
    FacilityUnit,
    ServiceCategory,
    Option,
    Service,
    FacilityService,
    FacilityServiceRating,
    FacilityApproval,
    FacilityOperationState,
    FacilityUpgrade,
    RegulatingBodyContact,
    FacilityOfficer,
    RegulatoryBodyUser,
    FacilityUnitRegulation,
    FacilityUpdates,
    KephLevel,
    OptionGroup,
    FacilityLevelChangeReason
)

from ..utils import CreateFacilityOfficerMixin


class FacilityLevelChangeReasonSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = FacilityLevelChangeReason


class KephLevelSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = KephLevel


class RegulatoryBodyUserSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')
    regulatory_body_name = serializers.ReadOnlyField(
        source='regulatory_body.name')

    class Meta:
        model = RegulatoryBodyUser


class FacilityOfficerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer,):
    facility_name = serializers.ReadOnlyField(source='facility.name')
    officer_name = serializers.ReadOnlyField(source='officer.name')
    id_number = serializers.ReadOnlyField(source='officer.id_number')
    registration_number = serializers.ReadOnlyField(
        source='officer.registration_number')
    job_title = serializers.ReadOnlyField(source='officer.job_title.name')

    class Meta(object):
        model = FacilityOfficer


class RegulatingBodyContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    contact_text = serializers.ReadOnlyField(source='contact.contact')
    contact_type = serializers.ReadOnlyField(
        source='contact.contact_type.name'

    )

    class Meta(object):
        model = RegulatingBodyContact


class FacilityUpgradeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityUpgrade


class FacilityOperationStateSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityOperationState


class FacilityApprovalSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    done_by = serializers.ReadOnlyField(source="created_by.get_full_name")

    class Meta(object):
        model = FacilityApproval


class ServiceCategorySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = ServiceCategory


class OptionSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Option


class ServiceSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True)

    class Meta(object):
        model = Service
        read_only_fields = ('code',)


class FacilityServiceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    service_name = serializers.CharField(read_only=True)
    option_display_value = serializers.CharField(read_only=True)
    average_rating = serializers.ReadOnlyField()
    number_of_ratings = serializers.ReadOnlyField()
    service_has_options = serializers.ReadOnlyField()

    class Meta(object):
        model = FacilityService


class FacilityStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityStatus


class RegulatingBodySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    regulatory_body_type_name = serializers.ReadOnlyField(
        source='regulatory_body_type.name'
    )
    contacts = serializers.ReadOnlyField()
    inlining_errors = []

    def _validate_contacts(self, contacts):
        # the serializer class seems to be caching the errors
        # reinitialize them each time this function is called
        self.inlining_errors = []
        for contact in contacts:
            if 'contact' not in contact:
                self.inlining_errors.append("The contact is missing")
            if 'contact_type' not in contact:
                self.inlining_errors.append("The contact type is missing")
            try:
                ContactType.objects.get(id=contact['contact_type'])
            except (KeyError, ValueError, ContactType.DoesNotExist):
                self.inlining_errors.append(
                    "The contact type provided does not exist")

    def create_contact(self, contact_data):
        try:
            return Contact.objects.get(contact=contact_data["contact"])
        except Contact.DoesNotExist:
            contact = ContactSerializer(
                data=contact_data, context=self.context)
            return contact.save() if contact.is_valid() else \
                self.inlining_errors.append(json.dumps(contact.errors))

    def create_reg_body_contacts(self, instance, contact_data, validated_data):
            contact = self.create_contact(contact_data)
            reg_contact_data = {
                "contact": contact,
                "regulating_body": instance
            }
            audit_data = {
                "created_by_id": self.context['request'].user.id,
                "updated_by_id": self.context['request'].user.id,
                "created": (
                    validated_data['created'] if
                    validated_data.get('created') else timezone.now()),
                "updated": (
                    validated_data['updated'] if
                    validated_data.get('updated') else timezone.now())
            }
            reg_complete_contact_data = reg_contact_data
            reg_complete_contact_data.update(audit_data)

            try:
                RegulatingBodyContact.objects.get(**reg_contact_data)
            except RegulatingBodyContact.DoesNotExist:
                RegulatingBodyContact.objects.create(
                    **reg_complete_contact_data)

    @transaction.atomic
    def create(self, validated_data):
        contacts = self.initial_data.pop('contacts')
        self._validate_contacts(contacts)
        if self.inlining_errors:
            raise ValidationError({
                "contacts": self.inlining_errors
            })
        instance = super(RegulatingBodySerializer, self).create(validated_data)
        for contact in contacts:
            self.create_reg_body_contacts(instance, contact, validated_data)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        contacts = self.initial_data.pop('contacts')
        self._validate_contacts(contacts)
        if self.inlining_errors:
            raise ValidationError({
                "contacts": self.inlining_errors
            })
        for contact in contacts:
            self.create_reg_body_contacts(instance, contact, validated_data)
        return instance

    class Meta(object):
        model = RegulatingBody


class OwnerTypeSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = OwnerType


class FacilityRegulationStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityRegulationStatus


class FacilityTypeSerializer(serializers.ModelSerializer):
    owner_type_name = serializers.ReadOnlyField(source='owner_type.name')

    class Meta(object):
        model = FacilityType


class OfficerContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = OfficerContact


class JobTitleSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = JobTitle


class RegulationStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    next_state_name = serializers.CharField(read_only=True)
    previous_state_name = serializers.CharField(read_only=True)

    class Meta(object):
        model = RegulationStatus


class OfficerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    job_title_name = serializers.ReadOnlyField(source='job_title.name')

    class Meta(object):
        model = Officer


class OwnerSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    owner_type_name = serializers.ReadOnlyField(source='owner_type.name')

    class Meta(object):
        model = Owner
        read_only_fields = ('code',)


class FacilityContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    contact_type = serializers.ReadOnlyField(
        source="contact.contact_type.name")
    actual_contact = serializers.ReadOnlyField(source="contact.contact")

    class Meta(object):
        model = FacilityContact


class FacilityUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    regulation_status = serializers.ReadOnlyField()
    regulating_body_name = serializers.ReadOnlyField(
        source="regulating_body.name")

    class Meta(object):
        model = FacilityUnit


class FacilitySerializer(
        AbstractFieldsMixin, CreateFacilityOfficerMixin,
        serializers.ModelSerializer):
    regulatory_status_name = serializers.CharField(
        read_only=True,
        source='current_regulatory_status')
    facility_type_name = serializers.CharField(read_only=True)
    owner_name = serializers.CharField(read_only=True)
    owner_type_name = serializers.CharField(read_only=True)
    owner_type = serializers.CharField(
        read_only=True, source='owner.owner_type.pk')
    operation_status_name = serializers.CharField(read_only=True)
    county = serializers.CharField(read_only=True)
    constituency = serializers.CharField(read_only=True)
    ward_name = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    facility_services = serializers.ReadOnlyField(
        source="get_facility_services")
    is_approved = serializers.ReadOnlyField()
    has_edits = serializers.ReadOnlyField()
    latest_update = serializers.ReadOnlyField()
    regulatory_body_name = serializers.ReadOnlyField(
        source="regulatory_body.name"
    )
    owner = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Owner.objects.all())
    date_requested = serializers.ReadOnlyField(source='created')
    date_approved = serializers.ReadOnlyField(
        source='latest_approval.created')
    latest_approval_or_rejection = serializers.ReadOnlyField()

    class Meta(object):
        model = Facility

    @transaction.atomic
    def create(self, validated_data):
        # prepare the audit fields
        context = self.context
        audit_data = {
            "created_by_id": self.context['request'].user.id,
            "updated_by_id": self.context['request'].user.id,
            "created": (
                validated_data['created'] if
                validated_data.get('created') else timezone.now()),
            "updated": (
                validated_data['update'] if
                validated_data.get('updated') else timezone.now())
        }

        def inject_audit_fields(dict_a):
            return dict_a.update(audit_data)

        # create new owners
        errors = []

        def create_owner(owner_data):
            inject_audit_fields(owner_data)
            owner = OwnerSerializer(data=owner_data, context=context)
            if owner.is_valid():
                return owner.save()
            else:
                errors.append(json.dumps(owner.errors))

        new_owner = self.initial_data.pop('new_owner', None)
        if new_owner:
            owner = create_owner(new_owner)
            validated_data['owner'] = owner

        if errors:
            raise ValidationError(json.dumps({"detail": errors}))
        facility = super(FacilitySerializer, self).create(validated_data)

        officer_in_charge = self.initial_data.pop("officer_in_charge", None)
        if officer_in_charge:
            self.user = self.context['request'].user
            officer_in_charge['facility_id'] = facility.id
            created_officer = self.create_officer(officer_in_charge)
            errors.append(created_officer.get("detail")) if not \
                created_officer.get("created") else None

        return facility


class FacilityDetailSerializer(FacilitySerializer):
    regulatory_status_name = serializers.CharField(read_only=True)
    facility_services = serializers.ReadOnlyField(
        source="get_facility_services")
    facility_contacts = serializers.ReadOnlyField(
        read_only=True, source="get_facility_contacts")
    coordinates = serializers.ReadOnlyField()
    latest_approval = serializers.ReadOnlyField(source='latest_approval.id')
    boundaries = serializers.ReadOnlyField()
    service_catalogue_active = serializers.ReadOnlyField()
    facility_units = FacilityUnitSerializer(many=True, required=False)
    officer_in_charge = serializers.ReadOnlyField()
    town_name = serializers.ReadOnlyField(source='town.name')

    class Meta(object):
        model = Facility
        exclude = ('attributes', )

    inlining_errors = []

    def inject_audit_fields(self, dict_a, validated_data):
        audit_data = {
            "created_by_id": self.context['request'].user.id,
            "updated_by_id": self.context['request'].user.id,
            "created": (
                validated_data['created'] if
                validated_data.get('created') else timezone.now()),
            "updated": (
                validated_data['update'] if
                validated_data.get('updated') else timezone.now())
        }
        dict_a.update(audit_data)
        return dict_a

    def create_contact(self, contact_data):
            try:
                Contact.objects.get(contact=contact_data["contact"])
            except Contact.DoesNotExist:
                contact = ContactSerializer(
                    data=contact_data, context=self.context)
                return contact.save() if contact.is_valid() else \
                    self.inlining_errors.append(json.dumps(contact.errors))

    def create_facility_contacts(self, instance, contact_data, validated_data):
            contact = self.create_contact(contact_data)
            facility_contact_data = {
                "contact": contact,
                "facility": instance
            }
            facility_contact_data = self.inject_audit_fields(
                facility_contact_data, validated_data)
            try:
                FacilityContact.objects.get(**facility_contact_data)
            except FacilityContact.DoesNotExist:
                FacilityContact.objects.create(**facility_contact_data)

    def create_facility_units(self, instance, unit_data, validated_data):
            unit_data['facility'] = instance.id
            unit_data = self.inject_audit_fields(unit_data, validated_data)
            unit = FacilityUnitSerializer(data=unit_data, context=self.context)
            if unit.is_valid():
                return unit.save()
            else:
                self.inlining_errors.append((json.dumps(unit.errors)))

    def create_facility_services(self, instance, service_data, validated_data):
            service_data['facility'] = instance.id
            service_data = self.inject_audit_fields(
                service_data, validated_data)
            f_service = FacilityServiceSerializer(
                data=service_data, context=self.context)
            f_service.save() if f_service.is_valid() else \
                self.inlining_errors.append(json.dumps(f_service.errors))

    @transaction.atomic
    def update(self, instance, validated_data):
        contacts = self.initial_data.pop('contacts', None)
        units = self.initial_data.pop('units', None)
        services = self.initial_data.pop('services', None)
        officer_in_charge = self.initial_data.pop('officer_in_charge', None)

        facility = super(FacilityDetailSerializer, self).update(
            instance, validated_data)

        if officer_in_charge:
            self.user = self.context['request'].user
            officer_in_charge['facility_id'] = facility.id
            created_officer = self.create_officer(officer_in_charge)
            self.inlining_errors = created_officer.get("detail") if not \
                created_officer.get("created") else None

        def create_facility_child_entity(entity_creator_callable, entity_data):
            actual_function = getattr(self, entity_creator_callable)
            actual_function(facility, entity_data, validated_data)
        if contacts:
            [create_facility_child_entity(
                "create_facility_contacts", contact) for contact in contacts]

        if units:
            [create_facility_child_entity(
                "create_facility_units", unit) for unit in units]
        if services:
            [create_facility_child_entity(
                "create_facility_services", service) for service in services]
        if self.inlining_errors:
            raise ValidationError(self.inlining_errors)
        return instance


class FacilityListSerializer(FacilitySerializer):

    class Meta(object):
        model = Facility
        fields = [
            'code', 'name', 'id', 'county', 'constituency',
            'facility_type_name', 'owner_name', 'owner_type_name',
            'regulatory_status_name', 'ward', 'operation_status_name',
            'ward_name', 'is_published', "is_approved", "has_edits",
            "rejected"
        ]


class FacilityServiceRatingSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    facility_name = serializers.ReadOnlyField(
        source='facility_service.facility.name'
    )
    service_name = serializers.ReadOnlyField(source='facility_service.name')

    class Meta(object):
        model = FacilityServiceRating


class FacilityUnitRegulationSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = FacilityUnitRegulation


class FacilityUpdatesSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    facility_updates = serializers.ReadOnlyField()
    facility_updated_json = serializers.ReadOnlyField()
    created_by_name = serializers.ReadOnlyField(
        source='created_by.get_full_name')

    class Meta:
        model = FacilityUpdates
        exclude = ('facility_updates', )


class OptionGroupSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    options = OptionSerializer(required=False, many=True)

    class Meta:
        model = OptionGroup
