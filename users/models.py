import reversion

from django.db import models
from django.utils import timezone
from django.core.validators import (
    validate_email, RegexValidator, ValidationError)
from django.contrib.auth.models import make_password
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group
)
from django.conf import settings
from django.template import Context, loader
from django.core.mail import EmailMultiAlternatives

from oauth2_provider.models import AbstractApplication


USER_MODEL = settings.AUTH_USER_MODEL


def send_email_on_signup(user, user_password):
    html_email_template = loader.get_template(
        "registration/registration_success.html")
    context = Context(
        {
            "user": user,
            "user_password": user_password,
            "login_url": settings.FRONTEND_URL
        }
    )
    plain_text = loader.get_template("registration/registration_success.txt")
    subject = "Account Created"
    plain_text_content = plain_text.render(context)
    html_content = html_email_template.render(context)
    mfl_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(
        subject, plain_text_content, mfl_email, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def check_password_length(raw_password):
    # use not isalpha in order to allow special characters also
    # user not isdigit to make the passsword is not a number
    if (len(raw_password) >= 8 and not raw_password.isalpha()
            and not raw_password.isdigit()):
        return True
    else:
        return False


class MflUserManager(BaseUserManager):

    def create_user(self, email, first_name,
                    username, password=None, is_staff=False, **extra_fields):
        if not check_password_length(password):
            error = "The password must be at least 8"
            "characters long and have at least one number"
            raise ValidationError(error)
        now = timezone.now()
        validate_email(email)
        p = make_password(password)
        email = MflUserManager.normalize_email(email)
        user = self.model(email=email, first_name=first_name, password=p,
                          username=username,
                          is_staff=is_staff, is_active=True,
                          is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
        user.save(using=self._db)
        send_email_on_signup(user, password)
        return user

    def create_superuser(self, email, first_name, username,
                         password, is_staff=True, **extra_fields):
        user = self.create_user(email, first_name,
                                username, password, **extra_fields)
        user.is_staff = is_staff
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super(
            MflUserManager, self).get_queryset().filter(deleted=False)


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
    first_name = models.CharField(max_length=60, null=False, blank=True)
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
    search = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    password_history = ArrayField(
        models.TextField(null=True, blank=True),
        null=True, blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = MflUserManager()
    everything = BaseUserManager()

    def set_password(self, raw_password):
        """Overridden so that we can keep track of password age"""
        super(MflUser, self).set_password(raw_password)

        # We rely on this to implement a "change password on first login"
        # roadblock

        if self.password_history:
            self.password_history.append(
                make_password(raw_password)) if self.is_authenticated else None
        else:
            self.password_history = [make_password(
                raw_password)] if self.is_authenticated else None

    def __unicode__(self):
        return self.email

    @property
    def get_short_name(self):
        return self.first_name

    @property
    def requires_password_change(self):
        return True if not self.password_history else False

    @property
    def get_full_name(self):
        return "{0} {1} {2}".format(
            self.first_name, self.last_name, self.other_names)

    @property
    def permissions(self):
        return self.get_all_permissions()

    @property
    def county(self):
        from common.models import UserCounty
        user_counties = UserCounty.objects.filter(
            user=self, active=True)
        return user_counties[0].county if user_counties else None

    @property
    def constituency(self):
        from common.models import UserConstituency
        user_consts = UserConstituency.objects.filter(
            user=self, active=True)
        return user_consts[0].constituency if user_consts else None

    @property
    def regulator(self):
        from facilities.models import RegulatoryBodyUser
        user_regulators = RegulatoryBodyUser.objects.filter(
            user=self, active=True)
        return user_regulators[0].regulatory_body if user_regulators else None

    def save(self, *args, **kwargs):
        super(MflUser, self).save(*args, **kwargs)

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view', )

        # This is not a "true permission"
        # It is a marker, used to create an is_county_level read only prop
        # on groups
        permissions = (
            (
                'county_group_marker',
                'A marker permission for county level groups'
            ),
        )
        ordering = ('-date_joined', )


Group.is_county_level = property(
    lambda self: 'county_group_marker' in [
        perm.codename for perm in self.permissions.all()]
)


class MFLOAuthApplication(AbstractApplication):

    class Meta(object):
        verbose_name = 'mfl oauth application'
        verbose_name_plural = 'mfl oauth applications'
        default_permissions = ('add', 'change', 'delete', 'view', )
