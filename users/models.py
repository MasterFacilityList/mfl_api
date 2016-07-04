import reversion
import datetime
import uuid

from smtplib import socket, SMTPAuthenticationError
from django.db import models
from django.utils import timezone, encoding
from django.core.validators import (
    validate_email, RegexValidator, ValidationError
)
from django.contrib.auth.models import make_password
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
)
from django.conf import settings
from django.template import Context, loader
from django.core.mail import EmailMultiAlternatives

from celery import shared_task
from oauth2_provider.models import AbstractApplication, AccessToken
from oauth2_provider.settings import oauth2_settings


@shared_task(name='send_user_email')
def send_email_on_signup(
        user_id, email, first_name, employee_number, user_password=None):
    from common.models import ErrorQueue
    sent = False
    html_email_template = loader.get_template(
        "registration/registration_success.html")
    context = Context(
        {
            "email": email,
            "first_name": first_name,
            "employee_number": employee_number,
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
        subject, plain_text_content, mfl_email, [email])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        sent = True
    except socket.gaierror:
        ErrorQueue.objects.get_or_create(
            object_pk=user_id,
            error_type="SEND_EMAIL_ERROR",
            app_label='users',
            model_name='MflUser',
            except_message=(
                'Unable to send user email; Please confirm that email'
                ' settings are present in the environment')
        )
    except SMTPAuthenticationError:
        ErrorQueue.objects.get_or_create(
            object_pk=user_id,
            error_type="SEND_EMAIL_ERROR",
            app_label='users',
            model_name='MflUser',
            except_message=(
                'Unable to send user email; The email '
                'and password given in settings are not correct')
        )
    return sent


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
                    "The password must be at least 8 characters and contain both letters and numbers"  # noqa
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
        send_email_on_signup(
            user.id, email, first_name, employee_number, password)
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


@reversion.register
@encoding.python_2_unicode_compatible
class JobTitle(models.Model):

    """
    This is the job title names of the officers in-charge of facilities.

    For example, Nursing Officer In-Charge, Medical Superintendent, and
    Hospital Director. This should not be confused with the professional
     (Nursing Officer I) or Job Group title.Officer
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100, unique=True,
        help_text="A short name for the job title")
    abbreviation = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="The short name for the title")
    description = models.TextField(
        null=True, blank=True,
        help_text="A short summary of the job title")
    search = models.TextField(
        null=True, blank=True,
        help_text='A dummy field to enable search on the model through a'
        ' filter')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ('-created', )
        permissions = (
            (
                "view_jobtitle",
                "Can view job title"
            ),
        )


@encoding.python_2_unicode_compatible
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
    job_title = models.ForeignKey(
        JobTitle, null=True, blank=True,
        help_text="The job title of the user e.g County Reproductive "
        "Health Officer",
        on_delete=models.PROTECT)
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
    created_by = models.ForeignKey(
        'self', null=True, blank=True, related_name='+',
        on_delete=models.PROTECT)
    updated_by = models.ForeignKey(
        'self', null=True, blank=True, related_name='+',
        on_delete=models.PROTECT)
    updated = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)

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

    def __str__(self):
        return self.get_full_name

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
    def user_groups(self):
        user_groups = self.groups.all()
        proxy_groups = ProxyGroup.objects.filter(
            id__in=[group.id for group in user_groups]
        )

        reg, admin, county, sub_county, national = (False,) * 5

        for proxy in proxy_groups:
            reg = True if proxy.is_regulator else reg
            admin = True if proxy.is_administrator else admin
            county = True if proxy.is_county_level else county
            sub_county = True if proxy.is_sub_county_level else sub_county
            national = True if proxy.is_national else national

        return {
            "is_regulator": reg,
            "is_administrator": admin,
            "is_county_level": county,
            "is_national": national,
            "is_sub_county_level": sub_county
        }

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
    def sub_county(self):
        from common.models import UserSubCounty
        user_subs = UserSubCounty.objects.filter(
            user=self, active=True)
        return user_subs[0].sub_county if user_subs else None

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

    @property
    def contacts(self):
        from common.models import UserContact
        return [
            {
                "id": user_contact.id,
                "contact": user_contact.contact.id,
                "contact_text": user_contact.contact.contact,
                "contact_type": user_contact.contact.contact_type.id,
                "contact_type_name": user_contact.contact.contact_type.name

            } for user_contact in UserContact.objects.filter(user=self)
        ]

    def save(self, *args, **kwargs):
        super(MflUser, self).save(*args, **kwargs)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', )
        ordering = ('-date_joined', )


@encoding.python_2_unicode_compatible
class MFLOAuthApplication(AbstractApplication):

    def __str__(self):
        return self.name or self.client_id

    class Meta(object):
        verbose_name = 'mfl oauth application'
        verbose_name_plural = 'mfl oauth applications'
        default_permissions = ('add', 'change', 'delete', 'view', )


@encoding.python_2_unicode_compatible
class CustomGroup(models.Model):
    group = models.OneToOneField(
        Group, on_delete=models.PROTECT, related_name='custom_group_fields')
    regulator = models.BooleanField(
        default=False, help_text="Are the regulators in this group?")
    national = models.BooleanField(
        default=False,
        help_text='Will the users in this group see all facilities in the '
        'country?')
    administrator = models.BooleanField(
        default=False,
        help_text='Will the users in this group administrator user rights?')
    county_level = models.BooleanField(
        default=False, help_text='Will the user be creating sub county users?')
    sub_county_level = models.BooleanField(
        default=False,
        help_text='Will the user be creating users below the sub county level '
        'users?')

    def __str__(self):
        return "{}".format(self.group)


@encoding.python_2_unicode_compatible
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
            return CustomGroup.objects.get(group=self).sub_county_level
        except CustomGroup.DoesNotExist:
            return False

    class Meta(object):
        proxy = True

    def __str__(self):
        return self.name


# model registration done here
reversion.register(MFLOAuthApplication, follow=['user'])
reversion.register(Permission)
reversion.register(Group, follow=['permissions'])
reversion.register(MflUser, follow=['groups', 'user_permissions'])
reversion.register(CustomGroup, follow=['group'])
