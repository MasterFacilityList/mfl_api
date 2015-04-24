import logging
import uuid
import pytz
import reversion

from django.db import models
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings

from ..utilities.sequence_helper import SequenceGenerator

LOGGER = logging.getLogger(__file__)


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

        # In order for auditability to work, all descendants of AbstractBase
        # must @reversion.register
        with transaction.atomic(), reversion.create_revision():
            super(AbstractBase, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Mark the field model deleted
        self.deleted = True
        self.save()

    def __unicode__(self):
        """Default if child models do not define their string representation"""
        return '{} {}'.format(self._meta.verbose_name, self.pk)

    class Meta(object):
        ordering = ('-updated', '-created',)
        abstract = True


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
