from django.db import models
from django.contrib.gis.db import models as gis_models

from common.models import (
    County,
    AbstractBase,
    Contact,
    SubCounty,
    Constituency
)

from mfl_gis.models import CoordinatesValidatorMixin
from facilities.models import JobTitle


class AdminOfficeContact(Contact):
    """
    This is the admin office contacts.

    It will hold the both the official contacts for an office and
    the contacts of the in-charge.
    """
    admin_office = models.ForeignKey('AdminOffice', related_name='contacts')


class AdminOffice(CoordinatesValidatorMixin, AbstractBase):
    """
    The administration offices from the sub-county level to the national level.

    If the county and sub-county are null then the offices are
    assumed to be at the national level.
    """
    county = models.ForeignKey(County, null=True, blank=True)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True)
    constituency = models.ForeignKey(Constituency, null=True, blank=True)
    coordinates = gis_models.PointField(null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    job_title = models.ForeignKey(JobTitle)

    def clean(self):
        if self.county:
            self.validate_longitude_and_latitude_within_county(
                self.county)
        if self.constituency:
            self.validate_longitude_and_latitude_within_constituency(
                self.constituency)
