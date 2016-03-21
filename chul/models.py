import json
import datetime
import reversion

from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils import timezone, encoding

from common.models import AbstractBase, Contact, SequenceMixin
from common.fields import SequenceField
from facilities.models import Facility


@reversion.register
@encoding.python_2_unicode_compatible
class Status(AbstractBase):

    """
    Indicates the operation status of a community health unit.
    e.g  fully-functional, semi-functional, functional
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'statuses'


@reversion.register(follow=['health_unit', 'contact'])
@encoding.python_2_unicode_compatible
class CommunityHealthUnitContact(AbstractBase):

    """
    The contacts of the health unit may be email, fax mobile etc.
    """
    health_unit = models.ForeignKey('CommunityHealthUnit')
    contact = models.ForeignKey(Contact)

    def __str__(self):
        return "{}: ({})".format(self.health_unit, self.contact)

    class Meta(object):
        unique_together = ('health_unit', 'contact', )
        # a hack since the view_communityhealthunitcontact
        # is disappearing into thin air
        permissions = (
            (
                "view_communityhealthunitcontact",
                "Can view community health_unit contact"
            ),
        )


@reversion.register(follow=['facility', 'status'])
@encoding.python_2_unicode_compatible
class CommunityHealthUnit(SequenceMixin, AbstractBase):

    """
    This is a health service delivery structure within a defined geographical
    area covering a population of approximately 5,000 people.

    Each unit is assigned 2 Community Health Extension Workers (CHEWs) and
    community health volunteers who offer promotive, preventative and basic
    curative health services
    """
    name = models.CharField(max_length=100)
    code = SequenceField(unique=True)
    facility = models.ForeignKey(
        Facility,
        help_text='The facility on which the health unit is tied to.')
    status = models.ForeignKey(Status)
    households_monitored = models.PositiveIntegerField(
        default=0,
        help_text='The number of house holds a CHU is in-charge of')
    date_established = models.DateField(default=timezone.now)
    date_operational = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approval_comment = models.TextField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    closing_comment = models.TextField(null=True, blank=True)
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(null=True, blank=True)
    has_edits = models.BooleanField(
        default=False,
        help_text='Indicates that a community health unit has updates that are'
                  ' pending approval')
    number_of_chvs = models.PositiveIntegerField(
        default=0,
        help_text='Number of Community Health volunteers in the CHU')

    def __str__(self):
        return self.name

    @property
    def workers(self):
        from .serializers import CommunityHealthWorkerPostSerializer
        return CommunityHealthWorkerPostSerializer(
            self.health_unit_workers, many=True).data

    def validate_facility_is_not_closed(self):
        if self.facility.closed:
            raise ValidationError(
                {
                    "facility":
                    [
                        "A Community Unit cannot be attached to a closed "
                        "facility"
                    ]
                }
            )

    def validate_either_approved_or_rejected_and_not_both(self):
        error = {
            "approve/reject": [
                "A Community Unit cannot be approved and"
                " rejected at the same time "]
        }
        values = [self.is_approved, self.is_rejected]
        if values.count(True) > 1:
            raise ValidationError(error)

    def validate_date_operation_is_less_than_date_established(self):
        if self.date_operational and self.date_established:
            if self.date_established > self.date_operational:
                raise ValidationError(
                    {
                        "date_operational": [
                            "Date operation cannot be greater than date "
                            "established"
                        ]
                    })

    def validate_date_established_not_in_future(self):
        """
        Only the date operational needs to be validated.

        date_established should always be less then the date_operational.
        Thus is the date_operational is not in future the date_established
        is also not in future
        """

        today = datetime.datetime.now().date()

        if self.date_operational and self.date_operational > today:
            raise ValidationError(
                {
                    "date_operational": [
                        "The date operational cannot be in the future"
                    ]
                })

    @property
    def contacts(self):
        return [
            {
                "id": con.id,
                "contact_id": con.contact.id,
                "contact": con.contact.contact,
                "contact_type": con.contact.contact_type.id,
                "contact_type_name": con.contact.contact_type.name

            }
            for con in CommunityHealthUnitContact.objects.filter(
                health_unit=self)
        ]

    @property
    def json_features(self):
        return {
            "geometry": {
                "coordinates": [
                    self.facility.facility_coordinates_through.coordinates[0],
                    self.facility.facility_coordinates_through.coordinates[1]
                ]
            },
            "properties": {
                "ward": self.facility.ward.id,
                "constituency": self.facility.ward.constituency.id,
                "county": self.facility.ward.county.id
            }
        }

    def clean(self):
        super(CommunityHealthUnit, self).clean()
        self.validate_facility_is_not_closed()
        self.validate_either_approved_or_rejected_and_not_both()
        self.validate_date_operation_is_less_than_date_established()
        self.validate_date_established_not_in_future()

    @property
    def pending_updates(self):
        try:
            chu = ChuUpdateBuffer.objects.get(
                is_approved=False,
                is_rejected=False,
                health_unit=self
            )
            return chu.updates
        except ChuUpdateBuffer.DoesNotExist:
            return {}

    @property
    def latest_update(self):
        try:
            chu = ChuUpdateBuffer.objects.get(
                is_approved=False,
                is_rejected=False,
                health_unit=self
            )
            return chu
        except ChuUpdateBuffer.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        super(CommunityHealthUnit, self).save(*args, **kwargs)

    @property
    def average_rating(self):
        return self.chu_ratings.aggregate(r=models.Avg('rating'))['r'] or 0

    @property
    def rating_count(self):
        return self.chu_ratings.count()

    class Meta(AbstractBase.Meta):
        unique_together = ('name', 'facility', )
        permissions = (
            (
                "view_rejected_chus",
                "Can see the rejected community health units"
            ),
            (
                "can_approve_chu",
                "Can approve or reject a Community Health Unit"
            ),

        )


@reversion.register(follow=['health_worker', 'contact'])
@encoding.python_2_unicode_compatible
class CommunityHealthWorkerContact(AbstractBase):

    """
    The contacts of the health worker.

    They may be as many as the health worker has.
    """
    health_worker = models.ForeignKey('CommunityHealthWorker')
    contact = models.ForeignKey(Contact)

    def __str__(self):
        return "{}: ({})".format(self.health_worker, self.contact)


@reversion.register(follow=['health_unit'])
@encoding.python_2_unicode_compatible
class CommunityHealthWorker(AbstractBase):

    """
    A person who is in-charge of a certain community health area.

    The status of the worker that is whether still active or not will be
    shown by the active field inherited from abstract base.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_incharge = models.BooleanField(default=False)
    health_unit = models.ForeignKey(
        CommunityHealthUnit,
        help_text='The health unit the worker is in-charge of',
        related_name='health_unit_workers')

    def __str__(self):
        return "{} ({})".format(self.first_name, self.health_unit.name)

    @property
    def name(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name).strip()
        else:
            return self.first_name


