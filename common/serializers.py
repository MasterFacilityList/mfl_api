from django.utils import timezone

from rest_framework import serializers

from .models import (
    Contact, Province, County, District,
    Division, Location, SubLocation, Constituency)


class AbstractFieldsMixin(object):
    """
    Injects the fields in the abstract base model as a model
    instance is being saved.

    """
    def __init__(self, *args, **kwargs):
        super(AbstractFieldsMixin, self).__init__(*args, **kwargs)
        exclude_fields = ['created', 'created_by', 'updated', 'updated_by']
        for i in exclude_fields:
            if i in self.fields:
                self.fields.pop(i)

    def create(self, validated_data):
        validated_data['created'] = timezone.now()
        validated_data['updated'] = timezone.now()
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user

        return self.Meta.model.objects.create(**validated_data)


class ContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Contact


class ProvinceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Province


class CountySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = County


class DistrictSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = District


class DivisionSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Division


class LocationSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Location


class SubLocationSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    division = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    county = serializers.CharField(required=False)
    province = serializers.CharField(required=False)
    constituency = serializers.CharField(required=False)

    class Meta:
        model = SubLocation


class ConstituencySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Constituency
