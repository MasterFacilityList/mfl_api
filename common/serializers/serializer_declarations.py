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
    UserConstituency
)
from .serializer_base import AbstractFieldsMixin


class UserContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    contact_text = serializers.ReadOnlyField(source='contact.contact')
    contact_type_text = serializers.ReadOnlyField(
        source='contact.contact_type.name'
    )

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

    ward_name = serializers.ReadOnlyField(source='ward.name')
    class Meta(object):
        model = Town


class WardSerializer(AbstractFieldsMixin, GeoModelSerializer):

    class Meta(object):
        model = Ward
        read_only_fields = ('code',)


class WardDetailSerializer(AbstractFieldsMixin, GeoModelSerializer):
    from mfl_gis.serializers import WardBoundarySerializer

    ward_boundary = WardBoundarySerializer(
        source='wardboundary', read_only=True)
    facility_coordinates = serializers.ReadOnlyField()
    county = CountySerializer(read_only=True)

    class Meta(object):
        model = Ward
        read_only_fields = ('code',)


class WardSlimDetailSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Ward


class ConstituencySerializer(AbstractFieldsMixin, GeoModelSerializer):

    class Meta(object):
        model = Constituency
        read_only_fields = ('code',)


class ConstituencyDetailSerializer(AbstractFieldsMixin, GeoModelSerializer):
    bound = serializers.ReadOnlyField(source="constituency_bound")

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
    user_email = serializers.ReadOnlyField(
        source='user.email')

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

    class Meta:
        model = UserConstituency
