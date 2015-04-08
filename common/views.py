from django.contrib.auth.models import AnonymousUser

from rest_framework import generics

from .models import (
    Contact, County, SubCounty, Constituency, ContactType)

from .serializers import (
    ContactSerializer, CountySerializer, SubCountySerializer,
    ConstituencySerializer, ContactTypeSerializer)


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
    ordering_fields = ('contact_type', )
    filter_fields = ('contact_type', )


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
    filter_fields = ('county', )
    ordering_fields = ('name', )


class SubCountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()
    serializer_class = SubCountySerializer


class ConstituencyView(generics.ListCreateAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    filter_fields = ('county', )
    ordering_fields = ('name', )


class ConstituencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class ContactTypeListView(generics.ListCreateAPIView):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    ordering_fields = ('name', )
