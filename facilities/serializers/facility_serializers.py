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
    GeoCodeSource,
    GeoCodeMethod,
    FacilityCoordinates,
    FacilityContact,
    FacilityUnit,
    ServiceCategory,
    Option,
    Service,
    FacilityService,
    ServiceOption
)


class ServiceCategorySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory


class OptionSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Option


class ServiceOptionSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = ServiceOption


class ServiceSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Service


class FacilityServiceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = FacilityService


class FacilityStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = FacilityStatus


class RegulatingBodySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = RegulatingBody


class GeoCodeSourceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = GeoCodeSource


class GeoCodeMethodSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = GeoCodeMethod


class OwnerTypeSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = OwnerType


class FacilityRegulationStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = FacilityRegulationStatus


class FacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityType


class OfficerContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = OfficerContact


class JobTitleSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = JobTitle


class RegulationStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = RegulationStatus


class OfficerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Officer


class OwnerSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Owner


class FacilitySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Facility


class FacilityContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = FacilityContact


class FacilityCoordinatesSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = FacilityCoordinates


class FacilityUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = FacilityUnit
