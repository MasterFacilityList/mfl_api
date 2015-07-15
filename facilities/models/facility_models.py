from __future__ import division

import reversion
import json

from django.conf import settings
from django.core import validators
from django.db import models

from django.core.exceptions import ValidationError
from common.models import (
    AbstractBase,
    Ward,
    Contact,
    SequenceMixin,
    PhysicalAddress
)
from common.fields import SequenceField


@reversion.register
class OwnerType(AbstractBase):
    """
    Sub divisions of owners of facilities.

    Owners of facilities could be classified into several categories.
    E.g we could have government, corporate owners, faith based owners
    private owners.
    """
    name = models.CharField(
        max_length=100,
        help_text="Short unique name for a particular type of owners. "
        "e.g INDIVIDUAL")
    description = models.TextField(
        null=True, blank=True,
        help_text="A brief summary of the particular type of owner.")

    def __unicode__(self):
        return self.name


@reversion.register
class Owner(AbstractBase, SequenceMixin):
    """
    Entity that has exclusive legal rights to the facility.

    For the master facility list, ownership especially for the faith-based
    facilities is broadened to also include the body that coordinates
    service delivery and health programmes. Therefore, the Christian Health
    Association of Kenya (CHAK), Kenya Episcopal Conference (KEC), or
    Supreme Council of Kenya Muslim (SUPKEM) will be termed as owners though
    in fact the facilities under them are owned by the individual churches,
    mosques, or communities affiliated with the faith.
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text="The name of owner e.g Ministry of Health.")
    description = models.TextField(
        null=True, blank=True, help_text="A brief summary of the owner.")
    code = SequenceField(
        unique=True,
        help_text="A unique number to identify the owner."
        "Could be up to 7 characteres long.", editable=False)
    abbreviation = models.CharField(
        max_length=30, null=True, blank=True,
        help_text="Short form of the name of the owner e.g Ministry of health"
        " could be shortened as MOH")
    owner_type = models.ForeignKey(
        OwnerType,
        help_text="The classification of the owner e.g INDIVIDUAL",
        on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        super(Owner, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


@reversion.register
class JobTitle(AbstractBase):
    """
    This is the job title names of the officers incharge of facilities.

    For example, Nursing Officer In-Charge, Medical Superintendent, and
    Hospital Director. This should not be confused with the professional
     (Nursing Officer I) or Job Group title.Officer
    """
    name = models.CharField(
        max_length=100,
        help_text="A short name for the job title")
    description = models.TextField(
        null=True, blank=True,
        help_text="A short summary of the job title")

    def __unicode__(self):
        return self.name


@reversion.register
class OfficerContact(AbstractBase):
    """
    The contact details of the officer incharge.

    The officer incharge may have as many mobile numbers as possible.
    Also the number of email addresses is not limited.
    """
    officer = models.ForeignKey(
        'Officer',
        help_text="The is the officer in charge", on_delete=models.PROTECT)
    contact = models.ForeignKey(
        Contact,
        help_text="The contact of the officer incharge may it be email, "
        " mobile number etc", on_delete=models.PROTECT)

    def __unicode__(self):
        return "{}: {}".format(self.officer.name, self.contact.contact)


@reversion.register
class Officer(AbstractBase):
    """
    Identify officers in-charge of facilities
    """
    name = models.CharField(
        max_length=255,
        help_text="the name of the officer in-charge e.g Roselyne Wiyanga ")
    id_number = models.CharField(
        max_length=10, null=True, blank=True,
        help_text='The  National Identity number of the officer')
    registration_number = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="This is the licence number of the officer. e.g for a nurse"
        " use the NCK registration number.")
    job_title = models.ForeignKey(JobTitle, on_delete=models.PROTECT)

    contacts = models.ManyToManyField(
        Contact, through=OfficerContact,
        help_text='Personal contacts of the officer in charge')

    def __unicode__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'officer in charge'
        verbose_name_plural = 'officers in charge'


@reversion.register
class FacilityStatus(AbstractBase):
    """
    Facility Operational Status covers the following elements:
    whether the facility
        1. has been approved to operate
        2. is operating
        3. is temporarily non-operational
        4. is closed down.
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text="A short name respresenting the operanation status"
        " e.g OPERATIONAL")
    description = models.TextField(
        null=True, blank=True,
        help_text="A short explanation of what the status entails.")

    def __unicode__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'facility statuses'


