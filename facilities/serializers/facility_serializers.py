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
    ServiceRating,
    FacilityApproval,
    FacilityOperationState,
    FacilityUpgrade,
    RegulatingBodyContact,
    RatingScale
)


class RatingScaleSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = RatingScale


class RegulatingBodyContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

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

    class Meta(object):
        model = FacilityApproval


class ServiceCategorySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = ServiceCategory


class ServiceRatingSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = ServiceRating


class OptionSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Option


class ServiceOptionSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = ServiceOption


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
    operations_status_name = serializers.CharField(read_only=True)
    county = serializers.CharField(read_only=True)
    constituency = serializers.CharField(read_only=True)
    ward_name = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()

    class Meta(object):
        model = Facility
        exclude = ('attributes',)


class FacilityDetailSerializer(FacilitySerializer):
    facility_services = serializers.ReadOnlyField(
        source="get_facility_services")
    facility_contacts = serializers.ReadOnlyField(
        read_only=True, source="get_facility_contacts")
    facility_physical_address = serializers.DictField(
        read_only=True, required=False)


class FacilityContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityContact


class FacilityUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityUnit


class FacilityServiceRatingSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityServiceRating
