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
    from mfl_gis.serializers import CountyBoundarySerializer

    county_boundary = CountyBoundarySerializer(
        source='countyboundary', read_only=True)
    facility_coordinates = serializers.ReadOnlyField()

    class Meta(object):
        model = County


class TownSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Town


class WardSerializer(AbstractFieldsMixin, GeoModelSerializer):
    from mfl_gis.serializers import WardBoundarySerializer

    ward_boundary = WardBoundarySerializer(
        source='wardboundary', read_only=True)
    facility_coordinates = serializers.ReadOnlyField()

    county = serializers.CharField(read_only=True)

    class Meta(object):
        model = Ward


class ConstituencySerializer(AbstractFieldsMixin, GeoModelSerializer):
    from mfl_gis.serializers import ConstituencyBoundarySerializer

    constituency_boundary = ConstituencyBoundarySerializer(
        source='constituencyboundary', read_only=True)
    facility_coordinates = serializers.ReadOnlyField()

    class Meta(object):
        model = Constituency


class UserCountySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = UserCounty
