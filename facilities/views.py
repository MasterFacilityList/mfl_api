from rest_framework import generics

from .models import (
    OwnerType, Owner, JobTitle, OfficerIncharge,
    OfficerInchargeContact, ServiceCategory,
    Service, FacilityStatus, FacilityType,
    RegulatingBody, RegulationStatus, Facility,
    FacilityRegulationStatus, GeoCodeSource,
    GeoCodeMethod, FacilityGPS,
    FacilityService, FacilityContact
)


from .serializers import (
    OwnerSerializer, ServiceSerializer, FacilitySerializer,
    FacilityGPSSerializer, FacilityContactSerializer,
    FacilityServiceSerializer, FacilityStatusSerializer,
    FacilityTypeSerializer, JobTitleSerializer,
    OfficerInchargeSerializer, RegulatingBodySerializer,
    GeoCodeMethodSerializer, GeoCodeSourceSerializer,
    ServiceCategorySerializer, OwnerTypeSerializer,
    OfficerInchargeContactSerializer, FacilityRegulationStatusSerializer
)

from .filters import (
    FacilityFilter, ServiceFilter, FacilityGPSFilter,
    OwnerFilter, JobTitleFilter)


class FacilityStatusListView(generics.ListCreateAPIView):
    queryset = FacilityStatus.objects.all()
    serializer_class = FacilityStatusSerializer
    ordering_fields = ('name',)


class FacilityStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityStatus.objects.all()
    serializer_class = FacilityStatusSerializer


class JobTitleListView(generics.ListCreateAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    ordering_fields = ('name',)
    filter_class = JobTitleFilter


class JobTitleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer


class OfficerInchargeListView(generics.ListCreateAPIView):
    queryset = OfficerIncharge.objects.all()
    serializer_class = OfficerInchargeSerializer
    filter_class = None
    ordering_fields = ('name',)


class OfficerInchargeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfficerIncharge.objects.all()
    serializer_class = OfficerInchargeSerializer


class RegulatingBodyListView(generics.ListCreateAPIView):
    queryset = RegulatingBody.objects.all()
    serializer_class = RegulatingBodySerializer
    filter_class = None
    ordering_fields = ('name', )


class RegulatingBodyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegulatingBody.objects.all()
    serializer_class = RegulatingBodySerializer


class GeoCodeSourceListView(generics.ListCreateAPIView):
    queryset = GeoCodeSource.objects.all()
    serializer_class = GeoCodeSourceSerializer
    filter_class = None
    ordering_fields = ('name',)


class GeoCodeSourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GeoCodeSource.objects.all()
    serializer_class = GeoCodeSourceSerializer


class ServiceCategoryListView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    filter_class = None
    ordering_fields = ('name',)


class ServiceCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class OwnerTypeListView(generics.ListCreateAPIView):
    queryset = OwnerType.objects.all()
    serializer_class = OwnerTypeSerializer
    filter_class = None
    ordering_fields = ('name', )


class OwnerTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OwnerType.objects.all()
    serializer_class = OwnerTypeSerializer


class OfficerInchargeContactListView(generics.ListCreateAPIView):
    queryset = OfficerInchargeContact.objects.all()
    serializer_class = OfficerInchargeContactSerializer
    filter_class = None
    ordering_fields = None


class OfficerInchargeContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfficerInchargeContact.objects.all()
    serializer_class = OfficerInchargeContactSerializer


class GeoCodeMethodListView(generics.ListCreateAPIView):
    queryset = GeoCodeMethod.objects.all()
    serializer_class = GeoCodeMethodSerializer
    filter_class = None
    ordering_fields = ('name', )


class GeoCodeMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GeoCodeMethod.objects.all()
    serializer_class = GeoCodeMethodSerializer


class OwnerListView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_class = OwnerFilter
    ordering_fields = ('name',)


class OwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class ServiceListView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_class = ServiceFilter
    ordering_fields = ('name', )


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
    filter_class = FacilityGPSFilter


class FacilityGPSDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityGPS.objects.all()
    serializer_class = FacilityGPSSerializer


class FacilityRegulationStatusListView(generics.ListCreateAPIView):
    queryset = FacilityRegulationStatus.objects.all()
    serializer_class = FacilityRegulationStatusSerializer
    filter_class = None
    ordering_fields = ('', )


class FacilityRegulationStatusDetailView(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityRegulationStatus.objects.all()
    serializer_class = FacilityRegulationStatusSerializer


class FacilityTypeListView(generics.ListCreateAPIView):
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer
    filter_class = None
    ordering_fields = ('name', )


class FacilityTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer


class RegulationStatusListView(generics.ListCreateAPIView):
    queryset = RegulationStatus.objects.all()
    serializer_class = FacilityRegulationStatusSerializer
    filter_class = None
    ordering_fields = ('name', )


class RegulationStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegulationStatus.objects.all()
    serializer_class = FacilityRegulationStatusSerializer
