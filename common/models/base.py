import logging
import uuid
import pytz

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.deletion import Collector, ProtectedError


from rest_framework.exceptions import ValidationError

from ..utilities.sequence_helper import SequenceGenerator

LOGGER = logging.getLogger(__file__)

from rest_framework import generics



def delete_child_instances(instance):
    try:
        collector = Collector(using='default')
        collector.collect(objs=[instance], collect_related=True)
    except ProtectedError as error:
        raise
        # raise ValidationError({

        #        "Error": ["cannot deleted the record since there are"
        #        " other records that depend on it"]

        #     })


def get_default_system_user_id():
    """
    Ensure that there is a default system user, unknown password
    """
    try:
        return get_user_model().objects.get(
            email='system@ehealth.or.ke',
            first_name='System',
            username='system'
        ).pk
    except get_user_model().DoesNotExist:
        return get_user_model().objects.create(
            email='system@ehealth.or.ke',
            first_name='System',
            username='system'
        ).pk


def get_utc_localized_datetime(datetime_instance):
    """
    Converts a naive datetime to a UTC localized datetime.

    :datetime_instance datetime A naive datetime instance.
    """
    current_timezone = pytz.timezone(settings.TIME_ZONE)
    localized_datetime = current_timezone.localize(datetime_instance)
    return localized_datetime.astimezone(pytz.utc)


class CustomDefaultManager(models.Manager):

    def get_queryset(self):
        return super(
            CustomDefaultManager, self).get_queryset().filter(deleted=False)


class AbstractBase(models.Model):

    """
    Provides auditing attributes to a model.

    It will provide audit fields that will keep track of when a model
    is created or updated and by who.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=get_default_system_user_id,
        on_delete=models.PROTECT, related_name='+')
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=get_default_system_user_id,
        on_delete=models.PROTECT, related_name='+')
    deleted = models.BooleanField(default=False)
    active = models.BooleanField(
        default=True,
        help_text="Indicates whether the record has been retired?")

    # place holder to enable implementation of a search filter.
    # Will be replaced in future
    search = models.CharField(
        max_length=255, null=True, blank=True, editable=False)

    objects = CustomDefaultManager()
    everything = models.Manager()

    def validate_updated_date_greater_than_created(self):
        if timezone.is_naive(self.updated):
            self.updated = get_utc_localized_datetime(self.updated)

        if self.updated < self.created:
            raise ValidationError(
                'The updated date cannot be less than the created date')

    def preserve_created_and_created_by(self):
        """
        Ensures that in subsequent times created and created_by fields
        values are not overriden.
        """
        try:
            original = self.__class__.objects.get(pk=self.pk)
            self.created = original.created
            self.created_by = original.created_by
        except self.__class__.DoesNotExist:
            LOGGER.info(
                'preserve_created_and_created_by '
                'Could not find an instance of {} with pk {} hence treating '
                'this as a new record.'.format(self.__class__, self.pk))

    def save(self, *args, **kwargs):
        self.full_clean(exclude=None)
        self.preserve_created_and_created_by()
        self.validate_updated_date_greater_than_created()
        super(AbstractBase, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Mark the field model deleted
        delete_child_instances(self)

        self.deleted = True
        self.save()

    def __str__(self):
        raise NotImplementedError(
            "child models need to define their representation"
        )

    def __unicode__(self):
        return self.__str__()

    class Meta(object):
        ordering = ('-updated', '-created',)
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view', )


class AbstractBaseMapping(models.Model):

    id = models.AutoField(primary_key=True)
    mfl_name = models.CharField(max_length=255, null=True, blank=True)
    mfl_code = models.IntegerField(default=0, null=True, blank=True)
    dhis_name = models.CharField(max_length=255, null=True, blank=True)
    dhis_id = models.CharField(max_length=255, null=True, blank=True)
    dhis_parent_id = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def get_dhis_id(self):
        return self.dhis_id

    @property
    def get_dhis_name(self):
        return self.dhis_name

    @property
    def get_mfl_name(self):
        return self.mfl_name

    @property
    def get_mfl_code(self):
        return self.mfl_code

    def validate_updated_date_greater_than_created(self):
        if timezone.is_naive(self.updated):
            self.updated = get_utc_localized_datetime(self.updated)

        if self.updated < self.created:
            raise ValidationError(
                'The updated date cannot be less than the created date')

    def preserve_created(self):
        """
        Ensures that in subsequent times created and created_by fields
        values are not overriden.
        """
        try:
            original = self.__class__.objects.get(pk=self.pk)
            self.created = original.created
        except self.__class__.DoesNotExist:
            LOGGER.info(
                'preserve_created '
                'Could not find an instance of {} with pk {} hence treating '
                'this as a new record.'.format(self.__class__, self.pk))

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        self.full_clean(exclude=None)
        self.preserve_created()
        self.validate_updated_date_greater_than_created()
        super(AbstractBaseMapping, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Mark the field model deleted
        delete_child_instances(self)

        self.deleted = True
        self.save()

    def __str__(self):
        raise NotImplementedError(
            "child models need to define their representation"
        )

    def __unicode__(self):
        return self.__str__()

    class Meta(object):
        ordering = ('-updated', '-created',)
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view', )


class SequenceMixin(object):

    """
    Intended to be mixed into models with a `code` `SequenceField`
    """

    def generate_next_code_sequence(self):
        """
        Relies upon the predictability of Django sequence naming
        ( convention )
        """
        return SequenceGenerator(
            app_label=self._meta.app_label,
            model_name=self._meta.model_name
        ).next()


class ApiAuthentication(models.Model):
    username = models.CharField(max_length=255, default="healthit", null=False, blank=False)
    password = models.CharField(max_length=255, default="hEALTHIT2017", null=False, blank=False)
    client_id = models.CharField(max_length=255, default="101", null=False, blank=False)
    client_secret = models.CharField(max_length=255, default="873079d99-95b4-46f5-8369-9f23a3dd877", null=False,
                                     blank=False)
    server = models.CharField(max_length=255, default="https://test.hiskenya.org/dev/", null=False, blank=False)
    session_key = models.CharField(max_length=255, default="dhis2_api_12904rs", null=False, blank=False)

    @property
    def get_api_username(self):
        "Returns the API username."
        return '%s' % self.username

    @property
    def get_api_password(self):
        "Returns the API password."
        return '%s' % self.password

    @property
    def get_api_client_id(self):
        "Returns the API client_id."
        return '%s' % self.client_id

    @property
    def get_api_client_secret(self):
        "Returns the API client_secret."
        return '%s' % self.client_secret

    @property
    def get_api_server(self):
        "Returns the API server."
        return '%s' % self.server

    @property
    def get_api_session_key(self):
        "Returns the API session_key."
        return '%s' % self.session_key