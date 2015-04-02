from django.utils import timezone

from rest_framework import serializers

from .models import (
    Contact, Province, County, District,
    Division, Location, SubLocation, Constituency)


class AbastractFieldsMixin(object):
    """
    Injects the fields in the abstract base model as a model
    instance is being saved.
    """
    def create(self, validated_data):
        validated_data['created'] = timezone.now
        validated_data['updated'] = timezone.now
        validated_data['created_by'] = self.request.context['user']
        validated_data['updated_by'] = self.request.context['user']
        return self.Meta.model.objects.create(**validated_data)


class ContactSerializer(
        AbastractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Contact


class ProvinceSerializer(
        AbastractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Province


class CountySerializer(
        AbastractFieldsMixin, serializers.ModelSerializer):
            "constituency": "Limuru",

            "constituency": "Limuru",
            "constituency": "Limuru",
    class Meta:
        model = County


class DistrictSerializer(
        AbastractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = District


class DivisionSerializer(
        AbastractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Division


class LocationSerializer(
        AbastractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Location


class SubLocationSerializer(
        AbastractFieldsMixin, serializers.ModelSerializer):
    location = serializers.CharField()
    division = serializers.CharField()
    district = serializers.CharField()
    county = serializers.CharField()
    province = serializers.CharField()
    constituency = serializers.CharField()

    class Meta:
        model = SubLocation


class ConstituencySerializer(
        AbastractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Constituency
