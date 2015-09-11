import json

from django.db import transaction
from django.contrib.gis.geos.point import Point
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DrfValidationError
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from common.serializers import AbstractFieldsMixin
from facilities.models import Facility
from .models import (
    GeoCodeSource,
    GeoCodeMethod,
    FacilityCoordinates,
    WorldBorder,
    CountyBoundary,
    ConstituencyBoundary,
    WardBoundary
)

from facilities.models import FacilityUpdates


class BufferCooridinatesMixin(object):
    def buffer_coordinates(self, facility, validated_data):
        try:

            facility = Facility.objects.get(id=facility.id) if hasattr(facility, 'id') else facility
            updated_data = validated_data
            updated_data['facility'] = facility
            try:
                updated_data['coordinates'] = tuple(validated_data.get('coordinates').get('coordinates'))
                coordinates = validated_data.get('coordinates')
            except AttributeError:
                updated_data['coordinates'] = tuple(json.loads(validated_data.get('coordinates')).get('coordinates'))
                coordinates = json.loads(validated_data.get('coordinates'))

        except DrfValidationError:
            raise DrfValidationError(
                {"coordinates": [
                    "The coordinates are not valid. Please Ensure they are in"
                    " {}".format(facility.ward.name)]})
        facility_update = {}
        try:
            facility_update = FacilityUpdates.objects.filter(
                facility=facility,
                cancelled=False, approved=False)[0]
        except IndexError:
            facility_update = FacilityUpdates.objects.create(
                facility=facility)
        method = validated_data.get('')
        serialized_data = {}
        method = validated_data.get('method', None)
        source = validated_data.get('source', None)
        coordinates = validated_data.get('coordinates', None)

        humanized_data = {}
        machine_data = {}

        if method:
            humanized_data['method_human'] = method.name
            machine_data['method_id'] = str(validated_data.get('method').id)
        if source:
            humanized_data['source_human'] = source.name
            machine_data['source_id'] = str(validated_data.get('source').id),
        if coordinates:
            humanized_data["longitude"] = coordinates.get('coordinates')[0]
            humanized_data["latitude"] = coordinates.get('coordinates')[1]
            machine_data["coordinates"] = coordinates

        serialized_data.update(humanized_data)
        serialized_data.update(machine_data)
        facility_update.geo_codes = json.dumps(serialized_data)
        facility_update.save()


class GeoCodeSourceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = GeoCodeSource


class GeoCodeMethodSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = GeoCodeMethod


class FacilityCoordinatesListSerializer(
        AbstractFieldsMixin, GeoFeatureModelSerializer):
    # DO NOT make this any fatter than it must be
    # The facility list JSON payload is already > 1MB!
    # That is why there is a detail serializer
    ward = serializers.ReadOnlyField(source="facility.ward.id")
    constituency = serializers.ReadOnlyField(
        source="facility.ward.constituency.id"
    )
    county = serializers.ReadOnlyField(
        source="facility.ward.constituency.county.id"
    )
    geometry = serializers.ReadOnlyField(source='simplify_coordinates')

    class Meta(object):
        model = FacilityCoordinates
        geo_field = "geometry"
        exclude = (
            'created', 'created_by', 'updated', 'updated_by', 'deleted',
            'search', 'collection_date', 'source', 'method', 'active',
            'facility', 'coordinates', 'id'
        )


class FacilityCoordinatesDetailSerializer(
        AbstractFieldsMixin, GeoFeatureModelSerializer):
    facility_name = serializers.ReadOnlyField(source="facility.name")
    facility_id = serializers.ReadOnlyField(source="facility.id")
    ward = serializers.ReadOnlyField(source="facility.ward.id")
    constituency = serializers.ReadOnlyField(
        source="facility.ward.constituency.id"
    )
    county = serializers.ReadOnlyField(
        source="facility.ward.constituency.county.id"
    )

    class Meta(object):
        model = FacilityCoordinates
        geo_field = "geometry"


