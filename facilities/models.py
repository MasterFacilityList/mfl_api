from django.db import models
from common.models import AbstractBase, SubLocation

FACILLITY_STATUS = (
    ('OPERATIONAL', 'Operations are running normally'),
    ('NOT_OPERATIONAL', 'The facility is not operating'),
)

FACILITY_TYPES = (
    ('DISPENSARY', 'dispensary'),
    ('HEALTH_CENTER', 'Health Center'),
    ('LEVEL_1', 'Level 1 facility'),
    ('LEVEL_2', 'Level 2 facility'),
    ('LEVEL_3', 'Level 3 facility'),
    ('LEVEL_4', 'Level 4 facility'),
    ('LEVEL_5', 'Level 5 facility'),
)


class Owner(AbstractBase):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=100)


class Service(AbstractBase):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Facility(AbstractBase):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    is_classified = models.BooleanField(default=False)
    description = models.TextField()
    facility_type = models.CharField(
        max_length=100, choices=FACILITY_TYPES)
    services = models.ManyToManyField(Service)
    number_of_beds = models.PositiveIntegerField(default=0)
    number_of_cots = models.PositiveIntegerField(default=0)
    open_whole_day = models.BooleanField(default=False)
    open_whole_week = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50, choices=FACILLITY_STATUS)
    sub_location = models.ForeignKey(SubLocation)
    owner = models.ForeignKey(Owner)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Facilities'


class CommunityUnits(models.Model):
    pass
