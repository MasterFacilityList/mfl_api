from django.db import models
from django.utils import timezone
from django.conf import settings





class AbstractBase(models.Model):
    USER_MODEL = settings.AUTH_USER_MODEL
    created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(USER_MODEL, default=1)

    class Meta:
        abstract = True


class RegionAbstractBase(AbstractBase):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True


class Contact(AbstractBase):
    email = models.EmailField()
    town = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    nearest_town = models.CharField(max_length=100)
    landline = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    mobile =  models.CharField(max_length=100)
  
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
    district = models.ForeignKey(District)

    
    def __unicode__(self):
        return self.name


class Location(RegionAbstractBase):
    division =  models.ForeignKey(Division)

    def __unicode__(self):
        return self.name


class SubLocation(RegionAbstractBase):
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.name

    @property   
    def division(self):
        return self.location.division

    @property
    def district(self):
        return self.division.district
    
    @property
    def county():
        return self.district.county

    @property
    def province(self):
        return self.county.province


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
