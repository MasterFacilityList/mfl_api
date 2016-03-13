import logging
import reversion
import json

from django.db import models
from django.conf import settings
from django.utils import encoding, timezone

from rest_framework.exceptions import ValidationError

from ..fields import SequenceField
from .base import AbstractBase, SequenceMixin

LOGGER = logging.getLogger(__file__)

ERROR_TYPES = (
    (
        'SEARCH_INDEXING_ERROR',
        'An error that occurred during search indexing'
    ),
    (
        'SEND_EMAIL_ERROR',
        'An error that occurs when sending a user email'
    )
)


class UserAdminAreaLinkageMixin(object):

    def should_update_user_area(self, *args, **kwargs):
        """
        Ensure that a user is assigned to a certain admin area once.

        If one wants to remove the user from the area, then
        they should use deactivate the record and to link back the user to the
        admin area they should activate the record
        """
        try:
            if kwargs.pop('field_name', None) == 'constituency':
                old_obj = self.__class__.objects.get(
                    user=self.user, constituency=self.constituency)
            else:
                old_obj = self.__class__.objects.get(
                    user=self.user, county=self.county)

            active_list = [old_obj.active, self.active]
            return active_list.count(True) == 1
        except self.__class__.DoesNotExist:
            # the record is being created for the first time
            return True


@reversion.register
@encoding.python_2_unicode_compatible
class ContactType(AbstractBase):

    """
    Captures the different types of contacts that we have in the real world.

    The most common contacts are email, phone numbers, land-line etc.
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text="A short name, preferably 6 characters long, "
        "representing a certain type of contact e.g EMAIL")
    description = models.TextField(
        null=True, blank=True,
        help_text='A brief description of the contact type.')

    def __str__(self):
        return self.name


@reversion.register(follow=['contact_type'])
@encoding.python_2_unicode_compatible
class Contact(AbstractBase):

    """
    Holds ways in which entities can communicate.

    The communication ways are not limited provided that all parties
    willing to communicate will be able to do so. The communication
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

    def __str__(self):
        return "{}: {}".format(self.contact_type.name, self.contact)

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
    return [
        {
            "name": facility_coordinate.facility.name,
            "geometry": json.loads(facility_coordinate.coordinates.geojson)
        }
        for facility_coordinate in facility_coordinates
    ]


@reversion.register
@encoding.python_2_unicode_compatible
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

    def __str__(self):
        return self.name

    class Meta(AdministrativeUnitBase.Meta):
        verbose_name_plural = 'counties'


@reversion.register(follow=['county'])
@encoding.python_2_unicode_compatible
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

    def __str__(self):
        return self.name

    @property
    def constituency_bound(self):
        from mfl_gis.models import ConstituencyBoundary
        unit = ConstituencyBoundary.objects.filter(area=self)
        return unit[0].bound if len(unit) else {}

    class Meta(AdministrativeUnitBase.Meta):
        verbose_name_plural = 'constituencies'
        unique_together = ('name', 'county')


@reversion.register(follow=['county'])
@encoding.python_2_unicode_compatible
class SubCounty(AdministrativeUnitBase):

    """
    A county can be sub divided into sub counties.

    The sub-counties do not necessarily map to constituencies
    """
    county = models.ForeignKey(County, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


@reversion.register(follow=['constituency'])
@encoding.python_2_unicode_compatible
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
    sub_county = models.ForeignKey(
        SubCounty, null=True, blank=True,
        help_text='The sub-county where the ward is located',
        on_delete=models.PROTECT)

    def __str__(self):
        return self.name

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

    def validate_county(self):
        if self.sub_county:
            if not self.sub_county.county == self.constituency.county:
                raise ValidationError(
                    {
                        "sub_county": [
                            "Ensure the sub-county and the constituency "
                            "are in the same county"
                        ]
                    }
                )

    def clean(self, *args, **kwargs):
        super(Ward, self).clean(*args, **kwargs)
        self.validate_county()


@reversion.register(follow=['user', 'county'])
@encoding.python_2_unicode_compatible
class UserCounty(UserAdminAreaLinkageMixin, AbstractBase):

    """
    Will store a record of the counties that a user has been in-charge of.

    A user can only be in-charge of only one county at a time.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_counties',
        on_delete=models.PROTECT)
    county = models.ForeignKey(County, on_delete=models.PROTECT)

    def __str__(self):
        return "{}: {}".format(self.user, self.county)

    def clean(self, *args, **kwargs):
        super(UserCounty, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean(exclude=None)
        super(UserCounty, self).save(*args, **kwargs) if \
            self.should_update_user_area(field_name='county') else None

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'user_counties'


@reversion.register(follow=['user', 'contact'])
@encoding.python_2_unicode_compatible
class UserContact(AbstractBase):

    """
    Stores a user's contacts.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_contacts', on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact)

    def __str__(self):
        return "{}: ({})".format(self.user, self.contact)

    def validate_user_linked_to_a_certain_contact_once(self):
        """
        Ensures that user contacts are not duplicated
        """
        user_contact_instance_count = self.__class__.objects.filter(
            user=self.user, contact=self.contact).count()
        if user_contact_instance_count > 0 and not self.deleted:
            msg = "The user contact {0} is already added to the user".format(
                self.contact.contact)
            raise ValidationError(
                {
                    "contact": [msg]

                })

    def clean(self, *args, **kwargs):
        super(UserContact, self).clean(*args, **kwargs)
        self.validate_user_linked_to_a_certain_contact_once()


