from django.utils import timezone

from rest_framework import serializers


from .models import Contact, County, Ward, Constituency, ContactType


class AbstractFieldsMixin(object):
    """
    Injects the fields in the abstract base model as a model
    instance is being saved.
    """
    def __init__(self, *args, **kwargs):
        super(AbstractFieldsMixin, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        if not validated_data['created']:
            validated_data['created'] = timezone.now()
        validated_data['updated'] = timezone.now()

        if not validated_data['updated_by']:
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


class WardSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Ward


class ConstituencySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Constituency
