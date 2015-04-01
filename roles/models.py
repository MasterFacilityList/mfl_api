from django.db import models
from django.conf import settings

from common.models import AbstractBase


USER_MODEL = settings.AUTH_USER_MODEL


INITIAL_ROLES = (
    ('REGULATOR', ''),
    ('SCHMT', ''),
    ('APPROVER', ''),
)


class Role(AbstractBase):
    name = models.CharField(max_length=100)
    description = models.TextField()
    code = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class UserRoles(AbstractBase):
    user =  models.ForeignKey(USER_MODEL, related_name='user_roles')
    role = models.ForeignKey(Role)

    def __unicode__(self):
        custom_string = "{} {}".format(
            self.user.email, self.role.name)
        return custom_string
