from django.db import models
from django.conf import settings

from common.models import AbstractBase


USER_MODEL = settings.AUTH_USER_MODEL


class Role(AbstractBase):
    name = models.CharField(max_length=100)
    description = models.TextField()
    code = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Permission(AbstractBase):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class RolePermissions(AbstractBase):
    role = models.ForeignKey(Role, related_name='role_permissions')
    permission = models.ForeignKey(Permission)

    def __unicode__(self):
        return "{}: {}".format(self.role.name, self.permission.name)

    class Meta:
        unique_together = ('role', 'permission',)


class UserRoles(AbstractBase):
    user = models.ForeignKey(USER_MODEL, related_name='user_roles')
    role = models.ForeignKey(Role)

    def __unicode__(self):
        custom_string = "{}: {}".format(
            self.user.email, self.role.name)
        return custom_string
