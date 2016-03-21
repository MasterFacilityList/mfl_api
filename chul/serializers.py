import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.serializers import AbstractFieldsMixin, ContactSerializer
from common.models import Contact, ContactType

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact,
    CHUService,
    CHURating,
    ChuUpdateBuffer
)


class ChuUpdateBufferSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = ChuUpdateBuffer


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
    health_unit_workers = serializers.ReadOnlyField(source='workers')
    facility_name = serializers.ReadOnlyField(source='facility.name')
    facility_ward = serializers.ReadOnlyField(source='facility.ward.name')
    facility_constituency = serializers.ReadOnlyField(
        source='facility.ward.constituency.name')
    facility_subcounty = serializers.ReadOnlyField(
        source='facility.ward.sub_county.name')
    facility_county = serializers.ReadOnlyField(
        source='facility.ward.constituency.county.name')
    ward_code = serializers.ReadOnlyField(source='facility.ward.code')
    lat_long = serializers.ReadOnlyField(source='facility.lat_long')
    contacts = serializers.ReadOnlyField()
    geo_features = serializers.ReadOnlyField(source='json_features')
    boundaries = serializers.ReadOnlyField(source='facility.boundaries')
    pending_updates = serializers.ReadOnlyField()
    latest_update = serializers.ReadOnlyField(source='latest_update.id')
    avg_rating = serializers.ReadOnlyField(source='average_rating')
    number_of_ratings = serializers.ReadOnlyField(source='rating_count')
    inlined_errors = {}

    class Meta(object):
        model = CommunityHealthUnit
        read_only_fields = ('code', )

    def get_basic_updates(self, chu_instance, validated_data):
        updates = self.initial_data
        if ('facility' in self.initial_data and
                validated_data['facility'] != chu_instance):
            updates['facility'] = {
                "facility_id": str(validated_data['facility'].id),
                "facility_name": validated_data['facility'].name,
            }
        if ('status' in self.initial_data and
                validated_data['status'] != chu_instance.status):
            updates['status'] = {
                'status_id': str(validated_data['status'].id),
                'status_name': validated_data['status'].name
            }
        updates.pop('health_unit_workers', None)
        updates.pop('contacts', None)
        return json.dumps(updates)

    def buffer_updates(
            self, validated_data, chu_instance, chews=None, contacts=None, ):

        try:
            update = ChuUpdateBuffer.objects.get(
                health_unit=chu_instance,
                is_approved=False, is_rejected=False)
        except ChuUpdateBuffer.DoesNotExist:
            update = ChuUpdateBuffer.objects.create(
                health_unit=chu_instance,
                created_by_id=self.context['request'].user.id,
                updated_by_id=self.context['request'].user.id,
                is_new=True)
        basic_updates = self.get_basic_updates(chu_instance, validated_data)

        update.basic = basic_updates if basic_updates \
            and not update.basic else update.basic

        if chews:
            for chew in chews:
                chew.pop('created', None)
                chew.pop('updated', None)
                chew.pop('updated_by', None)
                chew.pop('created_by', None)

            chews = json.dumps(chews)
            update.workers = chews
        if contacts:
            for contact in contacts:
                contact_type = ContactType.objects.get(
                    id=contact['contact_type'])
                contact['contact_type_name'] = contact_type.name

            contacts = json.dumps(contacts)

            update.contacts = contacts
        update.save()

    def _ensure_all_chew_required_provided(self, chew):
        if 'first_name' and 'last_name' not in chew:
            self.inlined_errors.update({
                "Community Health Worker": [
                    "Ensure the CHEW first name and last name are provided"
                ]
            })

    def _validate_chew(self, chews):
        for chew in chews:
            self._ensure_all_chew_required_provided(chew)

    def save_chew(self, instance, chews, context):
        for chew in chews:

            chew_id = chew.pop('id', None)
            if chew_id:
                chew_obj = CommunityHealthWorker.objects.get(id=chew_id)
                chew_obj.first_name = chew['first_name']
                chew_obj.last_name = chew['last_name']
                chew_obj.is_incharge = chew['is_incharge']
                chew_obj.save()
            else:
                chew['health_unit'] = instance.id
                chew_data = CommunityHealthWorkerSerializer(
                    data=chew, context=context)
                chew_data.save() if chew_data.is_valid() else None

    def _validate_contacts(self, contacts):
        for contact in contacts:
            if 'contact' not in contact or 'contact_type' not in contact:
                self.inlined_errors.update(
                    {
                        "contact": [
                            "Contact type of contact field is missing from"
                            " the payload"]
                    }
                )
                continue
            try:
                ContactType.objects.get(id=contact['contact_type'])
            except (ContactType.DoesNotExist, ValueError):
                self.inlined_errors.update(
                    {
                        "contact": ["The provided contact_type does not exist"]
                    }
                )

    def create_contact(self, contact_data):
        try:
            if 'id' in contact_data:
                contact = Contact.objects.get(
                    id=contact_data['id']
                )
                contact.contact = contact_data['contact']
                contact.contact_type_id = contact_data['contact_type']
                contact.save()
                return contact
            else:
                contact = Contact.objects.get(
                    contact=contact_data['contact']
                )
                return contact
        except Contact.DoesNotExist:
            contact = ContactSerializer(
                data=contact_data, context=self.context)
            return contact.save() if contact.is_valid() else \
                self.inlined_errors.update(contact.errors)

    def create_chu_contacts(self, instance, contacts, validated_data):

        for contact_data in contacts:
            contact = self.create_contact(contact_data)
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
        self.inlined_errors = {}
        chews = self.initial_data.pop('health_unit_workers', [])
        contacts = self.initial_data.pop('contacts', [])

        self._validate_contacts(contacts)
        self._validate_chew(chews)

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
        self.inlined_errors = {}
        chews = self.initial_data.pop('health_unit_workers', [])
        contacts = self.initial_data.pop('contacts', [])
        chu = CommunityHealthUnit.objects.get(id=instance.id)
        self._validate_contacts(contacts)
        self._validate_chew(chews)

        if not self.inlined_errors:
            if chu.is_approved and not instance.is_rejected:
                self.buffer_updates(validated_data, instance, chews, contacts)
                return instance

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


class CHURatingSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    facility_name = serializers.ReadOnlyField(source='chu.facility.name')
    facility_id = serializers.ReadOnlyField(source='chu.facility.id')
    chu_name = serializers.ReadOnlyField(source='chu.name')

    class Meta(object):
        model = CHURating
