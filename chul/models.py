from django.db import models
from common.models import AbstractBase, Contact, SequenceMixin, Ward
from common.fields import SequenceField
from facilities.models import Facility


class Status(AbstractBase):
    """
    Indicates the of operation of a community health unit.
    e.g  fully functiona, semi operational, operational
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Community(SequenceMixin, AbstractBase):
    """
    A certain area within a ward.
    """
    name = models.CharField(max_length=100)
    code = SequenceField(unique=True)
    ward = models.ForeignKey(Ward)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        super(Community, self).save(*args, **kwargs)


class CommunityHealthUnit(SequenceMixin, AbstractBase):
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
    code = SequenceField(unique=True)
    facility = models.ForeignKey(
        Facility,
        help_text='The facility on which the health unit is tied to.')
    status = models.ForeignKey(Status)
    community = models.ForeignKey(
        Community,
        help_text='Community area within which the health unit is located')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        super(CommunityHealthUnit, self).save(*args, **kwargs)


class CommunityHealthWorker(AbstractBase):
    """
    A person who is incharge of a certain community health area.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    id_number = models.PositiveIntegerField(unique=True)
    households_monitored = models.PositiveIntegerField(defaul=0)

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
