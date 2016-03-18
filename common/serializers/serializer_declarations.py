from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from ..models import (
    Contact,
    PhysicalAddress,
    County,
    Ward,
    Constituency,
    ContactType,
    UserCounty,
    UserContact,
    Town,
    UserConstituency,
    SubCounty,
    DocumentUpload,
    ErrorQueue,
    UserSubCounty
)
from .serializer_base import AbstractFieldsMixin


class UserSubCountySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    county_id = serializers.ReadOnlyField(source='sub_county.county.id')

    county_name = serializers.ReadOnlyField(source='sub_county.county.name')
    user = serializers.PrimaryKeyRelatedField(
        validators=[], required=False, queryset=get_user_model().objects.all())
    sub_county = serializers.PrimaryKeyRelatedField(
        validators=[], required=False, queryset=SubCounty.objects.all())
    sub_county_name = serializers.ReadOnlyField(source="sub_county.name")

    class Meta(object):
        model = UserSubCounty


class SubCountySerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    county_name = serializers.ReadOnlyField(source="county.name")

    class Meta(object):
        model = SubCounty


class UserContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        validators=[], required=False)
    user = serializers.PrimaryKeyRelatedField(
        validators=[],
        queryset=get_user_model().objects.all(),
        required=False)
    contact_text = serializers.CharField(
        source='contact.contact', required=False)
    contact_type_text = serializers.ReadOnlyField(
        source='contact.contact_type.name'
    )
    contact_type = serializers.CharField(source='contact.contact_type.id')

    class Meta(object):
        model = UserContact


class ContactTypeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = ContactType


class ContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    contact_type_name = serializers.ReadOnlyField(source='contact_type.name')

    class Meta(object):
        model = Contact


class PhysicalAddressSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    town_name = serializers.ReadOnlyField(source='town.name')

    class Meta(object):
        model = PhysicalAddress


class CountySerializer(AbstractFieldsMixin, GeoModelSerializer):

    class Meta(object):
        model = County
        read_only_fields = ('code',)


class CountyDetailSerializer(AbstractFieldsMixin, GeoModelSerializer):
    bound = serializers.ReadOnlyField(source="county_bound")

    class Meta(object):
        model = County
        read_only_fields = ('code',)


class CountySlimDetailSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = County
        read_only_fields = ('code',)


class TownSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Town


class WardSerializer(AbstractFieldsMixin, GeoModelSerializer):
    county_name = serializers.ReadOnlyField(source="constituency.county.name")
    constituency_name = serializers.ReadOnlyField(source="constituency.name")
    sub_county_name = serializers.ReadOnlyField(source="sub_county.name")
    sub_county = serializers.CharField(source='sub_county.id')

    class Meta(object):
        model = Ward
        read_only_fields = ('code',)


class WardDetailSerializer(AbstractFieldsMixin, GeoModelSerializer):
    from mfl_gis.serializers import WardBoundarySerializer

    ward_boundary = WardBoundarySerializer(
        source='wardboundary', read_only=True)
    facility_coordinates = serializers.ReadOnlyField()
    county = CountySerializer(read_only=True)
    county_name = serializers.ReadOnlyField(source="constituency.county.name")
    constituency_name = serializers.ReadOnlyField(source="constituency.name")
    sub_county_name = serializers.ReadOnlyField(source="sub_county.name")

    class Meta(object):
        model = Ward
        read_only_fields = ('code',)


class WardSlimDetailSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    county_name = serializers.ReadOnlyField(source="constituency.county.name")
    constituency_name = serializers.ReadOnlyField(source="constituency.name")
    sub_county_name = serializers.ReadOnlyField(source="sub_county.name")

    class Meta(object):
        model = Ward


class ConstituencySerializer(AbstractFieldsMixin, GeoModelSerializer):
    county_name = serializers.ReadOnlyField(source="county.name")

    class Meta(object):
        model = Constituency
        read_only_fields = ('code',)


class ConstituencyDetailSerializer(AbstractFieldsMixin, GeoModelSerializer):
    bound = serializers.ReadOnlyField(source="constituency_bound")
    county_name = serializers.ReadOnlyField(source="county.name")

    class Meta(object):
        model = Constituency
        read_only_fields = ('code',)


class ConstituencySlimDetailSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Constituency


class UserCountySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    user_full_name = serializers.ReadOnlyField(
        source='user.get_full_name')
    county_name = serializers.ReadOnlyField(
        source='county.name')
    county_code = serializers.ReadOnlyField(
        source='county.code')
    user_email = serializers.ReadOnlyField(
        source='user.email')
    user = serializers.PrimaryKeyRelatedField(
        validators=[], required=False,
        queryset=get_user_model().objects.all())
    county = serializers.PrimaryKeyRelatedField(
        validators=[], required=False,
        queryset=County.objects.all())

    class Meta(object):
        model = UserCounty


class FilteringOptionsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    id = serializers.CharField(max_length=200)


class FilteringSummariesSerializer(serializers.Serializer):
    county = FilteringOptionsSerializer(many=True)
    constituenncy = FilteringOptionsSerializer(many=True)
    ward = FilteringOptionsSerializer(many=True)
    facility_type = FilteringOptionsSerializer(many=True)
    service_category = FilteringOptionsSerializer(many=True)
    operation_status = FilteringOptionsSerializer(many=True)


class UserConstituencySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')
    constituency_name = serializers.ReadOnlyField(source='constituency.name')
    county_name = serializers.ReadOnlyField(source='constituency.county.name')
    county_id = serializers.ReadOnlyField(source='constituency.county.id')
    user = serializers.PrimaryKeyRelatedField(
        validators=[], required=False, queryset=get_user_model().objects.all())
    constituency = serializers.PrimaryKeyRelatedField(
        validators=[], required=False, queryset=Constituency.objects.all())

    class Meta(object):
        model = UserConstituency


class DocumentUploadSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = DocumentUpload
        read_only_fields = (
            'created', 'created_by', 'updated', 'updated_by', 'deleted',
        )


class ErrorQueueSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = ErrorQueue
