import json
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
    households_monitored = models.PositiveIntegerField(default=0)
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

    def __str__(self):
        return self.name

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

    def clean(self):
        super(CommunityHealthUnit, self).clean()
        self.validate_facility_is_not_closed()
        self.validate_either_approved_or_rejected_and_not_both()

    def _dump_updates(self):
        updates = {}
        old_obj = self.__class__.objects.get(id=self.id)
        fields = [obj.name for obj in self.__class__._meta.fields]
        del fields[fields.index('id')]
        del fields[fields.index('created')]
        del fields[fields.index('updated')]
        del fields[fields.index('created_by')]
        del fields[fields.index('updated_by')]
        for field in fields:
            if getattr(old_obj, field) != getattr(self, field):
                updates[field] = getattr(self, field)
        return json.dumps(updates) if any(updates) else None

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        if not self.is_approved and not self.is_rejected:
            super(CommunityHealthUnit, self).save(*args, **kwargs)
        allow_save = kwargs.pop('allow_save', None)
        if allow_save:
            super(CommunityHealthUnit, self).save(*args, **kwargs)
        updates = self._dump_updates()
        if updates:
            try:
                pending_update = ChuUpdateBuffer.objects.get(
                    is_approved=False, is_rejected=False)
                pending_update.basic = updates
                pending_update.save()
            except ChuUpdateBuffer.DoesNotExist:
                pending_update = ChuUpdateBuffer.objects.create(
                    health_unit=self, created_by=self.created_by,
                    updated_by=self.updated_by)
                pending_update.basic = updates
                pending_update.save()

    @property
    def average_rating(self):
        return self.chu_ratings.aggregate(r=models.Avg('rating'))['r'] or 0

    class Meta(AbstractBase.Meta):
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
    The contacts of the healh worker.

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
    A person who is incharge of a certain community health area.

    The status of the worker that is whether still active or not will be
    shown by the active field inherited from abstract base.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    id_number = models.PositiveIntegerField(unique=True, null=True, blank=True)
    is_incharge = models.BooleanField(default=False)
    health_unit = models.ForeignKey(
        CommunityHealthUnit,
        help_text='The health unit the worker is incharge of',
        related_name='health_unit_workers')

    def __str__(self):
        return "{} ({})".format(self.first_name, self.id_number)

    class Meta(AbstractBase.Meta):
        unique_together = ('id_number', 'health_unit')

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name).strip()


@reversion.register
@encoding.python_2_unicode_compatible
class CHUService(AbstractBase):
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
    is_cancelled = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def validate_atleast_one_attribute_updated(self):
        if not self.workers and not self.contacts and not self.basic:
            raise ValidationError({"__all__": ["Nothing was editted"]})

    def update_basic_details(self):
        basic_details = json.loads(self.basic)
        for key, value in basic_details.iteritems():
            setattr(self.health_unit, key, value)
        self.health_unit.save(allow_save=True)

    def update_workers(self):
        chews = json.loads(self.workers)
        for chew in chews:
            chew['health_unit'] = self.health_unit
            chew['created_by_id'] = self.created_by_id
            chew['updated_by_id'] = self.updated_by_id
            CommunityHealthWorker.objects.create(**chew)

    def update_contacts(self):
        contacts = json.loads(self.contacts)
        for contact in contacts:
            contact['updated_by_id'] = self.updated_by_id
            contact['created_by_id'] = self.created_by_id
            contact['contact_type_id'] = contact['contact_type']
            contact_obj = Contact.objects.create(**contact)
            CommunityHealthUnitContact.objects.create(
                contact=contact_obj, health_unit=self.health_unit,
                created_by_id=self.created_by_id,
                updated_by_id=self.updated_by_id)

    def updates(self):
        updates = {}
        if self.basic:
            updates['basic'] = json.loads(self.basic)
        if self.contacts:
            updates['contacts'] = json.loads(self.contacts)
        if self.workers:
            updates['workers'] = json.loads(self.workers)

    def clean(self, *args, **kwargs):
        self.validate_atleast_one_attribute_updated()
