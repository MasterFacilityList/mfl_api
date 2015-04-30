import reversion

from django.db import models
from django.utils import timezone
from django.core.validators import validate_email, RegexValidator
from django.contrib.auth.models import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.conf import settings


USER_MODEL = settings.AUTH_USER_MODEL


class MflUserManager(BaseUserManager):
    def create(self, email, first_name,
               username, password=None, **extra_fields):
        now = timezone.now()
        validate_email(email)
        p = make_password(password)
        email = MflUserManager.normalize_email(email)
        user = self.model(email=email, first_name=first_name, password=p,
                          username=username,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, username,
                         password, **extra_fields):
        user = self.create(email, first_name,
                           username, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


@reversion.register
class MflUser(AbstractBaseUser, PermissionsMixin):
    """
    Add custom behaviour to the user model.

    Purpose of the custom model:
        1. Make email the username field.
        2. Add additional fields to the user such as county and is_national

    ``User`` is the one model that cannot descend from AbstractBase.
    """
    email = models.EmailField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=60, null=False, blank=False)
    last_name = models.CharField(max_length=60, blank=True)
    other_names = models.CharField(max_length=80, null=False, blank=True,
                                   default="")
    username = models.CharField(
        max_length=60, null=False,
        blank=False, unique=True,
        validators=[RegexValidator(
            regex=r'^\w+$',
            message='Preferred name contain only '
                    'letters numbers or underscores'
        )
        ])

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_national = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = MflUserManager()

    def __unicode__(self):
        return self.email

    @property
    def get_short_name(self):
        return self.first_name

    @property
    def get_full_name(self):
        return "{0} {1} {2}".format(
            self.first_name, self.last_name, self.other_names)

    def save(self, *args, **kwargs):
        super(MflUser, self).save(*args, **kwargs)
