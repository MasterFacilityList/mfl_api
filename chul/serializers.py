from rest_framework import serializers

from common.serializers import AbstractFieldsMixin

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    Community,
    CommunityHealthUnitContact,
    Approver,
    CommunityHealthUnitApproval,
    CommunityHealthWorkerApproval,
    ApprovalStatus
)


class ApproverSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Approver


class ApprovalStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = ApprovalStatus


class CommunityHealthUnitApprovalSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CommunityHealthUnitApproval


class CommunityHealthWorkerApprovalSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CommunityHealthWorkerApproval


class CommunityHealthWorkerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    health_worker_approvals = CommunityHealthWorkerApprovalSerializer(
        many=True)

    class Meta:
        model = CommunityHealthWorker
        read_only_fields = ('health_unit_approvals',)


class CommunityHealthUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    health_unit_approvals = CommunityHealthWorkerApprovalSerializer(
        many=True)
    health_unit_workers = CommunityHealthWorkerSerializer(
        many=True)

    class Meta:
        model = CommunityHealthUnit
        read_only_fields = ('health_unit_workers', 'health_unit_approvals', )


class CommunityHealthWorkerContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CommunityHealthWorkerContact


class StatusSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Status


class CommunitySerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Community


class CommunityHealthUnitContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CommunityHealthUnitContact
