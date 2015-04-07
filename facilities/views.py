from rest_framework import generics
from .models import Owner, Facility, Service


from .serializers import (
    OwnerSerializer, ServiceSerializer, FacilitySerializer
)


class OwnerListView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    lookup_field = 'id'


class ServiceListView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'


class FacilityListView(generics.ListCreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_fields = ('owner',)
    ordering_fields = ('name', )


class FaciltyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    lookup_field = 'id'
