from rest_framework import generics

from .models import (
    Contact, Province, County, District,
    Division, Location, SubLocation, Constituency)

from .serializers import (
    ContactSerializer, ProvinceSerializer,
    CountySerializer, DistrictSerializer,
    DivisionSerializer, LocationSerializer,
    SubLocationSerializer, ConstituencySerializer)


class ContactView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_id = 'pk'


class ProvinceView(generics.ListCreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class ProvinceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    lookup_id = 'pk'


class DisctrictView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = DistrictSerializer
    filter_fields = ('county', 'province')


class DistrictDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    lookup_id = 'pk'


class DivisionView(generics.ListCreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    filter_fields = ('district', )


class DivisionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    lookup_id = 'pk'


class LocationView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_fields = ('division', )


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_id = 'pk'


class SubLocationView(generics.ListCreateAPIView):
    queryset = SubLocation.objects.all()
    serializer_class = SubLocationSerializer
    filter_fields = ('location', )


class SubLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubLocation.objects.all()
    serializer_class = SubLocationSerializer
    lookup_id = 'pk'


class CountyView(generics.ListCreateAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer


class CountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    lookup_id = 'pk'


class ConstituencyView(generics.ListCreateAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    filter_fields = ('county', )


class ConstituentcyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    lookup_id = 'pk'
