import logging
import reversion

from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

from ..fields import SequenceField
from .base import AbstractBase, SequenceMixin

LOGGER = logging.getLogger(__file__)


@reversion.register
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


@reversion.register
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


class Town(AbstractBase):
    name = models.CharField(
        max_length=100, unique=True,
        help_text="Name of the town")

    def __unicode__(self):
        return self.name


@reversion.register
class PhysicalAddress(AbstractBase):
    """
    The physical properties of a facility.

    These are physical properties of the facility and included is the
    plot number and nearest landmark. This information in conjunction with
    GPS codes is useful in locating the facility.
    """
    town = models.ForeignKey(
        Town, null=True, blank=True,
        help_text="The town where the entity is located e.g Nakuru")
    postal_code = models.CharField(
        max_length=100,
        help_text="The 5 digit number for the post office address. e.g 00900")
    address = models.TextField(
        help_text="This is the actual post office number of the entity. "
        "e.g 6790")
    nearest_landmark = models.TextField(
        null=True, blank=True,
        help_text="well-known physical features /structure that can be used to"
        " simplify directions to a given place. e.g town market or village ")
    plot_number = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="This is the same number found on the title deeds of the"
        "piece of land on which this facility is located")

    def __unicode__(self):
        return "{}: {}".format(self.postal_code, self.address)

    class Meta:
        verbose_name_plural = 'physical addresses'


@reversion.register
class RegionAbstractBase(AbstractBase, SequenceMixin):
    """
    Model to supply the common attributes of a region.

    A  region is an Administrative/political hierarchy and includes the
    following levels:
        1. County,
        2. Constituency,
        3. Sub-county,
        4. ward
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text="Name og the region may it be e.g Nairobi")
    code = SequenceField(
        unique=True,
        help_text="A unique_code 4 digit number representing the region.")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        super(RegionAbstractBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True


@reversion.register
class County(RegionAbstractBase):
    """
    This is the largest administrative/political division in Kenya.

    Kenya is divided in 47 different counties.

    Code generation is handled by the custom save method in RegionAbstractBase
    """
    pass  # Everything, including __unicode__ is handled by the abstract model

    class Meta:
        verbose_name_plural = 'counties'


@reversion.register
class Constituency(RegionAbstractBase):
    """
    Counties in Kenya are divided into constituencies.

    A Constituency is a political sub division of a county.
    There are 290 constituencies in total.
    In most cases they coincide with sub counties.

    Code generation is handled by the custom save method in RegionAbstractBase
    """
    county = models.ForeignKey(
        County,
        help_text="Name of the county where the constituency is located",
        on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'constituencies'


@reversion.register
class Ward(RegionAbstractBase):
    """
    The Kenyan counties are sub divided into wards.

    This is an administrative sub-division of the counties.
    A constituency can have one or more wards.
    In most cases the sub county is also the constituency.

    Code generation is handled by the custom save method in RegionAbstractBase
    """
    constituency = models.ForeignKey(
        Constituency,
        help_text="The constituency where the ward is located.",
        on_delete=models.PROTECT)

    @property
    def county(self):
        return self.constituency.county


@reversion.register
class UserCounty(AbstractBase):
    """
    Will store a record of the counties that a user has been incharge of.

    A user can only be incharge of only one county at a time.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_counties',
        on_delete=models.PROTECT)
    county = models.ForeignKey(County, on_delete=models.PROTECT)

    def __unicode__(self):
        return "{}: {}".format(self.user.email, self.county.name)

    def validate_only_one_county_active(self):
        """
        A user can be incharge of only one county at the a time.
        """
        counties = self.__class__.objects.filter(user=self.user, active=True)
        if counties.count() > 0:
            raise ValidationError(
                "A user can only be active in one county at a time")

    def save(self, *args, **kwargs):
        self.validate_only_one_county_active()
        super(UserCounty, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'user_counties'


@reversion.register
class UserResidence(AbstractBase):
    """
    Stores the wards in which the user resides in.
    If a user moves to another ward the current ward is deactivated by setting
    active to False
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_residence')
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.user.email + ": " + self.ward.name

    def validate_user_residing_in_one_place_at_a_time(self):
        user_wards = self.__class__.objects.filter(user=self.user, active=True)
        if user_wards.count() > 0:
            raise ValidationError(
                "User can only reside in one ward at a a time")

    def save(self, *args, **kwargs):
        self.validate_user_residing_in_one_place_at_a_time()
        super(UserResidence, self).save(*args, **kwargs)


@reversion.register
class UserContact(AbstractBase):
    """
    Stores a user's contacts.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_contacts', on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return "{}: {}".format(self.user.get_full_name, self.contact.contact)
