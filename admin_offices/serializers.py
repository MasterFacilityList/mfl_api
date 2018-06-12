from rest_framework import serializers
from common.serializers import AbstractFieldsMixin
from common.models import ContactType
from .models import AdminOffice, AdminOfficeContact


class AdminOfficeContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    contact_type_name = serializers.ReadOnlyField(
        source='contact_type.name')

    class Meta:
        model = AdminOfficeContact


class AdminOfficeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    county_name = serializers.ReadOnlyField(source='county.name')
    sub_county_name = serializers.ReadOnlyField(source='sub_county.name')
    contacts = AdminOfficeContactSerializer(many=True, required=False)

    def update_or_create_contacts(self, instance, contacts):
        for contact in contacts:
            if 'id' not in contact:
                contact['admin_office'] = instance
                contact_type_id = contact.get('contact_type')
                contact['contact'] = contact.get('contact')
                contact['updated_by'] = instance.updated_by
                contact['created_by'] = instance.created_by
                try:
                    contact_type_obj = ContactType.objects.get(
                        id=contact_type_id)
                    contact['contact_type'] = contact_type_obj
                except:
                    continue
                AdminOfficeContact.objects.create(**contact)
            else:
                pass

    def create(self, validated_data):
        contacts = self.initial_data.pop('contacts', [])
        instance = super(AdminOfficeSerializer, self).create(validated_data)
        self.update_or_create_contacts(instance, contacts)
        return instance

    def update(self, instance, validated_data):
        contacts = self.initial_data.pop('contacts', [])
        self.update_or_create_contacts(instance, contacts)
        return super(AdminOfficeSerializer, self).update(
            instance, validated_data)

    class Meta:
        model = AdminOffice
        fields = [
            "id", "name", "county_name", "county", "sub_county",
            "sub_county_name", "sub_county_name", "sub_county",
            "phone_number", "email", "is_national", "contacts"
        ]
