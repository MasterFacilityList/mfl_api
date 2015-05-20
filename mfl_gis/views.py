from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions
from common.views import AuditableDetailViewMixin

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
    FacilityCoordinatesSerializer,
    WorldBorderSerializer,
    WorldBorderDetailSerializer,
    CountyBoundarySerializer,
    ConstituencyBoundarySerializer,
    WardBoundarySerializer,
    CountyBoundaryDetailSerializer,
    ConstituencyBoundaryDetailSerializer,
    WardBoundaryDetailSerializer
)
from .pagination import GISPageNumberPagination


class GeoCodeSourceListView(generics.ListCreateAPIView):
    queryset = GeoCodeSource.objects.all()
    serializer_class = GeoCodeSourceSerializer
    ordering_fields = ('name', 'abbreviation',)
    filter_class = GeoCodeSourceFilter


class GeoCodeSourceDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = GeoCodeSource.objects.all()
    serializer_class = GeoCodeSourceSerializer


class GeoCodeMethodListView(generics.ListCreateAPIView):
    queryset = GeoCodeMethod.objects.all()
    serializer_class = GeoCodeMethodSerializer
    filter_class = GeoCodeMethodFilter
    ordering_fields = ('name', )


class GeoCodeMethodDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = GeoCodeMethod.objects.all()
    serializer_class = GeoCodeMethodSerializer


class FacilityCoordinatesListView(generics.ListCreateAPIView):

    # This data is controlled access
    # Do not change the permission_classes without good reason
    permission_classes = (DjangoModelPermissions,)
    queryset = FacilityCoordinates.objects.all()
    serializer_class = FacilityCoordinatesSerializer
    filter_class = FacilityCoordinatesFilter
    ordering_fields = (
        'facility', 'latitude', 'longitude', 'source', 'method',)
    pagination_class = GISPageNumberPagination


class FacilityCoordinatesDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):

    # This data is controlled access
    # Do not change the permission classes without good reason
    permission_classes = (DjangoModelPermissions,)
    queryset = FacilityCoordinates.objects.all()
    serializer_class = FacilityCoordinatesSerializer


class WorldBorderListView(generics.ListCreateAPIView):
    queryset = WorldBorder.objects.all()
    serializer_class = WorldBorderSerializer
    filter_class = WorldBorderFilter
    ordering_fields = ('name', 'code',)
    pagination_class = GISPageNumberPagination


class WorldBorderDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = WorldBorder.objects.all()
    serializer_class = WorldBorderDetailSerializer


class CountyBoundaryListView(generics.ListCreateAPIView):
    queryset = CountyBoundary.objects.all()
    serializer_class = CountyBoundarySerializer
    filter_class = CountyBoundaryFilter
    ordering_fields = ('name', 'code',)
    pagination_class = GISPageNumberPagination


class CountyBoundaryDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CountyBoundary.objects.all()
    serializer_class = CountyBoundaryDetailSerializer


class ConstituencyBoundaryListView(generics.ListCreateAPIView):
    queryset = ConstituencyBoundary.objects.all()
    serializer_class = ConstituencyBoundarySerializer
    filter_class = ConstituencyBoundaryFilter
    ordering_fields = ('name', 'code',)
    pagination_class = GISPageNumberPagination


class ConstituencyBoundaryDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ConstituencyBoundary.objects.all()
    serializer_class = ConstituencyBoundaryDetailSerializer


class WardBoundaryListView(generics.ListCreateAPIView):
    queryset = WardBoundary.objects.all()
    serializer_class = WardBoundarySerializer
    filter_class = WardBoundaryFilter
    ordering_fields = ('name', 'code',)
    pagination_class = GISPageNumberPagination


class WardBoundaryDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = WardBoundary.objects.all()
    serializer_class = WardBoundaryDetailSerializer
