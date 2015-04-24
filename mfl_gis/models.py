import uuid
import reversion
import logging

from django.contrib.gis.db import models
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError

from common.models import get_default_system_user_id
from common.models import get_utc_localized_datetime

from facilities.models import Facility


LOGGER = logging.getLogger(__name__)


class GISAbstractBase(models.Model):
    """
    We've intentionally duplicated the `AbstractBase` in the `common` app
    because we wanted to confine the impact of GIS ( Geographic ) stuff
    to this app.

    The GIS stuff should have only one touch-point with the rest of the
    models: the link to the Facility model.

    We've kept the fields that are in the `common` `AbstractBase` because
    we want to have the same kind of base behavior.
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

    objects = models.GeoManager()
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
            super(GISAbstractBase, self).save(*args, **kwargs)

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


@reversion.register
class GeoCodeSource(GISAbstractBase):
    """
    Where the geo-code came from.

    This is the organization collecting the code.
    For example, DHMT, the Service Availability Mapping survey (SAM),
    Kenya Medical Research Institute (KEMRI), the Regional Center for
    Mapping of Resources for Development (RCMRD), the AIDS, Population
    and Health Integrated Assistance (APHIA) II, or another source.
    It is not the individual who collected the code
    """
    name = models.CharField(
        max_length=100,
        help_text="The name of the collecting organization")
    description = models.TextField(
        help_text="A short summary of the collecting organization",
        null=True, blank=True)
    abbreviation = models.CharField(
        max_length=10, help_text="An acronym of the collecting or e.g SAM")

    def __unicode__(self):
        return self.name


@reversion.register
class GeoCodeMethod(GISAbstractBase):
    """
    Method used to capture the geo-code.

    Examples:
        1= Taken with GPS device,
        2= Calculated from proximity to school, village, markets
        3= Calculated from 1:50,000 scale topographic maps,
        4= Scanned from hand-drawn maps,
        5= Centroid calculation from sub-location
        8= No geo-code
        9= Other
    """
    name = models.CharField(
        max_length=100, help_text="The name of the method.")
    description = models.TextField(
        help_text="A short description of the method",
        null=True, blank=True)

    def __unicode__(self):
        return self.name


@reversion.register
class FacilityCoordinates(GISAbstractBase):
    """
    Location derived by the use of GPS satellites and GPS device or receivers.

    It it three dimensional.
    The three-dimensional readings from a GPS device are latitude, longitude,
    and attitude. The date/time the reading is done is also important, as
    is the source and method of the reading.
    """
    facility = models.OneToOneField(Facility)
    latitude = models.CharField(
        max_length=255,
        help_text="How far north or south a facility is from the equator")
    longitude = models.CharField(
        max_length=255,
        help_text="How far east or west one a facility is from the Greenwich"
        " Meridian")
    source = models.ForeignKey(
        GeoCodeSource,
        help_text="where the geo code came from", on_delete=models.PROTECT)
    method = models.ForeignKey(
        GeoCodeMethod,
        help_text="Method used to obtain the geo codes. e.g"
        " taken with GPS device")
    collection_date = models.DateTimeField()

    def validate_longitude_and_latitude_within_kenya(self):
        pass

    def validate_longitude_and_latitude_within_constituency(self):
        pass

    def validate_longitude_and_latitude_within_county(self):
        pass

    def validate_longitude_and_latitude_within_ward(self):
        pass

    def clean(self):
        self.validate_longitude_and_latitude_within_kenya()
        self.validate_longitude_and_latitude_within_constituency()
        self.validate_longitude_and_latitude_within_county()
        self.validate_longitude_and_latitude_within_ward()
        super(FacilityCoordinates, self).clean()

    def __unicode__(self):
        return self.facility.name

    class Meta(GISAbstractBase.Meta):
        verbose_name_plural = 'facility coordinates'
        verbose_name = 'facility coordinates'
