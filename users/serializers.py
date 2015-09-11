from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import Permission

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_auth.serializers import PasswordChangeSerializer

from common.serializers import (
    UserCountySerializer,
    UserConstituencySerializer,
    UserContactSerializer,
    PartialResponseMixin
)
from facilities.serializers import RegulatoryBodyUserSerializer
from .models import (
    MflUser,
    MFLOAuthApplication,
    check_password_strength,
    CustomGroup,
    ProxyGroup)


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
            ProxyGroup.objects.get(**user_supplied_group)
            for user_supplied_group in user_supplied_groups
        ]
    except Exception as ex:  # Will reraise a more API friendly exception
        raise ValidationError(
            '"{}"" when retrieving groups corresponding to "{}"'
            .format(ex, validated_data)
        )


class PermissionSerializer(serializers.ModelSerializer):

    """This is intended to power a read-only view"""
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    codename = serializers.ReadOnlyField()

    class Meta(object):
        model = Permission
        fields = ('id', 'name', 'codename',)


class GroupSerializer(PartialResponseMixin, serializers.ModelSerializer):

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
    is_regulator = serializers.ReadOnlyField()
    is_national = serializers.ReadOnlyField()
    is_administrator = serializers.ReadOnlyField()
    is_county_level = serializers.ReadOnlyField()
    is_sub_county_level = serializers.ReadOnlyField()

    @transaction.atomic
    def create(self, validated_data):
        regulator = self.initial_data.pop('is_regulator', False)
        national = self.initial_data.pop('is_national', False)
        admin = self.initial_data.pop('is_administrator', False)
        county_level = self.initial_data.pop('is_county_level', False)
        sub_county_level = self.initial_data.pop('is_sub_county_level', False)
        permissions = _lookup_permissions(
            self.context['request'].DATA
        )
        validated_data.pop('permissions', None)

        new_group = ProxyGroup(**validated_data)
        new_group.save()
        new_group.permissions.add(*permissions)
        custom_group_data = {
            "regulator": regulator,
            "national": national,
            "administrator": admin,
            'county_level': county_level,
            'sub_county_level': sub_county_level,
            "group": new_group
        }
        CustomGroup.objects.create(**custom_group_data)
        return new_group

    @transaction.atomic
    def update(self, instance, validated_data):
        regulator = self.initial_data.pop(
            'is_regulator', instance.is_regulator)
        national = self.initial_data.pop(
            'is_national', instance.is_national)
        admin = self.initial_data.pop(
            'is_administrator', instance.is_administrator)
        county_level = self.initial_data.pop(
            'is_county_level', instance.is_county_level)
        sub_county_level = self.initial_data.pop(
            'is_sub_county_level', instance.is_sub_county_level)
        permissions = _lookup_permissions(
            self.context['request'].DATA
        )
        validated_data.pop('permissions', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.permissions.clear()
        instance.permissions.add(*permissions)
        custom_group_data = {
            "regulator": regulator,
            "national": national,
            "administrator": admin,
            "county_level": county_level,
            "sub_county_level": sub_county_level,
            "group": instance
        }
        try:
            cg = CustomGroup.objects.get(group=instance)
            for key, value in custom_group_data.iteritems():
                setattr(cg, key, value)
            cg.save()
        except CustomGroup.DoesNotExist:
            CustomGroup.objects.create(**custom_group_data)

        return instance

    def get_fields(self):
        """Overridden to take advantage of partial response"""
        origi_fields = super(GroupSerializer, self).get_fields()
        request = self.context.get('request', None)
        return self.strip_fields(request, origi_fields)

    class Meta(object):
        model = ProxyGroup


class MflUserSerializer(PartialResponseMixin, serializers.ModelSerializer):

    """This should allow everything about users to be managed"""
    user_counties = UserCountySerializer(many=True, required=False)

    short_name = serializers.ReadOnlyField(source='get_short_name')
    full_name = serializers.ReadOnlyField(source='get_full_name')
    all_permissions = serializers.ReadOnlyField(source='permissions')

    requires_password_change = serializers.ReadOnlyField()

    user_permissions = PermissionSerializer(many=True, required=False)
    groups = GroupSerializer(many=True, required=False)
    regulator = serializers.ReadOnlyField(source='regulator.id')
    regulator_name = serializers.ReadOnlyField(source='regulator.name')
    county = serializers.ReadOnlyField(source='county.id')
    county_name = serializers.ReadOnlyField(source='county.name')
    constituency = serializers.ReadOnlyField(source='constituency.id')
    constituency_name = serializers.ReadOnlyField(
        source='constituency.name')
    user_contacts = UserContactSerializer(many=True, required=False)
    regulatory_users = RegulatoryBodyUserSerializer(many=True, required=False)
    user_constituencies = UserConstituencySerializer(many=True, required=False)
    last_login = serializers.ReadOnlyField(source='lastlog')

    def _upadate_validated_data_with_audit_fields(
            self, validated_data, is_creation=False):
        if is_creation:
            validated_data['created_by'] = self.context['request'].user
            validated_data['created'] = timezone.now()
        validated_data['updated_by'] = self.context['request'].user
        validated_data['updated'] = timezone.now()
        return validated_data

    @transaction.atomic
    def create(self, validated_data):
        validated_data = self._upadate_validated_data_with_audit_fields(
            validated_data, is_creation=True)
        groups = _lookup_groups(validated_data)
        validated_data.pop('groups', None)

        new_user = MflUser.objects.create_user(**validated_data)
        new_user.save()
        new_user.groups.add(*groups)

        return new_user

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data = self._upadate_validated_data_with_audit_fields(
            validated_data)
        groups = _lookup_groups(validated_data)
        validated_data.pop('groups', None)

        pwd = validated_data.pop('password', None)

        # This does not handle password changes intelligently
        # Use the documented password change endpoints
        # Also: teach your API consumers to always prefer PATCH to PUT
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if pwd is not None:
            instance.set_password(pwd)

        instance.save()

        instance.groups.clear()
        instance.groups.add(*groups)

        return instance

    def get_fields(self):
        """Overridden to take advantage of partial response"""
        origi_fields = super(MflUserSerializer, self).get_fields()
        request = self.context.get('request', None)
        return self.strip_fields(request, origi_fields)

    class Meta(object):
        model = MflUser
        exclude = ('password_history', )
        extra_kwargs = {'password': {'write_only': True}}


class MFLOAuthApplicationSerializer(serializers.ModelSerializer):

    """This powers the creation of OAuth2 applications"""

    class Meta(object):
        model = MFLOAuthApplication


class MflPasswordChangeSerializer(PasswordChangeSerializer):

    def validate(self, attrs):
        super(MflPasswordChangeSerializer, self).validate(attrs)
        check_password_strength(attrs['new_password1'])
        return attrs
