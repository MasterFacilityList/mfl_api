from django.db import models
from django.utils import timezone
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import make_password
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.conf import settings

from common.models import County, AbstractBase


USER_MODEL = settings.AUTH_USER_MODEL


class MflUserManager(BaseUserManager):
    def create_user(self, email, first_name,
                    username, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The email must be set')
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
        user = self.create_user(email, first_name,
                                username, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MflUser(AbstractBaseUser, PermissionsMixin):
    """
    Add custom behaviour to the user model.

    Purpose of the custom model:
        1. Make email the username field.
        2. Add additional fields to the user such as county and is_national
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
    county = models.ForeignKey(County, null=True, blank=True)
    is_national = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MflUserManager()

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return "{0} {1} {2}".format(
            self.first_name, self.last_name, self.other_names)

    def save(self, *args, **kwargs):
        super(MflUser, self).save(*args, **kwargs)


class UserCounties(AbstractBase):
    """
    Will store a record of the counties that a user has been incharge of.

    A user can only be incharge of only one county at a time.
    """

    user = models.ForeignKey(MflUser, related_name='user_counties')
    county = models.ForeignKey(County)
    is_active = models.BooleanField(
        default=True,
        help_text="Is the user currently incharge of the county?")

    def __unicode___(self):
        return "{}: {}".format(self.user.email, self.county.name)

    def validate_only_one_county_active(self):
        """
        A user can be incharge of only one county at the a time.
        """
        counties = self.__class___.objects.filter(
            user=self.user, is_active=True)
        if counties.count() > 0:
            raise ValidationError(
                "A user can only be active in one county at a time")

    def save(self, *args, **kwargs):
        self.validate_only_one_county_active()
        super(UserCounties, self).save(*args, **kwargs)
