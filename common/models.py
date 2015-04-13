import logging
import uuid
import pytz

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings

from .sequence_helper import next_value_in_sequence

LOGGER = logging.getLogger(__file__)


def get_utc_localized_datetime(datetime_instance):
    """
    Converts a naive datetime to a UTC localized datetime.

    :datetime_instance datetime A naive datetime instance.
    """
    current_timezone = pytz.timezone(settings.TIME_ZONE)
    localized_datetime = current_timezone.localize(datetime_instance)
    return localized_datetime.astimezone(pytz.utc)


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
        self.deleted = True
        self.save()

    class Meta:
        abstract = True


class RegionAbstractBase(AbstractBase):
    """
    Model to supply the common attributes of a region.

    A  region is an Administrative/political hierarchy and includes the
    following levels:
        1. county,
        2. Constituency,
        3. sub-county,
        4. ward
    """

    name = models.CharField(
        max_length=100, unique=True,
        help_text="Name og the region may it be e.g Nairobi")
    code = models.IntegerField(
        unique=True,
        help_text="A unique_code 4 digit number representing the region.")

    class Meta:
        abstract = True


class ContactType(AbstractBase):
    """
    Captures the different types of contacts that we have in the real world.

    The most common contacts are email, phone numbers, landline etc.
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text="A short name, preferrably 6 characters long, representing a"
        "certain type of contact e.g EMAIL")
    description = models.TextField(help_text='A brief desx')

    def __unicode__(self):
        return self.name


class Contact(AbstractBase):
    """
    Holds ways in which entities can communicate.

    The commincation ways are not limited provided that all parties
    willing to communicate will be able to do so. The commucation
    ways may include emails, phone numbers, landlines etc.
    """

    contact = models.CharField(
        max_length=100,
        help_text="The actual contact of the person e.g test@mail.com,"
        " 07XXYYYZZZ")
    contact_type = models.ForeignKey(
        ContactType,
        help_text="The type of contact that the given contact is e.g email"
        " or phone number",
        on_delete=models.PROTECT)

    def __unicode__(self):
        return "{}::{}".format(self.contact_type.name, self.contact)


class PhysicalAddress(AbstractBase):
    """
    The physical properties of a facility.

    These are physical properties of the facility and included is the
    plot number and nearest landmark. This information in conjunction with
    GPS codes is useful in locating the facility.
    """

    town = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="The town where the entity is located e.g Nakuru")
    postal_code = models.CharField(
        max_length=100,
        help_text="The 5 digit number for the post office address. e.g 00900")
    address = models.CharField(
        max_length=100,
        help_text="This is the actual post office number of the entity. "
        "e.g 6790")
    nearest_landmark = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="well-known physical features /structure that can be used to"
        " simplify directions to a given place. e.g town market or village ")
    plot_number = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="This is the same number found on the title deeds of the"
        "piece of land on which this facility is located")

    def __unicode__(self):
        return "{}: {}".format(self.postal_code, self.address)


class County(RegionAbstractBase):
    """
    This is the largest administrative/political division in Kenya.

    Kenya is divided in 47 different counties.
    """

    def get_code_value(self):
        value = next_value_in_sequence("county_code_seq")
        return value

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code_value()
        super(County, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class SubCounty(RegionAbstractBase):
    """
    The Kenyan counties are sub divided into sub counties.

    This is administrative sub-division of the counties.
    A county can have one or more sub counties.
    In most cases the sub county is also the constituency.
    """

    county = models.ForeignKey(
        County,
        help_text="The county where the sub county is located.",
        on_delete=models.PROTECT)

    def get_code_value(self):
        value = next_value_in_sequence("ward_code_seq")
        return value

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code_value()
        super(SubCounty, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Constituency(RegionAbstractBase):
    """
    Counties in Kenya are divided into constituencies.

    A Constituency is a political sub division of a county.
    There are 290 constituencies in total.
    In most cases they coincide with sub counties.
    """

    county = models.ForeignKey(
        County,
        help_text="Name of the county where the constituency is located",
        on_delete=models.PROTECT)

    def get_code_value(self):
        value = next_value_in_sequence("consituency_code_seq")
        return value

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code_value()
        super(Constituency, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class UserCounties(AbstractBase):
    """
    Will store a record of the counties that a user has been incharge of.

    A user can only be incharge of only one county at a time.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_counties',
        on_delete=models.PROTECT)
    county = models.ForeignKey(County, on_delete=models.PROTECT)
    is_active = models.BooleanField(
        default=True,
        help_text="Is the user currently incharge of the county?")

    def __unicode__(self):
        return "{}: {}".format(self.user.email, self.county.name)

    def validate_only_one_county_active(self):
        """
        A user can be incharge of only one county at the a time.
        """
        counties = self.__class__.objects.filter(
            user=self.user, is_active=True)
        if counties.count() > 0:
            raise ValidationError(
                "A user can only be active in one county at a time")

    def save(self, *args, **kwargs):
        self.validate_only_one_county_active()
        super(UserCounties, self).save(*args, **kwargs)
