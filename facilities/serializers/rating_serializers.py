from rest_framework import serializers

from common.serializers import AbstractFieldsMixin


from ..models import(
    RatingScale, Rating, FacilityRatingScale, FacilityServiceRatingScale,
    UserFacilityRating, UserFacitlityServiceRating)


class RatingScaleSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = RatingScale


class RatingSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Rating


class FacilityRatingScaleSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = FacilityRatingScale


class FacilityServiceRatingScaleSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = FacilityServiceRatingScale


class UserFacilityRatingSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserFacilityRating


class UserFacilityServiceRatingSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserFacitlityServiceRating
