from django.shortcuts import get_object_or_404

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
    FacilityServiceFilter,
    FacilityServiceRatingFilter
)


class FlattenedCategories(generics.GenericAPIView):

    """Specialized endpoint to filter out :
        - parent categories
        - categories without services
        This is a temporary fix and will be removed
    """

    def get(self, *args, **kwargs):
        vals = Service.objects.values(
                'category', 'category__name'
            ).distinct().order_by()
        vals = [  # is there a better way of doing alias in django ?
            {"id": i["category"], "name": i["category__name"]}
            for i in vals
        ]
        return Response({"count": len(vals), "results": vals})


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
    filter_class = FacilityServiceRatingFilter
    ordering_fields = ('rating', )


class FacilityServiceRatingDetailView(CustomRetrieveUpdateDestroyView):
    """
    Retrieves a particular facility service rating
    """
    queryset = FacilityServiceRating.objects.all()
    serializer_class = FacilityServiceRatingSerializer


class PostOptionGroupWithOptionsView(APIView):
    serializer_class = OptionGroupSerializer

    def _save_option_group(self, option_group):
        option_group = self._inject_user_from_request(option_group)

        try:
            group_in_db = OptionGroup.objects.get(id=option_group['id'])
            for key, value in option_group.iteritems():
                setattr(group_in_db, key, value)
            group_in_db.save()
            return group_in_db
        except (KeyError, OptionGroup.DoesNotExist):
            created_option_group = OptionGroup.objects.create(**option_group)
            return created_option_group

    def _inject_user_from_request(self, dict_obj):
        dict_obj['created_by_id'] = self.request.user.id
        dict_obj['updated_by_id'] = self.request.user.id
        return dict_obj

    def _save_options(self, options, option_group):
        for option in options:
            try:
                option_in_db = Option.objects.get(id=option["id"])
                option.pop("group", None)
                option.pop("created_by", None)
                option.pop("updated_by", None)
                option.pop('id')
                for key, value in option.iteritems():
                    setattr(option_in_db, key, value)
                option_in_db.save()

            except (KeyError, Option.DoesNotExist):
                option['group'] = option_group
                option = self._inject_user_from_request(option)
                Option.objects.create(**option)

    def post(self, *args, **kwargs):
        data = self.request.data
        option_group = data.get('name')
        option_group_dict = {
            "name": option_group
        }
        option_group_dict["id"] = data.get('id') if data.get('id') else None
        options = data.get('options')

        created_group = self._save_option_group(option_group_dict)
        self._save_options(options, created_group)
        return Response(data=OptionGroupSerializer(
            created_group).data, status=status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        option_group_id = kwargs.pop('pk', None)
        option_group = get_object_or_404(OptionGroup, id=option_group_id)
        [
            option.delete() for option in Option.objects.filter(
                group=option_group)
        ]
        option_group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
