import logging
import reversion
import json

from django.db import models
from django.conf import settings

from rest_framework.exceptions import ValidationError

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
    description = models.TextField(
        null=True, blank=True,
        help_text='A brief description of the contact type.')

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

    class Meta(AbstractBase.Meta):
        unique_together = ('contact', 'contact_type')


class AdministrativeUnitBase(SequenceMixin, AbstractBase):
    """Base class for County, Constituency and Ward"""
    name = models.CharField(
        max_length=100,
        help_text="Name of the administrative unit e.g Nairobi")
    code = SequenceField(
        unique=True,
        help_text="A unique_code 4 digit number representing the region.")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        super(AdministrativeUnitBase, self).save(*args, **kwargs)

    class Meta(AbstractBase.Meta):
        abstract = True


def _lookup_facility_coordinates(area_boundary):
    """A helper used by the County, Constituency and Ward classes"""
    from mfl_gis.models import FacilityCoordinates
    facility_coordinates = FacilityCoordinates.objects.filter(
        coordinates__contained=area_boundary.mpoly
    ) if area_boundary and area_boundary.mpoly else []
    return {
        facility_coordinate.facility.name:
        json.loads(facility_coordinate.coordinates.geojson)
        for facility_coordinate in facility_coordinates
    }


@reversion.register
class County(AdministrativeUnitBase):
    """
    This is the largest administrative/political division in Kenya.

    Kenya is divided in 47 different counties.

    Code generation is handled by the custom save method in
    AdministrativeUnitBase
    """
    @property
    def facility_coordinates(self):
        """Look up the facilities that are in this unit's boundaries"""
        try:
            return _lookup_facility_coordinates(self.countyboundary)
        except:  # Handling RelatedObjectDoesNotExist is a little funky
            LOGGER.info('No boundaries found for {}'.format(self))
            return _lookup_facility_coordinates(None)

    @property
    def county_bound(self):
        from mfl_gis.models import CountyBoundary
        unit = CountyBoundary.objects.filter(area=self)
        return unit[0].bound if len(unit) else {}

    class Meta(AdministrativeUnitBase.Meta):
        verbose_name_plural = 'counties'


@reversion.register
class Constituency(AdministrativeUnitBase):
    """
    Counties in Kenya are divided into constituencies.

    A Constituency is a political sub division of a county.
    There are 290 constituencies in total.
    In most cases they coincide with sub counties.

    Code generation is handled by the custom save method in
    AdministrativeUnitBase
    """
    county = models.ForeignKey(
        County,
        help_text="Name of the county where the constituency is located",
        on_delete=models.PROTECT)

    @property
    def facility_coordinates(self):
        """Look up the facilities that are in this unit's boundaries"""
        try:
            return _lookup_facility_coordinates(self.constituencyboundary)
        except:  # Handling RelatedObjectDoesNotExist is a little funky
            LOGGER.info('No boundaries found for {}'.format(self))
            return _lookup_facility_coordinates(None)

    @property
    def constituency_bound(self):
        from mfl_gis.models import ConstituencyBoundary
        unit = ConstituencyBoundary.objects.filter(area=self)
        return unit[0].bound if len(unit) else {}

    class Meta(AdministrativeUnitBase.Meta):
        verbose_name_plural = 'constituencies'
        unique_together = ('name', 'county')


@reversion.register
class Ward(AdministrativeUnitBase):
    """
    The Kenyan counties are sub divided into wards.

    This is an administrative sub-division of the counties.
    A constituency can have one or more wards.
    In most cases the sub county is also the constituency.

    Code generation is handled by the custom save method in
    AdministrativeUnitBase
    """
    constituency = models.ForeignKey(
        Constituency,
        help_text="The constituency where the ward is located.",
        on_delete=models.PROTECT)

    @property
    def county(self):
        return self.constituency.county

    @property
    def facility_coordinates(self):
        """Look up the facilities that are in this unit's boundaries"""
        try:
            return _lookup_facility_coordinates(self.wardboundary)
        except:  # Handling RelatedObjectDoesNotExist is a little funky
            LOGGER.info('No boundaries found for {}'.format(self))
            return _lookup_facility_coordinates(None)


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
        counties = self.__class__.objects.filter(
            user=self.user, active=True, deleted=False)
        if counties.count() > 0 and not self.deleted:
            raise ValidationError(
                "A user can only be active in one county at a time")

    def save(self, *args, **kwargs):
        self.validate_only_one_county_active()
        super(UserCounty, self).save(*args, **kwargs)

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'user_counties'


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


@reversion.register
class UserConstituency(AbstractBase):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_constituencies')
    constituency = models.ForeignKey(Constituency)

    def validate_only_one_active_constituency(self):
        consts = self.__class__.objects.filter(
            user=self.user, active=True, deleted=False)
        if consts.count() > 0 and not self.deleted:
            raise ValidationError(
                "A user can be active in only one constituency at a time")

    def validate_constituency_county_in_creator_county(self):
        if self.constituency.county != self.created_by.county:
            error = "Users created must be in the administrators county"
            raise ValidationError(error)

    def clean(self, *args, **kwargs):
        self.validate_only_one_active_constituency()
        self.validate_constituency_county_in_creator_county()

    def __unicode__(self):
        custom_unicode = "{}: {}".format(self.user, self.constituency)
        return custom_unicode

    class Meta:
        verbose_name_plural = 'user constituencies'


class Town(AbstractBase):
    name = models.CharField(
        max_length=100, unique=True, null=True, blank=True,
        help_text="Name of the town")
    ward = models.ForeignKey(
        Ward, null=True, blank=True,
        help_text='The ward where the town is located')

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
        null=True, blank=True,
        max_length=100,
        help_text="The 5 digit number for the post office address. e.g 00900")
    address = models.TextField(
        null=True, blank=True,
        help_text="This is the actual post office number of the entity"
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

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'physical addresses'
