from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from common.serializers import AbstractFieldsMixin
from .models import (
    GeoCodeSource,
    GeoCodeMethod,
    FacilityCoordinates,
    WorldBorder,
    CountyBoundary,
    ConstituencyBoundary,
    WardBoundary
)


class GeoCodeSourceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = GeoCodeSource


class GeoCodeMethodSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = GeoCodeMethod


class FacilityCoordinatesSerializer(AbstractFieldsMixin, GeoModelSerializer):
    class Meta(object):
        model = FacilityCoordinates


class WorldBorderSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = WorldBorder


class WorldBorderDetailSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    facility_coordinates = serializers.ReadOnlyField()

    class Meta(object):
        model = WorldBorder


class CountyBoundarySerializer(AbstractFieldsMixin, GeoModelSerializer):
    class Meta(object):
        model = CountyBoundary


class ConstituencyBoundarySerializer(AbstractFieldsMixin, GeoModelSerializer):
    class Meta(object):
        model = ConstituencyBoundary


class WardBoundarySerializer(AbstractFieldsMixin, GeoModelSerializer):
    class Meta(object):
        model = WardBoundary
