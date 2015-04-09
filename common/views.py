from rest_framework import generics

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
    queryset = Constituency.objects.all()
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
