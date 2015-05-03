from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from common.serializers import InchargeCountiesSerializer
from .models import MflUser, MFLOAuthApplication


class PermissionSerializer(serializers.ModelSerializer):
    """This is intended to power a read-only view"""
    class Meta(object):
        model = Permission


class GroupSerializer(serializers.ModelSerializer):
    """This is intended to power retrieval, creation and addition of groups"""
    permissions = PermissionSerializer(many=True, required=False)

    class Meta(object):
        model = Group


class UserSerializer(serializers.ModelSerializer):
    """This should allow everything about users to be managed"""
    counties = InchargeCountiesSerializer(many=True, required=False)

    short_name = serializers.ReadOnlyField(source='get_short_name')
    full_name = serializers.ReadOnlyField(source='get_full_name')
    all_permissions = serializers.ReadOnlyField(source='permissions')

    user_permissions = PermissionSerializer(many=True, required=False)
    groups = GroupSerializer(many=True, required=False)

    class Meta(object):
        model = MflUser
        exclude = ('password',)


class MFLOAuthApplicationSerializer(serializers.ModelSerializer):
    """This powers the creation of OAuth2 applications"""

    class Meta(object):
        model = MFLOAuthApplication
