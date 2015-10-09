from django.db import models

from common.models import County, AbstractBase, Contact
from facilities.models import JobTitle


class AdminOfficeContact(Contact):
    admin_office = models.ForeignKey('AdminOffice', related_name='contacts')


class AdminOffice(AbstractBase):
    county = models.ForeignKey(County)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    job_title = models.ForeignKey(JobTitle)
