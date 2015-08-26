import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import (
    validate_email, RegexValidator, ValidationError
)
from django.contrib.auth.models import make_password
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
)
from django.conf import settings
from django.template import Context, loader
from django.core.mail import EmailMultiAlternatives

from oauth2_provider.models import AbstractApplication, AccessToken
from oauth2_provider.settings import oauth2_settings


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


def check_password_strength(raw_password):
    # use not isalpha in order to allow special characters also
    # user not isdigit to make the passsword is not a number
    if (len(raw_password) >= 8 and not raw_password.isalpha() and not
            raw_password.isdigit()):
            return True
    else:
        error = (
            {
                "password": [
                    "The password must be at least 8"
                    "characters long and have at least one number"
                ]
            }
        )
        raise ValidationError(error)


class MflUserManager(BaseUserManager):

    def create_user(self, email, first_name,
                    employee_number, password=None, is_staff=False,
                    **extra_fields):
        check_password_strength(password)
        now = timezone.now()
        validate_email(email)
        p = make_password(password)
        email = MflUserManager.normalize_email(email)
        user = self.model(email=email, first_name=first_name, password=p,
                          employee_number=employee_number,
                          is_staff=is_staff, is_active=True,
                          is_superuser=False, date_joined=now, **extra_fields)
        user.save(using=self._db)
        send_email_on_signup(user, password)
        return user

    def create_superuser(self, email, first_name, employee_number,
                         password, is_staff=True, **extra_fields):
        user = self.create_user(email, first_name,
                                employee_number, password, **extra_fields)
        user.is_staff = is_staff
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super(
            MflUserManager, self).get_queryset().filter(deleted=False)


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
        max_length=60, null=True,
        blank=True, unique=True,
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
    employee_number = models.CharField(
        max_length=20, unique=True, null=False, blank=False)

    USERNAME_FIELD = 'employee_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

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
        names = [self.first_name, self.last_name, self.other_names]
        return " ".join([i for i in names if i])

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

    @property
    def lastlog(self):
        django_login = self.last_login
        token_login = None

        try:
            # not including refresh tokens since they are generated if
            # access tokens are valid
            latest_access_token = AccessToken.objects.filter(
                user=self).latest('expires')
            delta = datetime.timedelta(
                seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS
            )
            token_login = latest_access_token.expires - delta
        except AccessToken.DoesNotExist:
            pass

        if django_login is None or token_login is None:
            return django_login or token_login

        if token_login > django_login:
            return token_login

        return django_login

    def save(self, *args, **kwargs):
        super(MflUser, self).save(*args, **kwargs)

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view', )
        ordering = ('-date_joined', )


class CustomGroup(models.Model):
    group = models.OneToOneField(
        Group,
        on_delete=models.PROTECT, related_name='custom_group_fields')
    regulator = models.BooleanField(
        default=False,
        help_text="Are the regulators in this group?")
    national = models.BooleanField(
        default=False,
        help_text='Will the users in this group see all facilities in the'
        'country?')
    administrator = models.BooleanField(
        default=False,
        help_text='Will the users in this group administor user rights?')
    county_level = models.BooleanField(
        default=False,
        help_text='Will the user be creating sub county users?')
    sub_county_level = models.BooleanField(
        default=False,
        help_text='Will the user be creating users below the sub county level '
        'users?')


class ProxyGroup(Group):

    @property
    def is_regulator(self):
        try:
            return CustomGroup.objects.get(group=self).regulator
        except CustomGroup.DoesNotExist:
            return False

    @property
    def is_administrator(self):
        try:
            return CustomGroup.objects.get(group=self).administrator
        except CustomGroup.DoesNotExist:
            return False

    @property
    def is_national(self):
        try:
            return CustomGroup.objects.get(group=self).national
        except CustomGroup.DoesNotExist:
            return False

    @property
    def is_county_level(self):
        try:
            return CustomGroup.objects.get(group=self).county_level
        except CustomGroup.DoesNotExist:
            return False

    @property
    def is_sub_county_level(self):
        try:
            return CustomGroup.objects.get(group=self).county_level
        except CustomGroup.DoesNotExist:
            return False

    class Meta:
        proxy = True


class MFLOAuthApplication(AbstractApplication):

    class Meta(object):
        verbose_name = 'mfl oauth application'
        verbose_name_plural = 'mfl oauth applications'
        default_permissions = ('add', 'change', 'delete', 'view', )
