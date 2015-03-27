from django.db import models

FACILLITY_STATUS = (
    ('OPERATIONAL', ''),
    ('OPERATIONAL', ''),
)

class Owners(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100)


class FacilityTypes(models.Model):
    pass


class Service(models.Model):
    name = models.CharField(max_length=255)
    description =  models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    is_classified = models.BooleanField(default=False)
    services = models.ManyToMany(Service)a

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Facilities'
 

class CommunityUnits(models.Model):
    pass