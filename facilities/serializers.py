from rest_framework import serializers
from .models import (Owner, Facility, Service, FacilityService,
    FacilityContact, FacilityGIS)

from common.serializers import AbstractFieldsMixin


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


class FacilityGISService(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = FacilityGIS