@reversion.register
@encoding.python_2_unicode_compatible
class CHUService(AbstractBase):

    """
    The services offered by the Community Health Units

    Examples:
        1. First Aid Administration
        2. De-worming e.t.c.

    All the community health units offer these services. Hence, there is
    no need to link a COmmunity Health Unit to a CHUService instance
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


@reversion.register
@encoding.python_2_unicode_compatible
class CHURating(AbstractBase):

    """Rating of a CHU"""

    chu = models.ForeignKey(CommunityHealthUnit, related_name='chu_ratings')
    rating = models.PositiveIntegerField(
        validators=[
            validators.MaxValueValidator(5),
            validators.MinValueValidator(0)
        ]
    )
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.chu, self.rating)


class ChuUpdateBuffer(AbstractBase):
    """
    Buffers a community units updates until they are approved by the CHRIO
    """
    health_unit = models.ForeignKey(CommunityHealthUnit)
    workers = models.TextField(null=True, blank=True)
    contacts = models.TextField(null=True, blank=True)
    basic = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)

    def validate_atleast_one_attribute_updated(self):
        if not self.workers and not self.contacts and not \
                self.basic and not self.is_new:
            raise ValidationError({"__all__": ["Nothing was edited"]})

    def update_basic_details(self):
        basic_details = json.loads(self.basic)
        if 'status' in basic_details:
            basic_details['status_id'] = basic_details.get(
                'status').get('status_id')
            basic_details.pop('status')
        if 'facility' in basic_details:
            basic_details['facility_id'] = basic_details.get(
                'facility').get('facility_id')
            basic_details.pop('facility')

        for key, value in basic_details.iteritems():
            setattr(self.health_unit, key, value)
        self.health_unit.save()

    def update_workers(self):
        chews = json.loads(self.workers)
        for chew in chews:
            chew['health_unit'] = self.health_unit
            chew['created_by_id'] = self.created_by_id
            chew['updated_by_id'] = self.updated_by_id
            chew.pop('created_by', None)
            chew.pop('updated_by', None)
            if 'id' in chew:
                chew_obj = CommunityHealthWorker.objects.get(
                    id=chew['id'])
                chew_obj.first_name = chew['first_name']
                chew_obj.last_name = chew['last_name']
                if 'is_incharge' in chew:
                    chew_obj.is_incharge = chew['is_incharge']
                chew_obj.save()
            else:
                CommunityHealthWorker.objects.create(**chew)

    def update_contacts(self):
        contacts = json.loads(self.contacts)
        for contact in contacts:
            contact['updated_by_id'] = self.updated_by_id
            contact['created_by_id'] = self.created_by_id
            contact['contact_type_id'] = contact['contact_type']
            contact.pop('contact_type', None)
            contact.pop('contact_id', None)
            contact.pop('contact_type_name', None)
            contact['contact'] = contact['contact']
            contact_data = {
                'contact_type_id': contact['contact_type_id'],
                'contact': contact['contact']
            }
            try:
                contact_obj = Contact.objects.get(**contact_data)
            except Contact.DoesNotExist:
                contact_obj = Contact.objects.create(**contact)
            try:
                CommunityHealthUnitContact.objects.filter(
                    contact=contact_obj)[0]
            except IndexError:
                CommunityHealthUnitContact.objects.create(
                    contact=contact_obj,
                    health_unit=self.health_unit,
                    created_by_id=self.created_by_id,
                    updated_by_id=self.updated_by_id)

    @property
    def updates(self):
        updates = {}
        if self.basic:
            updates['basic'] = json.loads(self.basic)
        if self.contacts:
            updates['contacts'] = json.loads(self.contacts)
        if self.workers:
            updates['workers'] = json.loads(self.workers)
        updates['updated_by'] = self.updated_by.get_full_name
        return updates

    def clean(self, *args, **kwargs):
        if not self.is_approved and not self.is_rejected:
            self.health_unit.has_edits = True
            self.health_unit.save()
        if self.is_approved and self.contacts:
            self.update_contacts()
            self.health_unit.has_edits = False
            self.health_unit.save()

        if self.is_approved and self.workers:
            self.update_workers()
            self.health_unit.has_edits = False
            self.health_unit.save()

        if self.is_approved and self.basic:
            self.update_basic_details()
            self.health_unit.has_edits = False
            self.health_unit.save()

        if self.is_rejected:
            self.health_unit.has_edits = False
            self.health_unit.save()

        self.validate_atleast_one_attribute_updated()

    def __str__(self):
        return self.health_unit.name
