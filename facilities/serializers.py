from rest_framework import serializers
from .models import Owner, Facility, Service
from common.serializers import AbstractFieldsMixin


class OwnerSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Owner


class ServiceSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Service


class FacilityReadSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Facility


class FacilitySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    services = ServiceSerializer(many=True, required=False)

    def create(self, validated_data):
        services = validated_data.pop('services')

        facility = super(FacilitySerializer, self).create(validated_data)

        def inject_audit_fields(data, model, unique_fields_data):
            data['created'] = facility.created
            data['updated'] = facility.updated
            data['updated_by'] = facility.updated_by
            data['created_by'] = facility.created_by
            try:
                obj = model.objects.get(**unique_fields_data)
            except:
                obj = model.objects.create(**data)
            facility.services.add(obj)

        for service in services:
            unique_data = {
                "name": service.get("name")
            }
            inject_audit_fields(service, Service, unique_data)

        return facility

    class Meta:
        model = Facility