@reversion.register(follow=['user', 'constituency'])
@encoding.python_2_unicode_compatible
class UserConstituency(UserAdminAreaLinkageMixin, AbstractBase):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_constituencies')
    constituency = models.ForeignKey(Constituency)

    def validate_constituency_county_in_creator_county(self):
        error = {
            "constituency": [
                "Users created must be in the administrators "
                "county or sub county"
            ]
        }
        nat_user = self.created_by.is_national or self.updated_by.is_national
        if self.created_by.constituency:
            if self.constituency.county != self.created_by.constituency.county:
                raise ValidationError(error)
        elif (self.constituency.county != self.created_by.county and not
                nat_user):
            raise ValidationError(error)

    def clean(self, *args, **kwargs):
        self.validate_constituency_county_in_creator_county()

    def __str__(self):
        return "{}: {}".format(self.user, self.constituency)

    def save(self, *args, **kwargs):
        self.full_clean(exclude=None)
        super(UserConstituency, self).save(*args, **kwargs) if \
            self.should_update_user_area(field_name='constituency') else None

    class Meta(object):
        verbose_name_plural = 'user constituencies'


@reversion.register
@encoding.python_2_unicode_compatible
class Town(AbstractBase):
    name = models.CharField(
        max_length=255, unique=True, null=True, blank=True,
        help_text="Name of the town")

    def __str__(self):
        return self.name


@reversion.register(follow=['town', ])
@encoding.python_2_unicode_compatible
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
    nearest_landmark = models.TextField(
        null=True, blank=True,
        help_text="well-known physical features /structure that can be used to"
        " simplify directions to a given place. e.g town market or village ")
    plot_number = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="This is the same number found on the title deeds of the"
        "piece of land on which this facility is located")
    location_desc = models.TextField(
        null=True, blank=True,
        help_text="This field allows a more detailed description of "
        "the location")

    def __str__(self):
        return self.location_desc

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'physical addresses'


@reversion.register
@encoding.python_2_unicode_compatible
class DocumentUpload(AbstractBase):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    fyl = models.FileField()

    def __str__(self):
        return self.name


@reversion.register
@encoding.python_2_unicode_compatible
class ErrorQueue(models.Model):
    """
    A model to store errors that occur when processing data
    """
    object_pk = models.CharField(max_length=100, null=True, blank=True)
    app_label = models.CharField(max_length=100, null=True, blank=True)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    resolved = models.BooleanField(default=False)
    retries = models.IntegerField(default=0)
    except_message = models.TextField(null=True, blank=True)
    error_type = models.CharField(choices=ERROR_TYPES, max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta(object):
        unique_together = ('object_pk', 'app_label', 'model_name')
        ordering = ('-created', )

    def __str__(self):
        return "{} - {} - {}".format(
            self.object_pk, self.app_label, self.model_name)


class UserSubCounty(AbstractBase):
    """
    Link a user to a sub-county
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_sub_counties')
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT)

    def __str__(self):
        return "{0} - {1}".format(
            self.user.email, self.sub_county.name)
