import logging

from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import Permission, Group

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_auth.serializers import PasswordChangeSerializer

from common.serializers import (
    UserCountySerializer,
    UserConstituencySerializer,
    PartialResponseMixin,
    UserSubCountySerializer
)

from common.models import (
    UserConstituency, UserContact, UserCounty, Contact,
    UserSubCounty,)
from facilities.serializers import RegulatoryBodyUserSerializer
from facilities.models import RegulatoryBodyUser
from .models import (
    MflUser,
    MFLOAuthApplication,
    check_password_strength,
    CustomGroup,
    ProxyGroup)


LOGGER = logging.getLogger(__name__)


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
        for user_supplied_group in user_supplied_groups:
            user_supplied_group.pop('permissions', None)

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

    def update_users_in_group(self, instance):

        group = Group.objects.get(id=instance.id)
        for user in MflUser.objects.all():
            user.is_staff = True if group in \
                user.groups.all() else False
            user.save()

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
        self.update_users_in_group(instance)
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
    groups = GroupSerializer(many=True, required=False)
    regulator = serializers.ReadOnlyField(source='regulator.id')
    regulator_name = serializers.ReadOnlyField(source='regulator.name')
    county = serializers.ReadOnlyField(source='county.id')
    county_name = serializers.ReadOnlyField(source='county.name')
    constituency = serializers.ReadOnlyField(source='constituency.id')
    constituency_name = serializers.ReadOnlyField(source='constituency.name')
    sub_county_name = serializers.ReadOnlyField(source='sub_county.name')
    contacts = serializers.ReadOnlyField()
    regulatory_users = RegulatoryBodyUserSerializer(many=True, required=False)
    user_constituencies = UserConstituencySerializer(many=True, required=False)
    user_sub_counties = UserSubCountySerializer(many=True, required=False)
    last_login = serializers.ReadOnlyField(source='lastlog')
    user_groups = serializers.ReadOnlyField()
    job_title_name = serializers.ReadOnlyField(source='job_title.name')

    def _upadate_validated_data_with_audit_fields(
            self, validated_data, is_creation=False):
        if is_creation:
            validated_data['created_by'] = self.context['request'].user
            validated_data['created'] = timezone.now()
        validated_data['updated_by'] = self.context['request'].user
        validated_data['updated'] = timezone.now()
        return validated_data

    def _assign_is_staff(self, user_groups):
        for group in user_groups:
            if group.is_administrator:
                return True
        return False

    def _update_or_create_contacts(self, instance, contacts):
        """
        Creates and updates user contacts in bulk

        Sample Payload:
            "user_contacts": [
                {
                    "id": <UserContact instance> // optional and provided
                        only when updating a uuid string
                    "contact": "the contact e.g 07224645657",
                    "contact_type": "the pk of the contact type" // uuid string
                }
            ]
        """
        for contact in contacts:
            if 'id' in contact:
                try:
                    user_contact_obj = UserContact.objects.get(
                        id=contact.get('id'))
                    user_contact_obj.contact.contact = contact.get(
                        'contact_text')
                    user_contact_obj.contact.contact_type_id = contact.get(
                        'contact_type')
                    user_contact_obj.contact.save()
                except UserContact.DoesNotExist:
                    msg = "User contact with id {0} does not exist".format(
                        contact.get('id'))
                    raise ValidationError(
                        {
                            "user_contact": [msg]
                        })
            else:
                contact['updated_by_id'] = self.context.get(
                    'request').user.id
                contact['created_by_id'] = self.context.get(
                    'request').user.id
                contact['contact_type_id'] = contact.pop('contact_type')
                contact['contact'] = contact.pop('contact_text')
                contact_obj = Contact.objects.create(**contact)
                user_contact = {}
                user_contact['updated_by_id'] = self.context.get(
                    'request').user.id
                user_contact['created_by_id'] = self.context.get(
                    'request').user.id
                user_contact['user_id'] = instance.id
                user_contact['contact_id'] = contact_obj.id
                UserContact.objects.create(**user_contact)

    def _create_user_county(self, instance, counties):
        """
        Allows batch linking of a user to counties

        Sample Payload:
            "user_counties": [
                {
                    "id": <UserCounty instance> // optional and provided
                        only when updating a uuid string
                    "county": "The county id of
                    the county to be linked",// uuid string

                }
            ]
        """
        updated_counties = []
        user = self.context.get('request').user

        UserCounty.everything.filter(user=instance).delete()
        for county in counties:
            county_obj = {}
            county_obj['updated_by'] = user
            county_obj['created_by'] = user
            county_obj['county_id'] = county.pop('id')
            county_obj['user'] = instance
            county_obj['active'] = county.get('active', True)
            UserCounty.objects.create(**county_obj)
            updated_counties.append(str(county_obj['county_id']))

    def _create_user_constituency(self, instance, constituencies):
        """
        Allow batch linking of users to constituencies.

        Sample Payload:
            "user_constituencies": [
                {
                    "id": <UserConstituency instance> // optional and provided
                        only when updating a uuid string
                    "constituency": "The constituency id of
                        the constituency to be linked",// uuid string

                }
            ]
        """
        updated_consts = []
        user = self.context.get('request').user
        UserConstituency.everything.filter(user=instance).delete()
        for constituency in constituencies:
            constituency_obj = {}
            constituency_obj['updated_by'] = user
            constituency_obj['created_by'] = user
            constituency_obj['constituency_id'] = constituency.pop(
                'id')
            updated_consts.append(str(constituency_obj['constituency_id']))
            constituency_obj['user'] = instance
            constituency_obj['active'] = constituency.get('active', True)
            UserConstituency.objects.create(**constituency_obj)

    def _create_user_sub_counties(self, instance, sub_counties):
        """
        Allow batch linking of users to sub_counties.

        Sample Payload:
            "user_sub_counties": [
                {
                    "id": <UserSubCounty instance> // optional and provided
                        only when updating a uuid string
                    "sub_county": "The sub_county id of
                        the sub_county to be linked",// uuid string

                }
            ]
        """
        updated_subs = []
        user = self.context.get('request').user
        UserSubCounty.everything.filter(user=instance).delete()
        for sub_county in sub_counties:
            sub_county_obj = {}
            sub_county_obj['updated_by'] = user
            sub_county_obj['created_by'] = user
            sub_county_obj['sub_county_id'] = sub_county.pop(
                'id')
            updated_subs.append(str(sub_county_obj['sub_county_id']))
            sub_county_obj['user'] = instance
            sub_county_obj['active'] = sub_county.get('active', True)
            UserSubCounty.objects.create(**sub_county_obj)

    def _create_regulator(self, instance, regulators):
        """
        Links a user to a regulatory body.

        Sample Payload:
             "regulatory_users": [
                {
                    "id": <RegulatoryBodyUser instance>
                        // optional and provided
                        only when updating a uuid string
                    "regulatory_body": "The regulatory body id of
                        the regulatory body to be linked",// uuid string

                }
            ]

        """
        for regulator in regulators:
            if 'id' in regulator:
                LOGGER.info("The user is already linked to that regulator")
            else:
                regulator['updated_by_id'] = self.context.get(
                    'request').user.id
                regulator['created_by_id'] = self.context.get(
                    'request').user.id
                regulator['user'] = instance
                regulator['regulatory_body_id'] = regulator.pop(
                    'regulatory_body')
                RegulatoryBodyUser.objects.create(**regulator)

    @transaction.atomic
    def create(self, validated_data):
        validated_data = self._upadate_validated_data_with_audit_fields(
            validated_data, is_creation=True)
        groups = _lookup_groups(validated_data)
        validated_data.pop('groups', None)
        validated_data.pop('contacts', None)
        contacts = self.initial_data.pop('contacts', [])
        validated_data.pop('user_constituencies', None)
        constituencies = self.initial_data.pop('user_constituencies', [])
        sub_counties = self.initial_data.pop('user_sub_counties', [])
        validated_data.pop('user_sub_counties', None)
        validated_data.pop('user_counties', None)
        counties = self.initial_data.pop('user_counties', [])
        validated_data.pop('regulatory_users', None)
        regulators = self.initial_data.pop('regulatory_users', [])

        new_user = MflUser.objects.create_user(**validated_data)
        if self._assign_is_staff(groups):
            new_user.is_staff = True
        new_user.save()

        new_user.groups.add(*groups)
        self._create_user_constituency(new_user, constituencies)
        self._create_user_county(new_user, counties)
        self._update_or_create_contacts(new_user, contacts)
        self._create_regulator(new_user, regulators)
        self._create_user_sub_counties(new_user, sub_counties)

        return new_user

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data = self._upadate_validated_data_with_audit_fields(
            validated_data)
        groups = _lookup_groups(validated_data)
        validated_data.pop('groups', None)

        validated_data.pop('contacts', None)
        contacts = self.initial_data.pop('contacts', [])
        validated_data.pop('user_constituencies', None)
        constituencies = self.initial_data.pop('user_constituencies', [])
        validated_data.pop('user_counties', None)
        counties = self.initial_data.pop('user_counties', [])
        sub_counties = self.initial_data.pop('user_sub_counties', [])
        validated_data.pop('user_sub_counties', None)
        validated_data.pop('regulatory_users', None)
        regulators = self.initial_data.pop('regulatory_users', [])

        pwd = validated_data.pop('password', None)

        # This does not handle password changes intelligently
        # Use the documented password change endpoints
        # Also: teach your API consumers to always prefer PATCH to PUT
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if pwd is not None:
            instance.set_password(pwd)
        if self._assign_is_staff(groups):

            instance.is_staff = True
        instance.save()
        instance.groups.clear()
        instance.groups.add(*groups)

        self._create_user_constituency(instance, constituencies)
        self._create_user_county(instance, counties)
        self._update_or_create_contacts(instance, contacts)
        self._create_regulator(instance, regulators)
        self._create_user_sub_counties(instance, sub_counties)

        return instance

    def get_fields(self):
        """Overridden to take advantage of partial response"""
        origi_fields = super(MflUserSerializer, self).get_fields()
        request = self.context.get('request', None)
        return self.strip_fields(request, origi_fields)

    class Meta(object):
        model = MflUser
        exclude = ('password_history', 'user_permissions', )
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
