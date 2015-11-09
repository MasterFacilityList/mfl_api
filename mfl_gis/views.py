import six

from django.contrib.gis.geos import Point
from rest_framework import generics, views, status
from rest_framework import settings as rest_settings
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.compat import OrderedDict

from facilities.models import Facility
from common.views import AuditableDetailViewMixin
from common.utilities import CustomRetrieveUpdateDestroyView

from .models import (
    GeoCodeSource,
    GeoCodeMethod,
    FacilityCoordinates,
    WorldBorder,
    CountyBoundary,
    ConstituencyBoundary,
    WardBoundary
)
from .filters import (
    GeoCodeSourceFilter,
    GeoCodeMethodFilter,
    FacilityCoordinatesFilter,
    WorldBorderFilter,
    CountyBoundaryFilter,
    ConstituencyBoundaryFilter,
    WardBoundaryFilter
)
from .serializers import (
    GeoCodeSourceSerializer,
    GeoCodeMethodSerializer,
    FacilityCoordinatesListSerializer,
    FacilityCoordinatesDetailSerializer,
    WorldBorderSerializer,
    WorldBorderDetailSerializer,
    CountyBoundarySerializer,
    ConstituencyBoundarySerializer,
    WardBoundarySerializer,
    CountyBoundaryDetailSerializer,
    ConstituencyBoundaryDetailSerializer,
    WardBoundaryDetailSerializer,
    FacilityCoordinateSimpleSerializer,
    CountyBoundSerializer,
    ConstituencyBoundSerializer,
    BufferCooridinatesMixin
)
from .pagination import GISPageNumberPagination
from .generics import GISListCreateAPIView


class GeoCodeSourceListView(generics.ListCreateAPIView):

    """
    List and creates Geo-Code sources

    name -- Name of the Geo Code Source
    description -- The description of the Geo Code Source
    abbreviation -- The abbreviation of the Geo-Code source
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = GeoCodeSource.objects.all()
    serializer_class = GeoCodeSourceSerializer
    ordering_fields = ('name', 'abbreviation',)
    filter_class = GeoCodeSourceFilter


class GeoCodeSourceDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular Geo Code Source
    """
    queryset = GeoCodeSource.objects.all()
    serializer_class = GeoCodeSourceSerializer
    pagination_class = GISPageNumberPagination


class GeoCodeMethodListView(GISListCreateAPIView):

    """
    Lists and creates Geo-Code collection methods

    name -- Name of the Geo-Code Collectiom method
    description -- Description of the Geo-Code collection method
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = GeoCodeMethod.objects.all()
    serializer_class = GeoCodeMethodSerializer
    filter_class = GeoCodeMethodFilter
    ordering_fields = ('name', )


class GeoCodeMethodDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular Geo-Code Collectiom method
    """
    queryset = GeoCodeMethod.objects.all()
    serializer_class = GeoCodeMethodSerializer
    pagination_class = GISPageNumberPagination


class FacilityCoordinatesListView(GISListCreateAPIView):

    """
    Lists and creates facility coordinates

    ward -- A list of comma separated ward pks
    constituency -- A list of comma separated constituency pks
    county -- A list of comma separated county pks
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    # The list serializer omits many fields for size reasons
    # This data is controlled access
    # Do not change the permission_classes without good reason
    permission_classes = (DjangoModelPermissions,)
    queryset = FacilityCoordinates.objects.all()
    serializer_class = FacilityCoordinatesListSerializer
    filter_class = FacilityCoordinatesFilter
    ordering_fields = (
        'facility', 'latitude', 'longitude', 'source', 'method',)
    pagination_class = GISPageNumberPagination

    def get(self, *args, **kwargs):
        queryset = self.queryset
        ward = self.request.query_params.get('ward', None)
        county = self.request.query_params.get('county', None)
        constituency = self.request.query_params.get('constituency', None)
        if ward:
            queryset = queryset.filter(facility__ward=ward)
        if county:
            queryset = queryset.filter(
                facility__ward__constituency__county=county)
        if constituency:
            queryset = queryset.filter(
                facility__ward__constituency=constituency)

        result = [fc.json_features for fc in queryset]
        return views.Response(data=result)


class FacilityCoordinatesDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular facility coordinates details
    """
    # The detail serializer has all fields
    # This data is controlled access
    # Do not change the permission classes without good reason
    permission_classes = (DjangoModelPermissions,)
    queryset = FacilityCoordinates.objects.all()
    serializer_class = FacilityCoordinatesDetailSerializer


