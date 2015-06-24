from rest_framework import generics
from common.views import AuditableDetailViewMixin
from common.utilities import CustomRetrieveUpdateDestroyView

from ..models import (
    FacilityServiceRating,
    ServiceCategory,
    Option,
    Service,
    FacilityService,
    ServiceOption
)

from ..serializers import (
    FacilityServiceRatingSerializer,
    ServiceCategorySerializer,
    OptionSerializer,
    ServiceSerializer,
    FacilityServiceSerializer,
    ServiceOptionSerializer

)
from ..filters import (
    ServiceCategoryFilter,
    OptionFilter,
    ServiceFilter,
    FacilityServiceFilter,
    ServiceOptionFilter

)


class ServiceCategoryListView(generics.ListCreateAPIView):
    """
    Lists and creates service categories

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    filter_class = ServiceCategoryFilter
    ordering_fields = ('name', 'description', 'abbreviation')


class ServiceCategoryDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular service category
    """
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class OptionListView(generics.ListCreateAPIView):
    """
    Lists and Creates options

    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    filter_class = OptionFilter
    ordering_fields = ('option_type', 'display_text', 'value', )


class OptionDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a a particular option
    """
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class ServiceListView(generics.ListCreateAPIView):
    """
    Lists and creates services

    category -- Service category pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_class = ServiceFilter
    ordering_fields = ('name', 'category', 'code', 'abbreviation')


class ServiceDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular service
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class FacilityServiceListView(generics.ListCreateAPIView):
    """
    Lists and creates links between facilities and services

    facility -- A facility's pk
    selected_option -- A service selected_option's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = FacilityService.objects.all()
    serializer_class = FacilityServiceSerializer
    filter_class = FacilityServiceFilter
    ordering_fields = ('facility', 'service')


class FacilityServiceDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular facility service detail
    """
    queryset = FacilityService.objects.all()
    serializer_class = FacilityServiceSerializer


class FacilityServiceRatingListView(generics.ListCreateAPIView):
    """
    Lists and creates facility's services ratings
    """
    throttle_scope = 'rating'
    queryset = FacilityServiceRating.objects.all()
    serializer_class = FacilityServiceRatingSerializer
    ordering_fields = ('rating', )


class FacilityServiceRatingDetailView(CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular facility service rating
    """
    queryset = FacilityServiceRating.objects.all()
    serializer_class = FacilityServiceRatingSerializer


class ServiceOptionListView(generics.ListCreateAPIView):
    """
    Lists and creates service options

    service -- A service's pk
    option -- An option's pk
    Created --  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = ServiceOption.objects.all()
    serializer_class = ServiceOptionSerializer
    filter_class = ServiceOptionFilter
    ordering_fields = ('service', 'option',)


class ServiceOptionDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular service option
    """
    queryset = ServiceOption.objects.all()
    serializer_class = ServiceOptionSerializer
