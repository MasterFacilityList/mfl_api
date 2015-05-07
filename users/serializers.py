from django.db import transaction
from django.contrib.auth.models import Group, Permission

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.serializers import UserCountySerializer
from .models import MflUser, MFLOAuthApplication


def _lookup_permissions(validated_data):
    user_supplied_permissions = validated_data.get('permissions', [])
    try:
        return [
            Permission.objects.get(**user_supplied_permission)
            for user_supplied_permission in user_supplied_permissions
        ]
    except Exception as ex:  # Will reraise a more API friendly exception
        raise ValidationError(
            '"{}"" when retrieving permissions corresponding to "{}"'
            .format(ex, user_supplied_permissions)
        )


def _lookup_groups(validated_data):
    try:
        user_supplied_groups = validated_data.get('groups', [])
        return [
            Group.objects.get(**user_supplied_group)
            for user_supplied_group in user_supplied_groups
        ]
    except Exception as ex:  # Will reraise a more API friendly exception
        raise ValidationError(
            '"{}"" when retrieving groups corresponding to "{}"'
            .format(ex, user_supplied_groups)
        )


class PermissionSerializer(serializers.ModelSerializer):
    """This is intended to power a read-only view"""
    class Meta(object):
        model = Permission
        fields = ('id', 'name', 'codename',)


class GroupSerializer(serializers.ModelSerializer):
    """This is intended to power retrieval, creation and addition of groups

    # Assigning permissions to a group
    For each permission, send the `id`, `name` and `codename`, as obtained
    from `/api/users/permissions/`.

    This is an example payload `POST`ed to `/api/users/groups/`:

        {
            "name": "Documentation Example Group",
            "permissions": [
                {
                    "id": 61,
                    "name": "Can add email address",
                    "codename": "add_emailaddress"
                },
                {
                    "id": 62,
                    "name": "Can change email address",
                    "codename": "change_emailaddress"
                }
            ]
        }

    # Updating the permissions of an existing group
    This API **replaces** all the existing permissions.
    """
    # Don't even ask; in order for the manual create() in the user serializer
    # to work, the UniqueValidator on this name had to be silenced
    name = serializers.CharField(validators=[])
    permissions = PermissionSerializer(many=True, required=False)

    @transaction.atomic
    def create(self, validated_data):
        permissions = _lookup_permissions(validated_data)
        validated_data.pop('permissions', None)

        new_group = Group(**validated_data)
        new_group.save()
        new_group.permissions.add(*permissions)
        return new_group

    @transaction.atomic
    def update(self, instance, validated_data):
        permissions = _lookup_permissions(validated_data)
        validated_data.pop('permissions', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.permissions.clear()
        instance.permissions.add(*permissions)
        return instance

    class Meta(object):
        model = Group


class MflUserSerializer(serializers.ModelSerializer):
    """This should allow everything about users to be managed"""
    counties = UserCountySerializer(many=True, required=False)

    short_name = serializers.ReadOnlyField(source='get_short_name')
    full_name = serializers.ReadOnlyField(source='get_full_name')
    all_permissions = serializers.ReadOnlyField(source='permissions')

    requires_password_change = serializers.ReadOnlyField()

    user_permissions = PermissionSerializer(many=True, required=False)
    groups = GroupSerializer(many=True, required=False)

    @transaction.atomic
    def create(self, validated_data):
        groups = _lookup_groups(validated_data)
        validated_data.pop('groups', None)

        new_user = MflUser.objects.create(**validated_data)
        new_user.save()
        new_user.groups.add(*groups)

        return new_user

    @transaction.atomic
    def update(self, instance, validated_data):
        groups = _lookup_groups(validated_data)
        validated_data.pop('groups', None)

        # This does not handle password changes intelligently
        # Use the documented password change endpoints
        # Also: teach your API consumers to always prefer PATCH to PUT
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.groups.clear()
        instance.groups.add(*groups)

        return instance

    class Meta(object):
        model = MflUser
        exclude = ('password_history',)
        extra_kwargs = {'password': {'write_only': True}}


class MFLOAuthApplicationSerializer(serializers.ModelSerializer):
    """This powers the creation of OAuth2 applications"""

    class Meta(object):
        model = MFLOAuthApplication