class FacilityCoordinatesCreationAndListing(
        BufferCooridinatesMixin, GISListCreateAPIView):

    """
    Lists and creates facility coordinates

    ward -- A list of comma separated ward pks
    constituency -- A list of comma separated constituency pks
    county -- A list of comma separated county pks
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    # The list serializer omits many fields for size reasons
    # This data is controlled access
    # Do not change the permission_classes without good reason
    permission_classes = (DjangoModelPermissions,)
    queryset = FacilityCoordinates.objects.all()
    serializer_class = FacilityCoordinateSimpleSerializer
    filter_class = FacilityCoordinatesFilter
    ordering_fields = (
        'facility', 'latitude', 'longitude', 'source', 'method',)
    pagination_class = GISPageNumberPagination

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        request.data['updated_by'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        facility_id = request.data.get('facility')
        facility = Facility.objects.get(id=facility_id)
        if facility.approved:
            self.buffer_coordinates(facility, request.data)
        else:
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return views.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FacilityCoordinatesCreationAndDetail(
        BufferCooridinatesMixin, CustomRetrieveUpdateDestroyView):

    """
    Lists and creates facility coordinates

    ward -- A list of comma separated ward pks
    constituency -- A list of comma separated constituency pks
    county -- A list of comma separated county pks
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    # The list serializer omits many fields for size reasons
    # This data is controlled access
    # Do not change the permission_classes without good reason
    permission_classes = (DjangoModelPermissions,)
    queryset = FacilityCoordinates.objects.all()
    serializer_class = FacilityCoordinateSimpleSerializer


class WorldBorderListView(GISListCreateAPIView):

    """
    Lists and creates ward borders

    name -- A list of comma separated ward names
    code -- A  list of comma separated ward codes
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = WorldBorder.objects.all()
    serializer_class = WorldBorderSerializer
    filter_class = WorldBorderFilter
    ordering_fields = ('name', 'code',)
    pagination_class = GISPageNumberPagination


class WorldBorderDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular ward border details
    """
    queryset = WorldBorder.objects.all()
    serializer_class = WorldBorderDetailSerializer


class CountyBoundaryListView(GISListCreateAPIView):

    """
    Lists and creates county boundaries

    name --  A list of comma separated county names
    code  -- A list of comma separated county codes
    area -- A list of comma separated area pks
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = CountyBoundary.objects.all()
    serializer_class = CountyBoundarySerializer
    filter_class = CountyBoundaryFilter
    ordering_fields = ('name', 'code',)
    pagination_class = GISPageNumberPagination


class CountyBoundaryDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular county boundary detail
    """
    queryset = CountyBoundary.objects.all()
    serializer_class = CountyBoundaryDetailSerializer


class CountyBoundView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular county boundary detail
    """
    queryset = CountyBoundary.objects.all()
    serializer_class = CountyBoundSerializer


class ConstituencyBoundaryListView(GISListCreateAPIView):

    """
    Lists and creates constituency boundaries

    name --  A list of comma separated constituency names
    code  -- A list of comma separated constituency codes
    area -- A list of comma separated area pks
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = ConstituencyBoundary.objects.all()
    serializer_class = ConstituencyBoundarySerializer
    filter_class = ConstituencyBoundaryFilter
    ordering_fields = ('name', 'code',)
    pagination_class = GISPageNumberPagination


class ConstituencyBoundaryDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular constituency boundary detail
    """
    queryset = ConstituencyBoundary.objects.all()
    serializer_class = ConstituencyBoundaryDetailSerializer


class ConstituencyBoundView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular constituency boundary detail
    """
    queryset = ConstituencyBoundary.objects.all()
    serializer_class = ConstituencyBoundSerializer


class WardBoundaryListView(GISListCreateAPIView):

    """
    Lists and creates ward boundaries

    name --  A list of comma separated ward names
    code  -- A list of comma separated ward codes
    area -- A list of comma separated area pks
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = WardBoundary.objects.all()
    serializer_class = WardBoundarySerializer
    filter_class = WardBoundaryFilter
    ordering_fields = ('name', 'code',)
    pagination_class = GISPageNumberPagination


class WardBoundaryDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular ward boundary detail
    """
    queryset = WardBoundary.objects.all()
    serializer_class = WardBoundaryDetailSerializer


class IkoWapi(views.APIView):

    """
    A utility service to determine adminitrative unit based on geocoordinates.
    """

    def _validate_lat_long(self, lat, lng):
        err_dict = {}

        if not isinstance(lng, six.integer_types + (float, )):
            err_dict["longitude"] = ["Invalid longitude provided"]

        if not isinstance(lat, six.integer_types + (float, )):
            err_dict["latitude"] = ["Invalid latitude provided"]

        return err_dict

    def post(self, request, *args, **kwargs):
        lng, lat = request.data.get('longitude'), request.data.get('latitude')

        err = self._validate_lat_long(lat, lng)
        if err:
            return views.Response(err, status=400)

        try:
            point = Point(x=lng, y=lat)
        except TypeError:
            return views.Response({
                rest_settings.api_settings.NON_FIELD_ERRORS_KEY: [
                    "Invalid value given for longitude or latitude",
                ],
            }, status=400)

        try:
            data = WardBoundary.objects.values(
                'area', 'area__name',
                'area__constituency', 'area__constituency__name',
                'area__constituency__county',
                'area__constituency__county__name',
            ).get(mpoly__contains=point)

            return views.Response(OrderedDict([
                ('ward', data['area']),
                ('ward_name', data['area__name']),
                ('constituency', data['area__constituency']),
                ('constituency_name', data['area__constituency__name']),
                ('county', data['area__constituency__county']),
                ('county_name', data['area__constituency__county__name'])
            ]))
        except WardBoundary.DoesNotExist:
            return views.Response({
                rest_settings.api_settings.NON_FIELD_ERRORS_KEY: [
                    "No ward contains the coordinates ({}, {})".format(
                        lng, lat
                    )
                ]
            }, status=400)
