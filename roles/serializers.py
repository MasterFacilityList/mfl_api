from rest_framework import serializers

from common.serializers import AbstractFieldsMixin

from .models import (
    Role, Permission, RolePermissions, UserRoles)


class PermissionSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Permission


class RolePermissionSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    permission = PermissionSerializer()

    class Meta:
        model = RolePermissions
        exclude = ('role', )


class RolePermissionPostSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = RolePermissions


class RoleSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    role_permissions = RolePermissionSerializer(many=True, required=False)

    class Meta:
        model = Role


class UserRolesPostSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserRoles


class UserRolesSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = UserRoles
