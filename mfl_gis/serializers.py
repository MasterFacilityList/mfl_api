from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
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


class FacilityCoordinatesSerializer(
        AbstractFieldsMixin, GeoFeatureModelSerializer):
    class Meta(object):
        model = FacilityCoordinates
        geo_field = "coordinates"


class WorldBorderSerializer(
        AbstractFieldsMixin, GeoFeatureModelSerializer):
    class Meta(object):
        model = WorldBorder
        geo_field = "mpoly"


class WorldBorderDetailSerializer(
        AbstractFieldsMixin, GeoFeatureModelSerializer):
    facility_coordinates = serializers.ReadOnlyField()
    center = serializers.ReadOnlyField()

    class Meta(object):
        model = WorldBorder
        geo_field = "mpoly"


class CountyBoundarySerializer(
        AbstractFieldsMixin, GeoFeatureModelSerializer):
    center = serializers.ReadOnlyField()

    class Meta(object):
        model = CountyBoundary
        geo_field = "mpoly"


class ConstituencyBoundarySerializer(
        AbstractFieldsMixin, GeoFeatureModelSerializer):
    center = serializers.ReadOnlyField()

    class Meta(object):
        model = ConstituencyBoundary
        geo_field = "mpoly"


class WardBoundarySerializer(
        AbstractFieldsMixin, GeoFeatureModelSerializer):
    center = serializers.ReadOnlyField()

    class Meta(object):
        model = WardBoundary
        geo_field = "mpoly"
