from rest_framework import generics

from ..models import (
    Contact, PhysicalAddress, County, Ward, Constituency, ContactType,
    UserCounty, UserResidence, UserContact, Town)

from ..serializers import (
    ContactSerializer, CountySerializer, WardSerializer,
    PhysicalAddressSerializer, ConstituencySerializer,
    ContactTypeSerializer, InchargeCountiesSerializer,
    UserResidenceSerializer, UserContactSerializer, TownSerializer)

from ..filters import (
    ContactTypeFilter, ContactFilter, PhysicalAddressFilter,
    CountyFilter, ConstituencyFilter, WardFilter, UserCountyFilter,
    UserResidenceFilter, UserContactFilter, TownFilter)


class ContactView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    ordering_fields = ('contact_type', 'contact',)
    filter_class = ContactFilter


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class PhysicalAddressView(generics.ListCreateAPIView):
    queryset = PhysicalAddress.objects.all()
    serializer_class = PhysicalAddressSerializer
    ordering_fields = ('town', )
    filter_class = PhysicalAddressFilter


class PhysicalAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PhysicalAddress.objects.all()
    serializer_class = PhysicalAddressSerializer


class CountyView(generics.ListCreateAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    ordering_fields = ('name', 'code',)
    filter_class = CountyFilter


class CountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer


class WardView(generics.ListCreateAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    filter_class = WardFilter
    ordering_fields = ('name', 'code', 'constituency',)


class WardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer


class ConstituencyView(generics.ListCreateAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    filter_class = ConstituencyFilter
    ordering_fields = ('name', 'code', 'county',)


class ConstituencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class ContactTypeListView(generics.ListCreateAPIView):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    ordering_fields = ('name', )
    filter_class = ContactTypeFilter


class ContactTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer


class UserCountyView(generics.ListCreateAPIView):
    queryset = UserCounty.objects.all()
    serializer_class = InchargeCountiesSerializer
    filter_class = UserCountyFilter
    ordering_fields = ('user', 'county',)


class UserCountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserCounty.objects.all()
    serializer_class = InchargeCountiesSerializer


class UserResidenceListView(generics.ListCreateAPIView):
    queryset = UserResidence.objects.all()
    serializer_class = UserResidenceSerializer
    filter_class = UserResidenceFilter
    ordering_fields = ('user', 'ward',)


class UserResidenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserResidence.objects.all()
    serializer_class = UserResidenceSerializer


class UserContactListView(generics.ListCreateAPIView):
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer
    filter_class = UserContactFilter
    ordering_fields = ('user', 'contact',)


class UserContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer


class TownListView(generics.ListCreateAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    filter_class = TownFilter
    ordering_fields = ('name', )


class TownDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
