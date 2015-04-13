from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import (
    Contact, County, SubCounty, Constituency, ContactType)

from .serializers import (
    ContactSerializer, CountySerializer, SubCountySerializer,
    ConstituencySerializer, ContactTypeSerializer)

from .filters import ContactFilter, ConstituencyFilter, SubCountyFilter


class ContactView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    ordering_fields = ('contact_type', )
    filter_class = ContactFilter


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class CountyView(generics.ListCreateAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    ordering_fields = ('name', )


class CountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer


class SubCountyView(generics.ListCreateAPIView):
    queryset = SubCounty.objects.all()
    serializer_class = SubCountySerializer
    filter_class = SubCountyFilter
    ordering_fields = ('name', )


class SubCountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCounty.objects.all()
    serializer_class = SubCountySerializer


class ConstituencyView(generics.ListCreateAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    filter_class = ConstituencyFilter
    ordering_fields = ('name', )


class ConstituencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class ContactTypeListView(generics.ListCreateAPIView):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    ordering_fields = ('name', )


class ContactTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'counties': reverse(
            'api:common:counties_list', request=request, format=format),
        'users': reverse(
            'api:users:users_list', request=request, format=format),
        'facilities': reverse(
            'api:facilities:facility_list', request=request, format=format),
        'contacts': reverse(
            'api:common:contacts_list', request=request, format=format),
        'contact_types': reverse(
            'api:common:contact_types_list', request=request, format=format),
        'sub_counties': reverse(
            'api:common:sub_counties_list', request=request, format=format),
        'constituencies': reverse(
            'api:common:constituencies_list', request=request, format=format),
        'owners': reverse(
            'api:facilities:owners_list', request=request, format=format),
        'owner_types': reverse(
            'api:facilities:facility_list', request=request, format=format),
        'services': reverse(
            'api:facilities:services_list', request=request, format=format)
    })