class FacilityCoordinateSimpleSerializer(
        AbstractFieldsMixin, BufferCooridinatesMixin,
        serializers.ModelSerializer):
    source_name = serializers.ReadOnlyField(source="source.name")
    method_name = serializers.ReadOnlyField(source="method.name")

    class Meta(object):
        model = FacilityCoordinates

    @transaction.atomic
    def update(self, instance, validated_data):
        facility = instance.facility
        if facility.approved:
            self.buffer_coordinates(facility, validated_data)
            return instance
        else:
            return super(FacilityCoordinateSimpleSerializer, self).update(
                instance, validated_data)


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
    geometry = serializers.ReadOnlyField()

    class Meta(object):
        model = WorldBorder
        geo_field = 'geometry'
        exclude = (
            'mpoly', 'active', 'deleted', 'search', 'created', 'updated',
            'created_by', 'updated_by', 'longitude', 'latitude',
        )


class WorldBorderDetailSerializer(AbstractBoundarySerializer):
    facility_coordinates = serializers.ReadOnlyField()
    center = serializers.ReadOnlyField()

    class Meta(AbstractBoundarySerializer.Meta):
        model = WorldBorder


class CountyBoundarySerializer(AbstractBoundarySerializer):
    constituency_boundary_ids = serializers.ReadOnlyField()
    county_id = serializers.ReadOnlyField(source='area.id')
    geometry = serializers.ReadOnlyField()

    class Meta(object):
        model = CountyBoundary
        geo_field = 'geometry'
        exclude = (
            'active', 'deleted', 'search', 'created', 'updated', 'created_by',
            'updated_by', 'area', 'mpoly',
        )


class CountyBoundaryDetailSerializer(AbstractBoundarySerializer):
    constituency_ids = serializers.ReadOnlyField()
    constituency_boundary_ids = serializers.ReadOnlyField()
    facility_coordinates = serializers.ReadOnlyField()
    county_id = serializers.ReadOnlyField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = CountyBoundary


class CountyBoundSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    bound = serializers.ReadOnlyField()

    class Meta(AbstractBoundarySerializer.Meta):
        model = CountyBoundary
        fields = ("bound", )


class ConstituencyBoundarySerializer(AbstractBoundarySerializer):
    ward_ids = serializers.ReadOnlyField()
    ward_boundary_ids = serializers.ReadOnlyField()
    constituency_id = serializers.CharField(source='area.id')
    geometry = serializers.ReadOnlyField()

    class Meta(object):
        model = ConstituencyBoundary
        geo_field = 'geometry'
        exclude = (
            'active', 'deleted', 'search', 'created', 'updated', 'created_by',
            'updated_by', 'area', 'mpoly',
        )


class ConstituencyBoundaryDetailSerializer(AbstractBoundarySerializer):
    ward_ids = serializers.ReadOnlyField()
    ward_boundary_ids = serializers.ReadOnlyField()
    facility_coordinates = serializers.ReadOnlyField()
    constituency_id = serializers.ReadOnlyField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = ConstituencyBoundary


class ConstituencyBoundSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    bound = serializers.ReadOnlyField()

    class Meta(AbstractBoundarySerializer.Meta):
        model = ConstituencyBoundary
        fields = ("bound", )


class WardBoundarySerializer(AbstractBoundarySerializer):
    ward_id = serializers.CharField(source='area.id')
    geometry = serializers.ReadOnlyField()

    class Meta(object):
        model = WardBoundary
        geo_field = 'geometry'
        exclude = (
            'active', 'deleted', 'search', 'created', 'updated', 'created_by',
            'updated_by', 'area', 'mpoly',
        )


class WardBoundaryDetailSerializer(AbstractBoundarySerializer):
    facility_coordinates = serializers.ReadOnlyField()
    facility_ids = serializers.ReadOnlyField()
    ward_id = serializers.ReadOnlyField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = WardBoundary
