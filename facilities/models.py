import random
from django.db import models
from common.models import AbstractBase, SubCounty, Contact


class Owner(AbstractBase):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    def generate_code(self):
        return "{}{}".format("OWNER", str(self.id))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super(Owner, self).save(*args, **kwargs)


class Service(AbstractBase):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    def generate_code(self):
        return "{}{}".format(self.name, str(self.id))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super(Service, self).save(*args, **kwargs)


class FacilityStatus(AbstractBase):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class FacilityType(AbstractBase):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Facility(AbstractBase):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    facility_type = models.OneToOneField(FacilityType)
    number_of_beds = models.PositiveIntegerField(default=0)
    number_of_cots = models.PositiveIntegerField(default=0)
    open_whole_day = models.BooleanField(default=False)
    open_whole_week = models.BooleanField(default=False)
    status = models.OneToOneField(FacilityStatus)
    sub_county = models.ForeignKey(SubCounty)
    owner = models.ForeignKey(Owner)

    def generate_code(self):
        random_number = random.randint(10000, 1000000)
        try:
            self.__class__.objects.get(code=random_number)
            self.generate_code()
        except:
            return random_number

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Facilities'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super(Service, self).save(*args, **kwargs)


class FacitlityGIS(AbstractBase):
    facility = models.OneToOneField(Facility)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    is_classified = models.BooleanField(default=False)

    def __unicode___(self):
        return self.facility.name


class FacilityService(AbstractBase):
    facility = models.ForeignKey(Facility, related_name='facility_services')
    service = models.ForeignKey(Service)

    def __unicode__(self):
        return "{}::{}".format(self.facility.name, self.service.name)


class FacilityContact(AbstractBase):
    facility = models.ForeignKey(Facility)
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return "{}::{}::{}".format(
            self.facility.name, self.contact.contact_type,
            str(self.contact.id))
