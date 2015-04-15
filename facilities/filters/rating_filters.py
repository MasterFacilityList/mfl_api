import django_filters

from ..models import(
    RatingScale, Rating, FacilityRatingScale, FacilityServiceRatingScale,
    UserFacilityRating, UserFacitlityServiceRating)
from common.filters.filter_shared import CommonFieldsFilterset


class RatingScaleFilter(CommonFieldsFilterset):
    name = django_filters.CharFilter(lookup_type='icontains')
    description = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = RatingScale


class RatingFilter(CommonFieldsFilterset):
    scale = django_filters.AllValuesFilter(lookup_type='exact')
    description = django_filters.CharFilter(lookup_type='icontains')
    rating_code = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Rating


class FacilityRatingScaleFilter(CommonFieldsFilterset):
    scale = django_filters.AllValuesFilter(lookup_type='exact')
    facility = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = FacilityRatingScale


class FacilityServiceRatingScaleFilter(CommonFieldsFilterset):
    facility_service = django_filters.AllValuesFilter(lookup_type='exact')
    scale = django_filters.AllValuesFilter(lookup_type='exact')

    class Meta:
        model = FacilityServiceRatingScale


class UserFacilityRatingFilter(CommonFieldsFilterset):
    user = django_filters.AllValuesFilter(lookup_type='exact')
    facility = django_filters.AllValuesFilter(lookup_type='exact')
    comment = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = UserFacilityRating


class UserFacilityServiceRatingFilter(CommonFieldsFilterset):
    facility_service = django_filters.AllValuesFilter(lookup_type='exact')
    user = django_filters.AllValuesFilter(lookup_type='exact')
    comment = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = UserFacitlityServiceRating
