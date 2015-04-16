from rest_framework import generics


from ..models import(
    RatingScale, Rating, FacilityRatingScale, FacilityServiceRatingScale,
    UserFacilityRating, UserFacilityServiceRating)

from ..serializers import (
    RatingScaleSerializer, RatingSerializer,
    FacilityRatingScaleSerializer, FacilityServiceRatingScaleSerializer,
    UserFacilityRatingSerializer, UserFacilityServiceRatingSerializer)


from ..filters import (
    RatingScaleFilter, RatingFilter, FacilityRatingScaleFilter,
    FacilityServiceRatingScaleFilter, UserFacilityRatingFilter,
    UserFacilityServiceRatingFilter)


class RatingScaleListView(generics.ListCreateAPIView):
    queryset = RatingScale.objects.all()
    serializer_class = RatingScaleSerializer
    filter_class = RatingScaleFilter
    ordering_fields = ('name',)


class RatingScaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RatingScale.objects.all()
    serializer_class = RatingScaleSerializer


class RatingListView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_class = RatingFilter
    ordering_fields = ('scale', 'rating_code', )


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class FacilityRatingScaleListView(generics.ListCreateAPIView):
    queryset = FacilityRatingScale.objects.all()
    filter_class = FacilityRatingScaleFilter
    serializer_class = FacilityRatingScaleSerializer
    ordering_fields = ('facility', 'scale', )


class FacilityRatingScaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityRatingScale.objects.all()
    serializer_class = FacilityRatingScaleSerializer


class FacilityServiceRatingScaleListView(generics.ListCreateAPIView):
    queryset = FacilityServiceRatingScale.objects.all()
    serializer_class = FacilityServiceRatingScaleSerializer
    filter_class = FacilityServiceRatingScaleFilter
    ordering_fields = ('facility_service', 'scale', )


class FacilityServiceRatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacilityServiceRatingScale.objects.all()
    serializer_class = FacilityServiceRatingScaleSerializer


class UserFacilityRatingListView(generics.ListCreateAPIView):
    queryset = UserFacilityRating.objects.all()
    serializer_class = UserFacilityRatingSerializer
    filter_class = UserFacilityRatingFilter
    ordering_fields = ('facility', 'user', 'rating', )


class UserFacilityRatingDetailView(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = UserFacilityRating.objects.all()
    serializer_class = UserFacilityRatingSerializer


class UserFacilityServiceRatingListView(generics.ListCreateAPIView):
    queryset = UserFacilityServiceRating.objects.all()
    serializer_class = UserFacilityServiceRatingSerializer
    filter_class = UserFacilityServiceRatingFilter
    ordering_fields = ('facility_service', 'user', 'rating',)


class UserFacilityServiceRatingDetailView(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = UserFacilityServiceRating.objects.all()
    serializer_class = UserFacilityServiceRatingSerializer
