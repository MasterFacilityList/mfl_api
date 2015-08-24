from rest_framework import generics
from rest_framework import status
from rest_framework.views import Response, APIView

from common.views import AuditableDetailViewMixin
from common.utilities import CustomRetrieveUpdateDestroyView

from ..models import (
    FacilityServiceRating,
    ServiceCategory,
    Option,
    OptionGroup,
    Service,
    FacilityService
)

from ..serializers import (
    FacilityServiceRatingSerializer,
    ServiceCategorySerializer,
    OptionSerializer,
    ServiceSerializer,
    OptionGroupSerializer,
    FacilityServiceSerializer
)
from ..filters import (
    ServiceCategoryFilter,
    OptionFilter,
    ServiceFilter,
    FacilityServiceFilter
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


class PostOptionGroupWithOptionsView(APIView):
    serializer_class = OptionGroupSerializer
    errors = []

    def _validate_option_group_name_value_ok(self, option_group):
        option_group_obj = OptionGroupSerializer(data=option_group)
        if not option_group_obj.is_valid():
            self.errors.append(option_group_obj.errors)

    def _validate_option(self, options):
        for option in options:

            required = ["value", "display_text", "option_type"]
            if not set(required) <= set(option.keys()):
                error = [
                    "Ensure option has value, display text and option type"
                ]
                self.errors.append({"option": error})

    def _save_option_group(self, option_group):
        option_group = self._inject_user_from_request(option_group)
        import pdb
        pdb.set_trace()
        created_option_group = OptionGroup.objects.create(**option_group)
        return created_option_group

    def _inject_user_from_request(self, dict_obj):
        dict_obj['created_by_id'] = self.request.user.id
        dict_obj['updated_by_id'] = self.request.user.id
        return dict_obj

    def _save_options(self, options, option_group):
        for option in options:
            option['group'] = option_group
            option = self._inject_user_from_request(option)
            Option.objects.create(**option)

    def post(self, *args, **kwargs):
        data = self.request.data
        option_group = data.get('option_group')
        option_group_dict = {
            "name": option_group
        }
        options = data.get('options')
        self._validate_option_group_name_value_ok(option_group_dict)
        self._validate_option(options)
        if len(self.errors) is 0:
            created_group = self._save_option_group(option_group_dict)
            self._save_options(options, created_group)
            return Response(data=OptionGroupSerializer(
                created_group).data, status=status.HTTP_201_CREATED)
        else:
            data = {"detail": self.errors}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
