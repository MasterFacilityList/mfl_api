from rest_framework import serializers

from common.serializers import AbstractFieldsMixin

from ..models import (
    OwnerType, Owner, JobTitle, OfficerIncharge,
    OfficerInchargeContact, ServiceCategory,
    Service, FacilityStatus, FacilityType,
    RegulatingBody, RegulationStatus, Facility,
    FacilityRegulationStatus, GeoCodeSource,
    GeoCodeMethod, FacilityGPS,
    FacilityService, FacilityContact, FacilityUnit
)


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


class ServiceCategorySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory


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


class OfficerInchargeContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = OfficerInchargeContact


class JobTitleSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = JobTitle


class RegulationStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = RegulationStatus


class OfficerInchargeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = OfficerIncharge


class OwnerSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Owner


class ServiceSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Service


class FacilitySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    services = ServiceSerializer(many=True, required=False)

    class Meta:
        model = Facility


class FacilityServiceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = FacilityService


class FacilityContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = FacilityContact


class FacilityGPSSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = FacilityGPS


class FacilityUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = FacilityUnit
