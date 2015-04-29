from rest_framework import generics
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
    CountyBoundarySerializer,
    ConstituencyBoundarySerializer,
    WardBoundarySerializer
)


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
    queryset = FacilityCoordinates.objects.all()
    serializer_class = FacilityCoordinatesSerializer
    filter_class = FacilityCoordinatesFilter
    ordering_fields = (
        'facility', 'latitude', 'longitude', 'source', 'method',)


class FacilityCoordinatesDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityCoordinates.objects.all()
    serializer_class = FacilityCoordinatesSerializer


class WorldBorderListView(generics.ListCreateAPIView):
    queryset = WorldBorder.objects.all()
    serializer_class = WorldBorderSerializer
    filter_class = WorldBorderFilter
    ordering_fields = ('name', 'code',)


class WorldBorderDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = WorldBorder.objects.all()
    serializer_class = WorldBorderSerializer


class CountyBoundaryListView(generics.ListCreateAPIView):
    queryset = CountyBoundary.objects.all()
    serializer_class = CountyBoundarySerializer
    filter_class = CountyBoundaryFilter
    ordering_fields = ('name', 'code',)


class CountyBoundaryDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CountyBoundary.objects.all()
    serializer_class = CountyBoundarySerializer


class ConstituencyBoundaryListView(generics.ListCreateAPIView):
    queryset = ConstituencyBoundary.objects.all()
    serializer_class = ConstituencyBoundarySerializer
    filter_class = ConstituencyBoundaryFilter
    ordering_fields = ('name', 'code',)


class ConstituencyBoundaryDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ConstituencyBoundary.objects.all()
    serializer_class = ConstituencyBoundarySerializer


class WardBoundaryListView(generics.ListCreateAPIView):
    queryset = WardBoundary.objects.all()
    serializer_class = WardBoundarySerializer
    filter_class = WardBoundaryFilter
    ordering_fields = ('name', 'code',)


class WardBoundaryDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = WardBoundary.objects.all()
    serializer_class = WardBoundarySerializer
