from django.utils import timezone

from rest_framework import serializers


from .models import Contact, County, SubCounty, Constituency, ContactType


class AbstractFieldsMixin(object):
    """
    Injects the fields in the abstract base model as a model
    instance is being saved.

    """
    def __init__(self, *args, **kwargs):
        super(AbstractFieldsMixin, self).__init__(*args, **kwargs)
        exclude_fields = ['created', 'created_by', 'updated', 'updated_by']
        for i in exclude_fields:
            self.fields.pop(i) if i in self.fields else None

    def create(self, validated_data):
        validated_data['created'] = timezone.now()
        validated_data['updated'] = timezone.now()
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user

        return self.Meta.model.objects.create(**validated_data)


class ContactTypeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = ContactType


class ContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Contact


class CountySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = County


class SubCountySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = SubCounty


class ConstituencySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Constituency
