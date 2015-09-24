from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.serializers import AbstractFieldsMixin, ContactSerializer
from common.models import Contact

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact,
    CHUService
)


class CHUServiceSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = CHUService


class CommunityHealthWorkerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta(object):
        model = CommunityHealthWorker
        read_only_fields = ('health_unit_approvals',)


class CommunityHealthWorkerPostSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta(object):
        model = CommunityHealthWorker
        exclude = ('health_unit',)


class CommunityHealthUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    status_name = serializers.ReadOnlyField(source="status.name")
    health_unit_workers = CommunityHealthWorkerPostSerializer(
        many=True, required=False)
    facility_name = serializers.ReadOnlyField(source='facility.name')
    facility_ward = serializers.ReadOnlyField(source='facility.ward.name')
    facility_subcounty = serializers.ReadOnlyField(
        source='facility.ward.constituency.name')
    facility_county = serializers.ReadOnlyField(
        source='facility.ward.constituency.county.name')
    inlined_errors = {}

    class Meta(object):
        model = CommunityHealthUnit
        read_only_fields = ('code',)

    def _validate_chew(self, chews, context):
        for chew in chews:
            chew_data = CommunityHealthWorkerPostSerializer(
                data=chew, context=context)
            if chew_data.is_valid():
                pass
            else:
                self.inlined_errors.update(chew_data.errors)

    def save_chew(self, instance, chews, context):
        for chew in chews:
            chew['health_unit'] = instance.id
            chew_data = CommunityHealthWorkerSerializer(
                data=chew, context=context)
            chew_data.save() if chew_data.is_valid() else None

    def _validate_contacts(self, contacts):
        for contact in contacts:
            contact = ContactSerializer(
                data=contact, context=self.context)
            if contact.is_valid():
                return contact.save()
            else:
                self.inlined_errors.update(contact.errors)

    def create_contact(self, contact_data):

        try:
            return Contact.objects.get(contact=contact_data["contact"])
        except Contact.DoesNotExist:
            contact = ContactSerializer(
                data=contact_data, context=self.context)
            if contact.is_valid():
                return contact.save()
            else:
                self.inlined_errors.update(contact.errors)

    def create_chu_contacts(self, instance, contacts, validated_data):
        for contact_data in contacts:
            contact = self.create_contact(contact_data)
            if contact:
                health_unit_contact_data_unadit = {
                    "contact": contact.id,
                    "health_unit": instance.id
                }

                try:
                    CommunityHealthUnitContact.objects.get(
                        contact_id=contact.id, health_unit_id=instance.id)
                except CommunityHealthUnitContact.DoesNotExist:
                    chu_contact = CommunityHealthUnitContactSerializer(
                        data=health_unit_contact_data_unadit,
                        context=self.context)
                    chu_contact.save() if chu_contact.is_valid() else None

    def create(self, validated_data):
        chews = self.initial_data.pop('health_unit_workers', [])
        contacts = self.initial_data.pop('contacts', [])

        self._validate_chew(chews, self.context)
        self._validate_contacts(contacts)

        if not self.inlined_errors:
            validated_data.pop('health_unit_workers', None)

            chu = super(CommunityHealthUnitSerializer, self).create(
                validated_data)
            self.save_chew(chu, chews, self.context)
            self.create_chu_contacts(chu, contacts, validated_data)
            return chu
        else:
            raise ValidationError(self.inlined_errors)

    def update(self, instance, validated_data):
        chews = self.initial_data.pop('health_unit_workers', [])
        contacts = self.initial_data.pop('contacts', [])

        validated_data.pop('health_unit_workers', None)
        self._validate_chew(chews, self.context)
        self._validate_contacts(contacts)
        if not self.inlined_errors:
            super(CommunityHealthUnitSerializer, self).update(
                instance, validated_data)
            self.save_chew(instance, chews, self.context)
            self.create_chu_contacts(instance, contacts, validated_data)
            return instance
        else:
            raise ValidationError(self.inlined_errors)


class CommunityHealthWorkerContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = CommunityHealthWorkerContact


class StatusSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Status


class CommunityHealthUnitContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = CommunityHealthUnitContact
