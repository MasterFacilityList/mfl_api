from django.db import models
from django.contrib.auth import get_user_model

from common.models import AbstractBase


USER_MODEL = get_user_model()


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
    user =  models.ForeignKey(USER_MODEL)
    role = models.ForeignKey(Role)

    def __unicode__(self):
        custom_string = "{} {}".format(
            self.user.email, self.role.name)
        return custom_string
