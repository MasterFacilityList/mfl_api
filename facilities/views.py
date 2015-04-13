from rest_framework import generics
from .models import (
    Owner, Facility, Service, FacilityService, FacilityContact, FacilityGPS)


from .serializers import (
    OwnerSerializer, ServiceSerializer, FacilitySerializer,
    FacilityGPSSerializer, FacilityContactSerializer, FacilityServiceSerializer
)

from .filters import (
    FacilityFilter, ServiceFilter, FacilityGPSFilter, OwnerFilter)


class OwnerListView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_class = OwnerFilter


class OwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class ServiceListView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_class = ServiceFilter


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class FacilityListView(generics.ListCreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    ordering_fields = ('name', )
    filter_class = FacilityFilter


class FaciltyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class FacilityServiceListView(generics.ListCreateAPIView):
    queryset = FacilityService.objects.all()
    serializer_class = FacilityServiceSerializer
    filter_fields = ('facility', 'service', )


class FacilityServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityService.objects.all()
    serializer_class = FacilityServiceSerializer


class FacilityContactListView(generics.ListCreateAPIView):
    queryset = FacilityContact.objects.all()
    serializer_class = FacilityContactSerializer
    filter_fields = ('facility', 'contact', )


class FacilityContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityContact.objects.all()
    serializer_class = FacilityContactSerializer


class FacilityGPSListView(generics.ListCreateAPIView):
    queryset = FacilityGPS.objects.all()
    serializer_class = FacilityGPSSerializer
    filter_fields = ('facility', )
    filter_class = FacilityGPSFilter


class FacilityGPSDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityGPS.objects.all()
    serializer_class = FacilityGPSSerializer
