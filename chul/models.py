from django.db import models
from common.models import AbstractBase, Contact
from facilities.models import Facility


class CommunityHealthUnit(AbstractBase):
    """
    This is a health service delivery structure within a defined geographical
    area covering a population of approximately 5,000 people.

    Each unit is assigned 2 Community Health Extension Workers (CHEWs) and
    community health volunteers who offer promotive, preventative and basic
    curative health services
    """
    name = models.CharField(
        max_length=100,
        help_text="")
    facility = models.ForeignKey(
        Facility,
        help_text='The facility on which the health unit is tied to.')

    def __unicode__(self):
        return self.name


class CommunityHealthWorker(AbstractBase):
    """
    A person who is incharge of a certain community health area.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    id_number = models.PositiveIntegerField(unique=True)

    def __unicode__(self):
        return str(self.id_number)


class CommunityHealthWorkerContact(AbstractBase):
    """
    The contacts of the healh worker.

    They may be as many as the health worker has.
    """
    health_worker = models.ForeignKey(CommunityHealthWorker)
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return "{}: {}".format(self.health_worker, self.contact)
