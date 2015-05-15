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


class AbstractBoundarySerializer(
        AbstractFieldsMixin, GeoFeatureModelSerializer):
    center = serializers.ReadOnlyField()
    facility_count = serializers.ReadOnlyField()
    density = serializers.ReadOnlyField()
    bound = serializers.ReadOnlyField()

    class Meta(object):
        geo_field = 'mpoly'


class WorldBorderSerializer(AbstractBoundarySerializer):
    center = serializers.ReadOnlyField()

    class Meta(AbstractBoundarySerializer.Meta):
        model = WorldBorder


class WorldBorderDetailSerializer(AbstractBoundarySerializer):
    facility_coordinates = serializers.ReadOnlyField()
    center = serializers.ReadOnlyField()

    class Meta(AbstractBoundarySerializer.Meta):
        model = WorldBorder


class CountyBoundarySerializer(AbstractBoundarySerializer):
    constituency_ids = serializers.ReadOnlyField()
    constituency_boundary_ids = serializers.ReadOnlyField()
    county_id = serializers.ReadOnlyField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = CountyBoundary


class CountyBoundaryDetailSerializer(AbstractBoundarySerializer):
    constituency_ids = serializers.ReadOnlyField()
    constituency_boundary_ids = serializers.ReadOnlyField()
    facility_coordinates = serializers.ReadOnlyField()
    county_id = serializers.ReadOnlyField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = CountyBoundary


class ConstituencyBoundarySerializer(AbstractBoundarySerializer):
    ward_ids = serializers.ReadOnlyField()
    ward_boundary_ids = serializers.ReadOnlyField()
    constituency_id = serializers.CharField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = ConstituencyBoundary


class ConstituencyBoundaryDetailSerializer(AbstractBoundarySerializer):
    ward_ids = serializers.ReadOnlyField()
    ward_boundary_ids = serializers.ReadOnlyField()
    facility_coordinates = serializers.ReadOnlyField()
    constituency_id = serializers.ReadOnlyField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = ConstituencyBoundary


class WardBoundarySerializer(AbstractBoundarySerializer):
    ward_id = serializers.CharField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = WardBoundary


class WardBoundaryDetailSerializer(AbstractBoundarySerializer):
    facility_coordinates = serializers.ReadOnlyField()
    facility_ids = serializers.ReadOnlyField()
    ward_id = serializers.ReadOnlyField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = WardBoundary
