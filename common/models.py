from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class AbstractBase(models.Model):
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class RegionAbstractBase(AbstractBase):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True


class Contact(AbstractBase):
    email = models.EmailField(null=True, blank=True)
    town = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    nearest_town = models.CharField(max_length=100)
    landline = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)

    def __unicode__(self):
        if self.email:
            return self.email
        else:
            return str(self.id)

    def validate_mobile(self):
        """
        Ensures that a mobile phone number takes the Kenyan format
        07xxabcdef
        """
        if len(self.mobile) > 10 or len(self.mobile) < 10:
            error = "The mobile number format is wrong. Use 07XXABCDEF"
            raise ValidationError(error)

    def clean(self, *args, **kwargs):
        self.validate_mobile()

    def save(self, *args, **kwargs):
        self.full_clean(exclude=None)
        super(Contact, self).save(*args, **kwargs)


class Province(RegionAbstractBase):

    def __unicode__(self):
        return self.name


class County(RegionAbstractBase):
    Province = models.ForeignKey(Province, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        pass


class Constituency(RegionAbstractBase):
    county = models.ForeignKey(County)

    def __unicode__(self):
        return self.name


class District(RegionAbstractBase):
    province = models.ForeignKey(Province, null=True, blank=True)
    county = models.ForeignKey(County)

    def __unicode__(self):
        return self.name


class Division(RegionAbstractBase):
    district = models.ForeignKey(District)
    constituency = models.ForeignKey(Constituency, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Location(RegionAbstractBase):
    division = models.ForeignKey(Division)

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
    def county(self):
        return self.district.county

    @property
    def province(self):
        return self.district.province

    @property
    def constituency(self):
        return self.division.constituency


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
