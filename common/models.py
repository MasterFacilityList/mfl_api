import logging

from django.db import models
from django.utils import timezone
from django.conf import settings

LOGGER = logging.getLogger(__file__)

CONTACT_TYPES = (
    ('EMAIL', 'email'),
    ('LANDLINE', 'landline'),
    ('MOBILE', 'Mobile Phone number'),

)


class AbstractBase(models.Model):
    """
    Provides auditing attributes to a model.
    It will provide audit fields that will keep track of when a model
    is created or updated and by who.
    """

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
    Model to hold the common attributes of a region
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True


class Contact(AbstractBase):
    """
    Holds contacts such as email and phone number.
    """
    contact = models.CharField(max_length=100)
    contact_type = models.CharField(choices=CONTACT_TYPES, max_length=100)

    def __unicode__(self):
        return str(self.id)


class PhysicalAddress(AbstractBase):
    """
    Details partaining the physical location of a facility
    """
    town = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    nearest_town = models.CharField(max_length=100)
    plot_number = models.CharField(max_length=100)

    def __unicode__(self):
        return str(self.id)


class County(RegionAbstractBase):
    def __unicode__(self):
        return self.name


class SubCounty(RegionAbstractBase):
    county = models.ForeignKey(County)

    def __unicode__(self):
        return self.name


class Constituency(RegionAbstractBase):
    county = models.ForeignKey(County)

    def __unicode__(self):
        return self.name
