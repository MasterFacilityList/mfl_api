from rest_framework import serializers

from common.serializers import AbstractFieldsMixin

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact,
    Approver,
    CommunityHealthUnitApproval,
    CommunityHealthWorkerApproval,
    ApprovalStatus
)


class ApproverSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Approver


class ApprovalStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = ApprovalStatus


class CommunityHealthUnitApprovalSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = CommunityHealthUnitApproval


class CommunityHealthWorkerApprovalSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = CommunityHealthWorkerApproval


class CommunityHealthWorkerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta(object):
        model = CommunityHealthWorker
        read_only_fields = ('health_unit_approvals',)


class CommunityHealthUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    status_name = serializers.ReadOnlyField(source="status.name")
    health_unit_workers = CommunityHealthWorkerSerializer(
        many=True, required=False)

    class Meta(object):
        model = CommunityHealthUnit
        read_only_fields = (
            'health_unit_workers', 'health_unit_approvals', 'code',)


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
