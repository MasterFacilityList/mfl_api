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
    Town
)
from .serializer_base import AbstractFieldsMixin


class UserContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = UserContact


class ContactTypeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = ContactType


class ContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Contact


class PhysicalAddressSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = PhysicalAddress


class CountySerializer(AbstractFieldsMixin, GeoModelSerializer):

    class Meta(object):
        model = County
        read_only_fields = ('code',)


class CountyDetailSerializer(AbstractFieldsMixin, GeoModelSerializer):
    from mfl_gis.serializers import CountyBoundarySerializer

    county_boundary = CountyBoundarySerializer(
        source='countyboundary', read_only=True)
    facility_coordinates = serializers.ReadOnlyField()

    class Meta(object):
        model = County
        read_only_fields = ('code',)


class TownSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

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


class ConstituencySerializer(AbstractFieldsMixin, GeoModelSerializer):

    class Meta(object):
        model = Constituency
        read_only_fields = ('code',)


class ConstituencyDetailSerializer(AbstractFieldsMixin, GeoModelSerializer):
    from mfl_gis.serializers import ConstituencyBoundarySerializer

    constituency_boundary = ConstituencyBoundarySerializer(
        source='constituencyboundary', read_only=True)
    facility_coordinates = serializers.ReadOnlyField()

    class Meta(object):
        model = Constituency
        read_only_fields = ('code',)


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
