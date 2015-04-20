from rest_framework import serializers

from common.serializers import AbstractFieldsMixin

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact
)


class CommunityHealthUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CommunityHealthUnit


class CommunityHealthWorkerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CommunityHealthWorker


class CommunityHealthWorkerContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CommunityHealthWorkerContact
