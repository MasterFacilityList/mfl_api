from django.contrib.auth.models import AnonymousUser

from rest_framework import generics

from .models import (
    Contact, Province, County, District,
    Division, Location, SubLocation, Constituency)

from .serializers import (
    ContactSerializer, ProvinceSerializer,
    CountySerializer, DistrictSerializer,
    DivisionSerializer, LocationSerializer,
    SubLocationSerializer, ConstituencySerializer)


class FilterViewMixin(object):
    def get_queryset(self):
        user = self.request.user
        if not isinstance(user, AnonymousUser):
            if user.is_national:
                return self.queryset
            else:
                if user.is_incharge:
                    return self.queryset.filter(county=user.county)
                else:
                    return []
        else:
            return self.queryset


class ContactView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'id'


class ProvinceView(generics.ListCreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class ProvinceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    lookup_field = 'id'


class DisctrictView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = DistrictSerializer
    filter_fields = ('county', 'province')


class DistrictDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    lookup_field = 'id'


class DivisionView(generics.ListCreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    filter_fields = ('district', )


class DivisionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    lookup_field = 'id'


class LocationView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_fields = ('division', )


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'id'


class SubLocationView(generics.ListCreateAPIView):
    queryset = SubLocation.objects.all()
    serializer_class = SubLocationSerializer
    filter_fields = ('location', )


class SubLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubLocation.objects.all()
    serializer_class = SubLocationSerializer
    lookup_field = 'id'


class CountyView(generics.ListCreateAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer


class CountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    lookup_field = 'id'


class ConstituencyView(generics.ListCreateAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    filter_fields = ('county', )


class ConstituentcyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    lookup_field = 'id'
