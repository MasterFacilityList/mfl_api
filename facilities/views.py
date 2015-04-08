import django_filters

from rest_framework import generics
from .models import (
    Owner, Facility, Service, FacilityService, FacilityContact, FacilityGIS)


from .serializers import (
    OwnerSerializer, ServiceSerializer, FacilitySerializer,
    FacilityGISSerializer, FacilityContactSerializer, FacilityServiceSerializer
)


class FacilityFilter(django_filters.FilterSet):
    beds = django_filters.NumberFilter(name='number_of_beds')
    cots = django_filters.NumberFilter(name='number_of_cots')
    open_whole_day = django_filters.BooleanFilter(name='open_whole_day')
    open_whole_week = django_filters.BooleanFilter(name='open_whole_week')
    county = django_filters.CharFilter(name='sub_county__county')

    class Meta:
        model = Facility
        fields = [
            'beds', 'cots', 'open_whole_week', 'open_whole_day', 'sub_county',
            'county', 'facility_type', 'owner', 'status', 'name', 'services'
        ]


class OwnerListView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class ServiceListView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


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


class FacilityGISListView(generics.ListCreateAPIView):
    queryset = FacilityGIS.objects.all()
    serializer_class = FacilityGISSerializer
    filter_fields = ('facility', )


class FacilityGISDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityGIS.objects.all()
    serializer_class = FacilityGISSerializer
