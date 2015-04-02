from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import (
    Role, Permission, RolePermissions, UserRoles)


class BaseTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@gmail.com", "test", "test", "test")
        super(BaseTestCase, self).setUp()

    def inject_audit_fields(self, data):
        data["created_by"] = self.user
        data["updated_by"] = self.user
        data["created"] = timezone.now()
        data["updated"] = timezone.now()
        return data


class TestRoleModel(BaseTestCase):
    def test_save_role(self):
        data = {
            "name": "role",
            "description": "The description of the role"
        }
        data = self.inject_audit_fields(data)
        role = Role.objects.create(**data)
        self.assertEquals(1, Role.objects.count())
        self.assertEquals("role", role.__unicode__())


class TestPermission(BaseTestCase):
    def test_save_permission(self):
        data = {
            "name": "some permission",
            "description": "some description"
        }
        data = self.inject_audit_fields(data)
        perm = Permission.objects.create(**data)
        self.assertEquals(1, Permission.objects.count())
        self.assertEquals("some permission", perm.__unicode__())


class TestRolePermissions(BaseTestCase):
    def save_role_permission(self):
        role_data = {
            "name": "this is role name",
            "description": "This is a desc"
        }
        role_data = self.inject_audit_fields(role_data)
        role = Role.objects.create(**role_data)
        perm_data = {
            "name": "this is the perm",
            "description": "permission description"
        }
        perm_data = self.inject_audit_fields(perm_data)
        perm = Permission.objects.create(**perm_data)
        role_perm_data = {
            "role": role,
            "permission": perm
        }
        role_perm_data = self.inject_audit_fields(role_perm_data)
        role_perm = RolePermissions.objects.create(**role_perm_data)
        self.assertEquals(1, RolePermissions.objects.count())
        self.assertEquals(
            "this is role name: this is the perm", role_perm.__unicode__())


class TestUserRoles(BaseTestCase):
    def test_save_user_roles(self):
        role_data = {
            "name": "this is a role",
            "description": "this is the description"
        }
        role_data = self.inject_audit_fields(role_data)
        role = Role.objects.create(**role_data)
        user_role_data = {
            "user": self.user,
            "role": role
        }
        user_role_data = self.inject_audit_fields(user_role_data)
        user_role = UserRoles.objects.create(**user_role_data)
        self.assertEquals(1, UserRoles.objects.count())
        self.assertEquals(
            "test@gmail.com: this is a role",
            user_role.__unicode__())
