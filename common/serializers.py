from django.utils import timezone

from rest_framework import serializers


from .models import (
    Contact, PhysicalAddress, County, Ward, Constituency,
    ContactType, UserCounties)


class AbstractFieldsMixin(object):
    """
    Injects the fields in the abstract base model as a model
    instance is being saved.
    """
    def __init__(self, *args, **kwargs):
        super(AbstractFieldsMixin, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        """`created` and `created_by` are only mutated if they are null"""
        if not validated_data.get('created', None):
            validated_data['created'] = timezone.now()

        validated_data['updated'] = timezone.now()

        if not validated_data.get('created_by', None):
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


class PhysicalAddressSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = PhysicalAddress


class CountySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = County


class WardSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Ward


class ConstituencySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Constituency


class InchargeCountiesSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserCounties
