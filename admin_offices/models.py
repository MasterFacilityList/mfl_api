from django.db import models
from django.contrib.gis.db import models as gis_models

from common.models import (
    County,
    AbstractBase,
    Contact,
    SubCounty,
    Constituency,
    SequenceMixin
)

from common.fields import SequenceField


class AdminOfficeContact(Contact):
    """
    This is the admin office contacts.
    It will hold the both the official contacts for an office and
    the contacts of the in-charge.
    """
    admin_office = models.ForeignKey(
        'AdminOffice', related_name='contacts', on_delete=models.PROTECT,)


class AdminOffice(SequenceMixin, AbstractBase):
    """
    The administration offices from the sub-county level to the national level.
    If the county and sub-county are null then the offices are
    assumed to be at the national level.
    """
    code = SequenceField(
        unique=True,
        help_text="A unique number to identify the admin office.",
        editable=False)
    old_code = models.IntegerField(null=True, blank=True)
    county = models.ForeignKey(
        County, null=True, blank=True, on_delete=models.PROTECT,)
    sub_county = models.ForeignKey(
        SubCounty, null=True, blank=True, on_delete=models.PROTECT,)
    constituency = models.ForeignKey(
        Constituency, null=True, blank=True, on_delete=models.PROTECT,)
    coordinates = gis_models.PointField(null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    is_national = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        super(AdminOffice, self).save(*args, **kwargs)

