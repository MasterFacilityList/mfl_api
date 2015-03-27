from django.db import models
from django.utils import timezone
from django.conf import settings
from djano.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class AbstractBase(models.Model):
    created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abtract = True


class RegionAbstractBase(AbstractBase):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)

    class Meta:
        abtract = True


class Contact(AbstractBase):
    email = models.EmailField()
    town = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    nearest_town = models.CharField(max_length=100)
    landline = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    mobile =  mobile.CharField(max_length=100)
  
    def __unicode__(self):
        return self.email
        

class Province(RegionAbstractBase):    

    def __unicode__(self):
        return  self.name


class County(RegionAbstractBase):
    Province = models.ForeignKey(Province)

    def __unicode__(self):
        return self.name

    class Meta:
        pass


class Constituency(RegionAbstractBase):
    county  = models.ForeignKey(County)
    
    def __unicode__(self):
        return self.name


class District(RegionAbstractBase):
    county = models.ForeignKey(County)

    def __unicode__(self):
        return self.name


class Division(RegionAbstractBase):
    district = models.ForeignKey(District):

    
    def __unicode__(self):
        return self.name


class Location(RegionAbstractBase):
    division =  models.ForeignKey(Division)

    def __unicode__(self):
        return self.name


class Sublocation(RegionAbstractBase):
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    email = models.EmailField()
    subjet = models.CharField(max_length=255)
    comment = models.TextField()

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = 'Feedback from users'
        verbose_name_plural = 'Feedback from users'
