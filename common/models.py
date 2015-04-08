import logging
import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings

LOGGER = logging.getLogger(__file__)

# TODO ensure model update_by and udpated are not overwritten
# TODO check updated is greater then created
# TODO check deativate on delete


class AbstractBase(models.Model):
    """
    Provides auditing attributes to a model.

    It will provide audit fields that will keep track of when a model
    is created or updated and by who.
    """
    id = models.UUIDFIeld(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='+')
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='+')

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
        self.preserve_created_and_created_by()
        super(AbstractBase, self).save(*args, **kwargs)

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
    code = models.CharField(
        max_length=100, unique=True,
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
        " or phone number")

    def __unicode__(self):
        return str(self.id)


class PhysicalAddress(AbstractBase):
    """
    Details partaining the physical location of an entity.

    The entity could be a facility a person or a system.
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
    nearest_town = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="Provided in cases where the entity is not situated/residing"
        " in a town. e.g Kericho")
    plot_number = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="The plot number of the plot land the entity is "
        "situated/resides as it is in the title deed.")

    def __unicode__(self):
        return str(self.id)


class County(RegionAbstractBase):
    """
    This is the largest administrative/political division in Kenya.

    Kenya is divided in 47 different counties.
    """

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
        help_text="The county where the sub county is located.")

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
        help_text="Name of the county where the constituency is located")

    def __unicode__(self):
        return self.name
