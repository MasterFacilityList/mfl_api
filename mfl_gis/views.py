from rest_framework import generics
from common.views import AuditableDetailViewMixin

from .models import (
    GeoCodeSource,
    GeoCodeMethod,
    FacilityCoordinates
)
from .filters import (
    GeoCodeSourceFilter,
    GeoCodeMethodFilter,
    FacilityCoordinatesFilter
)
from .serializers import (
    GeoCodeSourceSerializer,
    GeoCodeMethodSerializer,
    FacilityCoordinatesSerializer
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
