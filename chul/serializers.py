from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.serializers import AbstractFieldsMixin

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact,
    CHUService
)


class CHUServiceSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = CHUService


class CommunityHealthWorkerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta(object):
        model = CommunityHealthWorker
        read_only_fields = ('health_unit_approvals',)


class CommunityHealthWorkerPostSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta(object):
        model = CommunityHealthWorker
        exclude = ('health_unit',)


class CommunityHealthUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    status_name = serializers.ReadOnlyField(source="status.name")
    inlined_errors = {}

    class Meta(object):
        model = CommunityHealthUnit
        read_only_fields = ('code',)

    def _validate_chew(self, chews, context):
        for chew in chews:
            chew_data = CommunityHealthWorkerPostSerializer(
                data=chew, context=context)
            if chew_data.is_valid():
                pass
            else:
                self.inlined_errors.update(chew_data.errors)

    def save_chew(self, instance, chews, context):
        for chew in chews:
            chew['health_unit'] = instance.id
            chew_data = CommunityHealthWorkerSerializer(
                data=chew, context=context)
            chew_data.save() if chew_data.is_valid() else None

    def create(self, validated_data):
        chews = self.initial_data.pop('health_unit_workers', [])
        self._validate_chew(chews, self.context)

        if not self.inlined_errors:
            chu = super(CommunityHealthUnitSerializer, self).create(
                validated_data)
            self.save_chew(chu, chews, self.context)
            return chu
        else:
            raise ValidationError(self.errors)

    def update(self, instance, validated_data):
        chews = self.initial_data.pop('health_unit_workers', [])
        super(CommunityHealthUnitSerializer, self).update(
            instance, validated_data)
        self.save_chew(instance, chews, self.context)
        return instance


class CommunityHealthWorkerContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = CommunityHealthWorkerContact


class StatusSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Status


class CommunityHealthUnitContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = CommunityHealthUnitContact
