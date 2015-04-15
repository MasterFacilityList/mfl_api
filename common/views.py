from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import (
    Contact, PhysicalAddress, County, Ward, Constituency, ContactType,
    UserCounties, UserResidence, UserContact, Town)

from .serializers import (
    ContactSerializer, CountySerializer, WardSerializer,
    PhysicalAddressSerializer, ConstituencySerializer,
    ContactTypeSerializer, InchargeCountiesSerializer,
    UserResidenceSerializer, UserContactSerializer, TownSerializer)

from .filters import (
    ContactTypeFilter, ContactFilter, PhysicalAddressFilter,
    CountyFilter, ConstituencyFilter, WardFilter, UserCountiesFilter,
    UserResidenceFilter, UserContactFilter, TownFilter)


class ContactView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    ordering_fields = ('contact_type', )
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
    ordering_fields = ('name', )
    filter_class = CountyFilter


class CountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer


class WardView(generics.ListCreateAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    filter_class = WardFilter
    ordering_fields = ('name', )


class WardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer


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
    filter_class = ContactTypeFilter


class ContactTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer


class UserCountiesView(generics.ListCreateAPIView):
    queryset = UserCounties.objects.all()
    serializer_class = InchargeCountiesSerializer
    filter_class = UserCountiesFilter
    ordering_fields = ('user', )


class UserCountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserCounties.objects.all()
    serializer_class = InchargeCountiesSerializer


class UserResidenceListView(generics.ListCreateAPIView):
    queryset = UserResidence.objects.all()
    serializer_class = UserResidenceSerializer
    filter_class = UserResidenceFilter
    ordering_fields = ('user',)


class UserResidenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserResidence.objects.all()
    serializer_class = UserResidenceSerializer


class UserContactListView(generics.ListCreateAPIView):
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer
    filter_class = UserContactFilter
    ordering_fields = ('user', )


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
        'wards': reverse(
            'api:common:wards_list', request=request, format=format),
        'constituencies': reverse(
            'api:common:constituencies_list', request=request, format=format),
        'owners': reverse(
            'api:facilities:owners_list', request=request, format=format),
        'owner_types': reverse(
            'api:facilities:facility_list', request=request, format=format),
        'services': reverse(
            'api:facilities:services_list', request=request, format=format)
    })
