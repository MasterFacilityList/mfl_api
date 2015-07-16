from rest_framework import serializers

from common.serializers import AbstractFieldsMixin

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
    ServiceOption,
    FacilityApproval,
    FacilityOperationState,
    FacilityUpgrade,
    RegulatingBodyContact,
    FacilityOfficer,
    RegulatoryBodyUser,
    FacilityUnitRegulation,
    FacilityUpdates
)


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


class ServiceOptionSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    display_text = serializers.ReadOnlyField(source="option.display_text")
    value = serializers.ReadOnlyField(source="option.value")
    is_exclusive_option = serializers.ReadOnlyField(
        source="option.is_exclusive_option"
    )
    option_type = serializers.ReadOnlyField(source="option.option_type")
    service_name = serializers.ReadOnlyField(source="service.name")

    class Meta(object):
        model = ServiceOption


class ServiceSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True)
    service_options = ServiceOptionSerializer(many=True, required=False)

    class Meta(object):
        model = Service
        read_only_fields = ('code',)


class FacilityServiceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    service_name = serializers.CharField(read_only=True)
    option_display_value = serializers.CharField(read_only=True)
    average_rating = serializers.ReadOnlyField()
    number_of_ratings = serializers.ReadOnlyField()

    class Meta(object):
        model = FacilityService


class FacilityStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityStatus


class RegulatingBodySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

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

    class Meta(object):
        model = Owner
        read_only_fields = ('code',)


class FacilitySerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    regulatory_status_name = serializers.CharField(read_only=True)
    facility_type_name = serializers.CharField(read_only=True)
    owner_name = serializers.CharField(read_only=True)
    owner_type_name = serializers.CharField(read_only=True)
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

    class Meta(object):
        model = Facility
        fields = [
            "name", "owner_name", "operation_status", "code", "id",
            "county", "constituency", "ward", "facility_type_name",
            "operation_status_name", "regulatory_status_name",
            "facility_type_name", "number_of_beds",
            "number_of_cots", "is_classified", "is_published",
            "open_weekends", "open_whole_day",
            "open_public_holidays", "owner_type_name",
            "ward_name", "average_rating", "facility_services",
            "created", "updated", "deleted", "active",
            "abbreviation", "description",
            "created_by", "updated_by", "facility_type",
            "owner", "physical_address",
            "parent", "contacts", "is_approved",
            "has_edits", "latest_update", "regulatory_body_name"]


class FacilityDetailSerializer(FacilitySerializer):
    facility_services = serializers.ReadOnlyField(
        source="get_facility_services")
    facility_contacts = serializers.ReadOnlyField(
        read_only=True, source="get_facility_contacts")
    facility_physical_address = serializers.DictField(
        read_only=True, required=False)
    coordinates = serializers.ReadOnlyField()
    latest_approval = serializers.ReadOnlyField()
    boundaries = serializers.ReadOnlyField()

    class Meta(object):
        model = Facility
        exclude = ('attributes', )


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


class FacilityServiceRatingSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

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
    facility = FacilityDetailSerializer(required=False)
    created_by_name = serializers.ReadOnlyField(
        source='created_by.get_full_name')

    class Meta:
        model = FacilityUpdates
        exclude = ('facility_updates', )
