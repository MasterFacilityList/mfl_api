from __future__ import unicode_literals
import json

from django.db import transaction
from django.utils import six
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from common.serializers import AbstractFieldsMixin, PartialResponseMixin
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

        facility = Facility.objects.get(id=facility.id) if hasattr(
            facility, 'id') else facility

        coordinates = []
        if isinstance(validated_data.get('coordinates'), six.string_types):
            coordinates = json.loads(validated_data.get('coordinates'))

        if isinstance(validated_data.get('coordinates'), dict):
            coordinates = validated_data.get('coordinates')

        facility_update = {}
        try:
            facility_update = FacilityUpdates.objects.filter(
                facility=facility,
                cancelled=False, approved=False)[0]
        except IndexError:
            facility_update = FacilityUpdates.objects.create(
                facility=facility)
        serialized_data = {}
        method = validated_data.get('method', None)
        source = validated_data.get('source', None)

        humanized_data = {}
        machine_data = {}
        if 'method' in validated_data:
            try:
                humanized_data['method_human'] = method.name
                machine_data['method_id'] = str(
                    validated_data.get('method').id)
            except AttributeError:
                method = GeoCodeMethod.objects.get(id=method)
                humanized_data['method_human'] = method.name
                machine_data['method_id'] = str(method.id)
        if 'source' in validated_data:
            try:
                humanized_data['source_human'] = source.name
                machine_data['source_id'] = str(
                    validated_data.get('source').id)
            except AttributeError:
                source = GeoCodeSource.objects.get(id=source)
                humanized_data['source_human'] = source.name
                machine_data['source_id'] = str(source.id)

        long_lat = coordinates.get('coordinates')
        humanized_data["longitude"] = long_lat[0]
        humanized_data["latitude"] = long_lat[1]
        machine_data["coordinates"] = coordinates

        serialized_data.update(humanized_data)
        serialized_data.update(machine_data)
        facility_update.geo_codes = json.dumps(serialized_data)
        facility_update.save()
        return facility_update


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
            FacilityCoordinates(**validated_data).clean()
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
    constituency_boundary_ids = serializers.ReadOnlyField()
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
    ward_boundary_ids = serializers.ReadOnlyField()
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
    ward_id = serializers.ReadOnlyField(source='area.id')

    class Meta(AbstractBoundarySerializer.Meta):
        model = WardBoundary


class DrillBoundarySerializer(GeoFeatureModelSerializer):
    id = serializers.ReadOnlyField(source='area.code')
    name = serializers.ReadOnlyField(source='area.name')
    geometry = serializers.ReadOnlyField()
    center = serializers.ReadOnlyField()
    facility_count = serializers.ReadOnlyField()
    density = serializers.ReadOnlyField()
    bound = serializers.ReadOnlyField()

    class Meta(object):
        geo_field = 'geometry'
        fields = (
            'geometry', 'center', 'bound', 'id',
            'facility_count', 'name',
        )

    def get_fields(self):
        p = PartialResponseMixin()
        origi_fields = super(DrillBoundarySerializer, self).get_fields()
        return p.strip_fields(self.context.get('request'), origi_fields)


class DrillCountyBoundarySerializer(DrillBoundarySerializer):

    class Meta(DrillBoundarySerializer.Meta):
        model = CountyBoundary


class DrillConstituencyBoundarySerializer(DrillBoundarySerializer):

    class Meta(DrillBoundarySerializer.Meta):
        model = ConstituencyBoundary


class DrillWardBoundarySerializer(DrillBoundarySerializer):

    area_id = serializers.ReadOnlyField(source='area.id')
    county_name = serializers.ReadOnlyField(
        source='area.constituency.county.name'
    )
    county_code = serializers.ReadOnlyField(
        source='area.constituency.county.code'
    )
    constituency_name = serializers.ReadOnlyField(
        source='area.constituency.name'
    )
    constituency_code = serializers.ReadOnlyField(
        source='area.constituency.code'
    )

    class Meta(object):
        geo_field = 'geometry'
        model = WardBoundary
        fields = (
            'geometry', 'center', 'bound', 'id', 'area_id',
            'facility_count', 'name',
            'county_name', 'county_code',
            'constituency_code', 'constituency_name'
        )
