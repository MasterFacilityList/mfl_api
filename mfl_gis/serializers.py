from rest_framework import serializers
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
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = FacilityCoordinates


class WorldBorderSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = WorldBorder


class CountyBoundarySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = CountyBoundary


class ConstituencyBoundarySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = ConstituencyBoundary


class WardBoundarySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = WardBoundary
