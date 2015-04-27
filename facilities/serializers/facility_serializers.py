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
    ServiceOption,
    ServiceRating,
    FacilityApproval,
    FacilityOperationState,
    FacilityUpgrade,
    InspectionReport,
    CoverReportTemplate
)


class CoverReportTemplateSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = CoverReportTemplate


class InspectionReportSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = InspectionReport


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
    class Meta(object):
        model = Service


class FacilityServiceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
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
    class Meta(object):
        model = RegulationStatus


class OfficerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Officer


class OwnerSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Owner


class FacilitySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Facility


class FacilityContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityContact


class FacilityUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = FacilityUnit