@reversion.register
class FacilityType(AbstractBase):
    owner_type = models.ForeignKey(
        OwnerType, null=True, blank=True)
    name = models.CharField(
        max_length=100, unique=True,
        help_text="A short unique name for the facility type e.g DISPENSARY")
    sub_division = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="This is a further division of the facility type e.g "
        "Hospitals can be further divided into District hispitals and"
        " Provincial Hospitals.")
    preceding = models.ForeignKey(
        'self', null=True, blank=True, related_name='preceding_type',
        help_text='The facility type that comes before this type')

    def __unicode__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        unique_together = ('name', 'sub_division', )


@reversion.register
class RegulatingBodyContact(AbstractBase):
    """
    A regulating body contacts.
    """
    regulating_body = models.ForeignKey('RegulatingBody')
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return "{}: {}".format(self.regulating_body, self.contact)


@reversion.register
class RegulatingBody(AbstractBase):
    """
    Bodies responsible for licensing of facilities.

    This is normally based on the relationship between the facility
    owner and the Regulator. For example, MOH-owned facilities are
    gazetted by the Director of Medical Services (DMS)  and the facilities
    owned by private practice nurses are licensed by the NCK.
    In some cases this may not hold e.g a KMPDB and not NCK will licence a
    nursing home owned by a nurse
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text="The name of the regulating body")
    abbreviation = models.CharField(
        max_length=50, null=True, blank=True,
        help_text="A shortform of the name of the regulating body e.g Nursing"
        "Council of Kenya could be abbreviated as NCK.")
    contacts = models.ManyToManyField(
        Contact, through='RegulatingBodyContact')
    regulation_verb = models.CharField(
        max_length=100)
    regulatory_body_type = models.ForeignKey(
        OwnerType, null=True, blank=True,
        help_text='Show the kind of institutions that the body regulates e.g'
        'private facilities')

    @property
    def postal_address(self):
        contacts = RegulatingBodyContact.objects.filter(
            regulating_body=self,
            contact__contact_type__name='POSTAL')
        return contacts[0]

    def __unicode__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'regulating bodies'


@reversion.register
class RegulatoryBodyUser(AbstractBase):
    """
    Links user to a regulatory body.
    These are the users who  will be carrying out the regulatory activities
    """
    regulatory_body = models.ForeignKey(RegulatingBody)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='regulatory_users')

    def make_user_national_user(self):
        self.user.is_national = True
        self.user.save()

    def __unicode__(self):
        custom_unicode = "{}: {}".format(self.regulatory_body, self.user)
        return custom_unicode

    def clean(self, *args, **kwargs):
        self.make_user_national_user()

    class Meta(AbstractBase.Meta):
        unique_together = ('regulatory_body', 'user', )


@reversion.register
class RegulationStatus(AbstractBase):
    """
    A Regulation state.

    The regulation states could be
        1. Pending Licensing: A facility that has been recommended by the DHMT
            but is  waiting for the license from the National Regulatory Body.

        2: Licensed:
            A facility that has been approved and issued a license by the
            appropriate National Regulatory Body.
        3. License Suspended:
            A facility whose license has been temporarily stopped for
            reasons including self-request, sickness, and disciplinary action.
        4. License Cancelled:
            A facility whose license has been permanently stopped by the
            national body.
        5. Pending Registration:
            A facility that has been approved by the DHMT as an Institution
            and a request for registration sent the KMPDB.
        6. Registered:
            A facility that has been approved as an institution by
            the KMPDB and a registration number given.
        7. Pending Gazettement:
            A facility that has been inspected and recommended by the DHMT
            (or District Development Committee [DDC] or presidential mandate)
            for gazettement as a MOH facility, but has not yet been officially
            gazetted. The facility is awaiting official gazettement and is
            known as 'pending gazettement'.
        8. Gazetted:
            A facility that has been gazetted and the notice published in the
            Kenya Gazette.

    There are number of fields that are worth looking at:
        is_initial_state:
            This is the state that shows whether the state is the
            first state
            Is should be only one for the entire api
        is_final_state:
            This is last state of the of the workflow state.
            Just like the is_initial_state is should be the only one in the
            entire workflow
        previous_status:
            If status has a a preceding status, it should added here.
            If does not then leave it blank.
            A status can have only one previous state.
        next_status:
            If the status has a suceedding status, it should be added here,
            If does not not leave it blank
            Again just the 'previous' field,  a status can have only one
            'next' field.
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text="A short unique name representing a state/stage of "
        "regulation e.g. PENDING_OPENING ")
    description = models.TextField(
        null=True, blank=True,
        help_text="A short description of the regulation state or state e.g"
        "PENDING_LINCENSING could be descriped as 'waiting for the license to"
        "begin operating' ")
    previous_status = models.ForeignKey(
        'self', related_name='previous_state', null=True, blank=True,
        help_text='The regulation_status preceding this regulation status.')
    next_status = models.ForeignKey(
        'self', related_name='next_state', null=True, blank=True,
        help_text='The regulation_status suceedding this regulation status.')
    is_initial_state = models.BooleanField(
        default=False,
        help_text='Indicates whether it is the very first state'
        'in the regulation workflow.')
    is_final_state = models.BooleanField(
        default=False,
        help_text='Indicates whether it is the last state'
        ' in the regulation work-flow')
    is_default = models.BooleanField(
        default=False,
        help_text='The default regulation status for facilties')

    @property
    def previous_state_name(self):
        if self.previous_status:
            return self.previous_status.name
        else:
            return ""

    @property
    def next_state_name(self):
        if self.next_status:
            return self.next_status.name
        else:
            return ""

    def validate_only_one_final_state(self):
        final_state = self.__class__.objects.filter(
            is_final_state=True)
        if final_state.count() > 0 and self.is_final_state:
            raise ValidationError("Only one final state is allowed.")

    def validate_only_one_initial_state(self):
        initial_state = self.__class__.objects.filter(is_initial_state=True)
        if initial_state.count() > 0 and self.is_initial_state:
            raise ValidationError("Only one Initial state is allowed.")

    def validate_only_one_default_status(self):
        default_states_count = self.__class__.objects.filter(
            is_default=True).count()
        if self.is_default and default_states_count >= 1:
            raise ValidationError(
                "Only one default regulation status is allowed")

    def clean(self, *args, **kwargs):
        self.validate_only_one_final_state()
        self.validate_only_one_initial_state()
        self.validate_only_one_default_status()
        super(RegulationStatus, self).clean(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'regulation_statuses'


@reversion.register
class FacilityRegulationStatus(AbstractBase):
    """
    Shows the regulation status of a facility.

    It adds the extra reason field that makes it possible to give
    an explanation as to why a facility is in a certain regulation status.
    """
    facility = models.ForeignKey(
        'Facility', on_delete=models.PROTECT,
        related_name='regulatory_details')
    regulating_body = models.ForeignKey(
        RegulatingBody, on_delete=models.PROTECT)
    regulation_status = models.ForeignKey(
        RegulationStatus, on_delete=models.PROTECT)
    reason = models.TextField(
        null=True, blank=True,
        help_text="An explanation for as to why is the facility is being"
        "put in the particular status")
    license_number = models.CharField(
        max_length=100, null=True, blank=True,
        help_text='The license number that the facility has been '
        'given by the regulator')
    is_confirmed = models.BooleanField(
        default=False,
        help_text='Has the proposed change been confirmed by higher'
        ' authorities')
    is_cancelled = models.BooleanField(
        default=False,
        help_text='Has the proposed change been cancelled by a higher'
        ' authority')

    def __unicode__(self):
        return "{}: {}".format(
            self.facility.name, self.regulation_status.name)

    def clean(self, *args, **kwargs):
        self.facility.regulated = True
        self.facility.save(allow_save=True)

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'facility regulation statuses'


@reversion.register
class FacilityContact(AbstractBase):
    """
    The facility contact.

    The facility contacts could be as many as the facility has.
    They also could be of as many different types as the facility has;
    they could be emails, phone numbers, land lines etc.
    """
    facility = models.ForeignKey(
        'Facility', related_name='facility_contacts', on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)

    def __unicode__(self):
        return "{}: {}".format(
            self.facility.name, self.contact.contact)


@reversion.register
class Facility(SequenceMixin, AbstractBase):
    """
    A health institution in Kenya.

    The health institution considered as facilities include:
    Health Centres, Dispensaries, Hospitals etc.
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text='This is the official name of the facility')
    code = SequenceField(
        unique=True, editable=False,
        help_text='A sequential number allocated to each facility')
    abbreviation = models.CharField(
        max_length=30, null=True, blank=True,
        help_text='A short name for the facility.')
    description = models.TextField(
        null=True, blank=True,
        help_text="A brief summary of the Facility")
    number_of_beds = models.PositiveIntegerField(
        default=0,
        help_text="The number of beds that a facility has. e.g 0")
    number_of_cots = models.PositiveIntegerField(
        default=0,
        help_text="The number of cots that a facility has e.g 0")
    open_whole_day = models.BooleanField(
        default=False,
        help_text="Does the facility operate 24 hours a day")
    open_public_holidays = models.BooleanField(
        default=False,
        help_text="Is the facility open on public holidays?")
    open_weekends = models.BooleanField(
        default=False,
        help_text="Is the facility_open during weekends?")
    is_classified = models.BooleanField(
        default=False,
        help_text="Should the facility geo-codes be visible to the public?"
        "Certain facilities are kept 'off-the-map'")

    # publishing is done at the county level
    is_published = models.BooleanField(
        default=False,
        help_text="COnfirmation by the CHRIO that the facility is okay")
    facility_type = models.ForeignKey(
        FacilityType,
        help_text="This depends on who owns the facility. For MOH facilities,"
        "type is the gazetted classification of the facility."
        "For Non-MOH check under the respective owners.",
        on_delete=models.PROTECT)
    operation_status = models.ForeignKey(
        FacilityStatus, null=True, blank=True,
        help_text="Indicates whether the facility"
        "has been approved to operate, is operating, is temporarily"
        "non-operational, or is closed down")
    ward = models.ForeignKey(
        Ward,
        on_delete=models.PROTECT,
        help_text="County ward in which the facility is located")
    owner = models.ForeignKey(
        Owner, help_text="A link to the organization that owns the facility")
    physical_address = models.ForeignKey(
        PhysicalAddress, null=True, blank=True,
        help_text="Postal and courier addressing for the facility")

    contacts = models.ManyToManyField(
        Contact, through=FacilityContact,
        help_text='Facility contacts - email, phone, fax, postal etc')
    parent = models.ForeignKey(
        'self', help_text='Indicates the umbrella facility of a facility',
        null=True, blank=True)
    attributes = models.TextField(null=True, blank=True)
    regulatory_body = models.ForeignKey(
        RegulatingBody, null=True, blank=True)
    regulated = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    @property
    def boundaries(self):
        from mfl_gis.models import (
            CountyBoundary, ConstituencyBoundary, WardBoundary)

        return {
            "county_boundary": str(CountyBoundary.objects.get(
                area=self.ward.constituency.county).id),
            "constituency_boundary": str(ConstituencyBoundary.objects.get(
                area=self.ward.constituency).id),
            "ward_boundary": str(WardBoundary.objects.get(area=self.ward).id)
        }

    @property
    def has_edits(self):
        return True if self.latest_update else False

    @property
    def latest_update(self):
        facility_updates = FacilityUpdates.objects.filter(
            facility=self, approved=False, cancelled=False)
        if facility_updates:
            return str(facility_updates[0].id)
        else:
            return None

    @property
    def ward_name(self):
        return self.ward.name

    @property
    def facility_physical_address(self):
        return {
            "id": self.physical_address.id,
            "town": self.physical_address.town.name,
            "town_id": self.physical_address.town.id,
            "nearest_landmark": self.physical_address.nearest_landmark,
            "plot_number": self.physical_address.plot_number,
            "location_desc": self.physical_address.location_desc
        }

    @property
    def get_county(self):
        return self.ward.constituency.county.name

    @property
    def get_constituency(self):
        return self.ward.constituency.name

    def validate_publish(self):
        if self.is_published and not self.is_approved:
            message = "A facility has to be approved for it to be published"
            raise ValidationError(message)

    @property
    def current_regulatory_status(self):
        try:
            # returns in reverse chronological order so just pick the first one
            return self.regulatory_details.filter(is_confirmed=True)[0]
        except IndexError:
            return RegulationStatus.objects.get(is_default=True)

    @property
    def is_regulated(self):
        default_reg_status = RegulationStatus.objects.get(is_default=True)
        if self.current_regulatory_status != default_reg_status:
            return True
        else:
            return False

    @property
    def county(self):
        return self.ward.constituency.county.name

    @property
    def constituency(self):
        return self.ward.constituency.name

    @property
    def operation_status_name(self):
        return self.operation_status.name

    @property
    def regulatory_status_name(self):
        if self.current_regulatory_status:
            return self.current_regulatory_status.regulation_status.name

    @property
    def facility_type_name(self):
        return self.facility_type.name

    @property
    def owner_name(self):
        return self.owner.name

    @property
    def owner_type_name(self):
        return self.owner.owner_type.name

    @property
    def is_approved(self):
        approvals = FacilityApproval.objects.filter(
            facility=self, is_cancelled=False).count()
        if approvals:
            return True
        else:
            False

    @property
    def latest_approval(self):
        approvals = FacilityApproval.objects.filter(
            facility=self, is_cancelled=False)
        if approvals:
            return str(approvals[0].id)
        else:
            return None

    @property
    def get_facility_services(self):
        """Digests the facility_services for the sake of frontend."""
        services = self.facility_services.all()
        return [
            {
                "id": service.id,
                "service_id": service.selected_option.service.id,
                "service_name": service.selected_option.service.name,
                "option_name": service.selected_option.option.display_text,
                "category_name": service.selected_option.service.category.name,
                "category_id": service.selected_option.service.category.id,
                "average_rating": service.average_rating,
                "number_of_ratings": service.number_of_ratings
            }
            for service in services
        ]

    @property
    def get_facility_contacts(self):
        """For the same purpose as the get_facility_services above"""
        contacts = self.facility_contacts.all()
        return [
            {
                "id": contact.id,
                "contact_id": contact.contact.id,
                "contact": contact.contact.contact,
                "contact_type_name": contact.contact.contact_type.name
            }
            for contact in contacts
        ]

    @property
    def average_rating(self):
        avg_service_rating = [
            i.average_rating for i in self.facility_services.all()
        ]
        try:
            return sum(avg_service_rating, 0) / self.facility_services.count()
        except ZeroDivisionError:
            return 0

    @property
    def coordinates(self):
        try:
            return self.facility_coordinates_through.id
        except:
            return None

    def clean(self, *args, **kwargs):
        self.validate_publish(*args, **kwargs)
        super(Facility, self).clean()

    def _dump_updates(self, origi_model):
        fields = [field.name for field in self._meta.fields]
        forbidden_fields = [
            'operation_status', 'regulatory_status', 'facility_type',
            'operation_status_id', 'regulatory_status_id', 'facility_type_id']
        for field in fields:
            if hasattr(getattr(self, field), 'id'):
                field_name = field + "_id"
                fields.append(field_name)
                del fields[fields.index(field)]
        data = {}

        for field in fields:
            if (getattr(self, field) != getattr(origi_model, field)
                    and field not in forbidden_fields):
                data[field] = str(getattr(self, field))
        if any(data):
            return json.dumps(data)
        else:
            error = "Either no field was editted or you editted all or one"
            " of {} which are not allowed".format(forbidden_fields)
            raise ValidationError(error)

    def save(self, *args, **kwargs):
        """
        Overide the save method in order to capture updates to a facility.
        This creates a record of the updates in the FacilityUpdates model.
        The updates will appear on the facilty once the updates have been
        approved.
        """
        from facilities.serializers import FacilityDetailSerializer
        if not self.code:
            self.code = self.generate_next_code_sequence()
        if not self.is_approved:
            kwargs.pop('allow_save', None)
            super(Facility, self).save(*args, **kwargs)
            return

        # Allow publishing facilities without requiring approvals
        old_details = self.__class__.objects.get(id=self.id)
        if not old_details.is_published and self.is_published:
            kwargs.pop('allow_save', None)
            super(Facility, self).save(*args, **kwargs)
            return
        old_details_serialized = FacilityDetailSerializer(old_details).data
        del old_details_serialized['updated']
        del old_details_serialized['created']
        del old_details_serialized['updated_by']
        new_details_serialized = FacilityDetailSerializer(self).data
        del new_details_serialized['updated']
        del new_details_serialized['created']
        del new_details_serialized['updated_by']

        if new_details_serialized != old_details_serialized:

            origi_model = self.__class__.objects.get(id=self.id)
            allow_save = kwargs.pop('allow_save', None)
            if allow_save:
                super(Facility, self).save(*args, **kwargs)
            else:
                updates = self._dump_updates(origi_model)
                try:
                    updates.pop('updated_by')
                except:
                    pass
                try:
                    updates.pop('updated_by_id')
                except:
                    pass
                FacilityUpdates.objects.create(
                    facility_updates=updates, facility=self,
                    created_by=self.updated_by, updated_by=self.updated_by
                )
        else:
            kwargs.pop('allow_save', None)
            super(Facility, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'facilities'
        permissions = (
            ("view_classified_facilities", "Can see classified facilities"),
            ("publish_facilities", "Can publish facilities"),
        )


class FacilityUpdates(AbstractBase):
    """
    Buffers facility updates until when they are approved upon
    which they reflect on the facility.
    """
    facility = models.ForeignKey(Facility, related_name='updates')
    approved = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    facility_updates = models.TextField()

    def facility_updated_json(self):
        return json.loads(self.facility_updates)

    def update_facility(self):
        data = json.loads(self.facility_updates)
        for key, value in data.items():
            setattr(self.facility, key, value)
        self.facility.save(allow_save=True)

    def validate_either_of_approve_or_cancel(self):
        error = "You can only approve or cancel and not both"
        if self.approved and self.cancelled:
            raise ValidationError(error)

    def validate_only_one_update_at_a_time(self):
        updates = self.__class__.objects.filter(
            facility=self.facility, approved=False, cancelled=False).count()
        if self.approved or self.cancelled:
            # No need to validate again as this is
            # an approval or rejection after the record was created first
            pass
        else:
            if updates >= 1:
                error = "The pending facility update has to be either approved "\
                    "or cancelled before another one is made"
                raise ValidationError(error)

    def clean(self, *args, **kwargs):
        self.validate_only_one_update_at_a_time()
        self.validate_either_of_approve_or_cancel()
        super(FacilityUpdates, self).clean()

    def save(self, *args, **kwargs):
        if self.approved and not self.cancelled:
            self.update_facility()
        super(FacilityUpdates, self).save(*args, **kwargs)


@reversion.register
class FacilityOperationState(AbstractBase):
    """
    logs chages to the operation_status of a facility.
    """
    operation_status = models.ForeignKey(
        FacilityStatus,
        help_text="Indicates whether the facility"
        "has been approved to operate, is operating, is temporarily"
        "non-operational, or is closed down")
    facility = models.ForeignKey(
        Facility, related_name='facility_operation_states')
    reason = models.TextField(
        null=True, blank=True,
        help_text='Additional information for the transition')


@reversion.register
class FacilityUpgrade(AbstractBase):
    """
    Logs the upgrades and the downgrades of a facility.
    """
    facility = models.ForeignKey(Facility, related_name='facility_upgrades')
    facility_type = models.ForeignKey(FacilityType)
    reason = models.TextField()
    is_confirmed = models.BooleanField(
        default=False,
        help_text='Indicates whether a facility upgrade or downgrade has been'
        ' confirmed')
    is_cancelled = models.BooleanField(
        default=False,
        help_text='Indicates whether a facility upgrade or downgrade has been'
        'cancelled or not')

    def validate_only_one_type_change_at_a_time(self):
        if self.is_confirmed or self.is_cancelled:
            pass
        else:
            type_change_count = self.__class__.objects.filter(
                facility=self.facility, is_confirmed=False, is_cancelled=False
            ).count()
            if type_change_count >= 1:
                error = "The pending level change has to confirmed"\
                        "first before another level change is made"
                raise ValidationError(error)

    def clean(self):
        super(FacilityUpgrade, self).clean()
        self.validate_only_one_type_change_at_a_time()


@reversion.register
class FacilityApproval(AbstractBase):
    """
    Before a facility is visible to the public it is first approved
    at the county level.
    The user who approves a facility will be the same as the created_by field.
    """
    facility = models.ForeignKey(Facility)
    comment = models.TextField()
    is_cancelled = models.BooleanField(
        default=False, help_text='Cancel a facility approval')

    def update_facility_rejection(self):
        if self.is_cancelled:
            self.facility.rejected = True
            self.facility.save(allow_save=True)

    def clean(self, *args, **kwargs):
        self.facility.approved = True
        self.facility.save(allow_save=True)
        self.update_facility_rejection()

    def __unicode__(self):
        return "{}: {}".format(self.facility, self.created_by)


@reversion.register
class FacilityUnitRegulation(AbstractBase):
    """
    Creates a facility units regulation status.
    A facility unit can have multiple regulation statuses
    but only one is active a time. The latest one is taken to the
    regulation status of the facility unit.
    """
    facility_unit = models.ForeignKey(
        'FacilityUnit', related_name='regulations')
    regulation_status = models.ForeignKey(
        RegulationStatus, related_name='facility_units')

    def __unicode__(self):
        custom_unicode = "{}: {}".format(
            self.facility_unit, self.regulation_status)
        return custom_unicode


@reversion.register
class FacilityUnit(AbstractBase):
    """
    Autonomous units within a facility that are regulated differently from the
    facility.

    For example AKUH  is a facility and licenced by KMPDB.
    In AKUH there are other units such as its pharmacy which is licensed by
    PPB.
    The pharmacy will in this case be treated as a facility unit.
    """
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(
        help_text='A short summary of the facility unit.')
    regulating_body = models.ForeignKey(
        RegulatingBody, null=True, blank=True)

    @property
    def regulation_status(self):
        reg_statuses = FacilityUnitRegulation.objects.filter(
            facility_unit=self)
        return reg_statuses[0].regulation_status if reg_statuses else None

    def __unicode__(self):
        return self.facility.name + ": " + self.name


@reversion.register
class ServiceCategory(AbstractBase):
    """
    Categorisation of health services. e.g Immunisation, Antenatal,
    Family Planning etc.
    """
    name = models.CharField(
        max_length=100,
        help_text="What is the name of the category? ")
    description = models.TextField(null=True, blank=True)
    abbreviation = models.CharField(
        max_length=50, null=True, blank=True,
        help_text='A short form of the category e.g ANC for antenatal')

    def __unicode__(self):
        return self.name

    @property
    def services_count(self):
        return len(self.category_services.all())

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'service categories'


@reversion.register
class Option(AbstractBase):
    """
    services could either be:
        Given in terms of KEPH levels:

        Similar services are offered in the different KEPH levels:
            For example, Environmental Health Services offered in KEPH level
            2 are similar to those offered in KEPH level 3. If the KEPH level
            of the facility is known, the corresponding KEPH level of the
            service should apply. If it is not known, write the higher KEPH
            level.

        Given through a choice of service level:
            For example, Oral Health Services are either Basic or Comprehensive

        A combination of choices and KEPH levels:
            For example, Mental Health Services are either Integrated or
            Specialised (and the Specialised Services are split into KEPH
            level).
    """
    value = models.TextField()
    display_text = models.CharField(max_length=30)
    is_exclusive_option = models.BooleanField(default=True)
    option_type = models.CharField(max_length=12, choices=(
        ('BOOLEAN', 'Yes/No or True/False responses'),
        ('INTEGER', 'Integral numbers e.g 1,2,3'),
        ('DECIMAL', 'Decimal numbers, may have a fraction e.g 3.14'),
        ('TEXT', 'Plain text'),
    ))

    def __unicode__(self):
        return "{}: {}".format(self.option_type, self.display_text)


@reversion.register
class Service(SequenceMixin, AbstractBase):
    """
    A health service.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    abbreviation = models.CharField(
        max_length=50, null=True, blank=True,
        help_text='A short form for the service e.g FANC for Focused '
        'Antenatal Care')
    category = models.ForeignKey(
        ServiceCategory,
        help_text="The classification that the service lies in.",
        related_name='category_services')

    code = SequenceField(unique=True, editable=False)
    options = models.ManyToManyField(Option, through='ServiceOption')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        super(Service, self).save(*args, **kwargs)

    @property
    def category_name(self):
        return self.category.name

    def __unicode__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'services'


@reversion.register
class ServiceOption(AbstractBase):
    """
    One service can have multiple options to be selected
    this is for defining the available choices for a service.
    """
    service = models.ForeignKey(Service, related_name='service_options')
    option = models.ForeignKey(Option)

    def __unicode__(self):
        return "{}: {}".format(self.service, self.option)


@reversion.register
class FacilityService(AbstractBase):
    """
    A facility can have zero or more services.
    """
    facility = models.ForeignKey(Facility, related_name='facility_services')
    selected_option = models.ForeignKey(ServiceOption)
    is_confirmed = models.BooleanField(
        default=False,
        help_text='Indiates whether a service has been approved by the CHRIO')
    is_cancelled = models.BooleanField(
        default=False,
        help_text='Indicates whether a service has been cancelled by the '
        'CHRIO')

    @property
    def number_of_ratings(self):
        return self.facility_service_ratings.count()

    @property
    def service_name(self):
        return self.selected_option.service.name

    @property
    def option_display_value(self):
        return self.selected_option.option.display_text

    @property
    def average_rating(self):
        avg = self.facility_service_ratings.aggregate(models.Avg('rating'))
        return avg['rating__avg'] or 0.0

    def __unicode__(self):
        return "{}: {}".format(self.facility, self.selected_option)


@reversion.register
class FacilityServiceRating(AbstractBase):

    """Rating of a facility's service"""

    facility_service = models.ForeignKey(
        FacilityService, related_name='facility_service_ratings'
    )
    rating = models.PositiveIntegerField(
        validators=[
            validators.MaxValueValidator(5),
            validators.MinValueValidator(0)
        ]
    )
    comment = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{} ({}): {}".format(
            self.facility_service.service_name,
            self.facility_service.facility.name,
            self.rating
        )


@reversion.register
class FacilityOfficer(AbstractBase):
    """
    A facility can have more than one officer. This models links the two.
    """
    facility = models.ForeignKey(Facility, related_name='facility_officers')
    officer = models.ForeignKey(Officer, related_name='officer_facilities')

    class Meta(AbstractBase.Meta):
        unique_together = ('facility', 'officer')
