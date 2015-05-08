import reversion

from django.db import models
from rest_framework.exceptions import ValidationError
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
    name = models.CharField(
        max_length=100, unique=True,
        help_text="A short unique name for the facility type e.g DISPENSARY")
    sub_division = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="This is a further division of the facility type e.g "
        "Hospitals can be further divided into District hispitals and"
        " Provincial Hospitals.")

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

    def clean(self, *args, **kwargs):
        self.validate_only_one_final_state()
        self.validate_only_one_initial_state()
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
    facility = models.ForeignKey('Facility', on_delete=models.PROTECT)
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
    location_desc = models.TextField(
        null=True, blank=True,
        help_text="This field allows a more detailed description of how to"
        "locate the facility e.g Joy medical clinic is in Jubilee Plaza"
        "7th Floor")
    number_of_beds = models.PositiveIntegerField(
        default=0,
        help_text="The number of beds that a facilty has. e.g 0")
    number_of_cots = models.PositiveIntegerField(
        default=0,
        help_text="The number of cots that a facility has e.g 0")
    open_whole_day = models.BooleanField(
        default=False,
        help_text="Is the facility open 24 hours a day?")
    open_whole_week = models.BooleanField(
        default=False,
        help_text="Is the facility open the entire week?")
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
        help_text="This depends on who owns the facilty. For MOH facilities,"
        "type is the gazetted classification of the facilty."
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
    officer_in_charge = models.ForeignKey(
        Officer, null=True, blank=True,
        help_text="The officer in charge of the facility")
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

    # synchronization is done at the national level.
    is_synchronized = models.BooleanField(
        default=False, help_text='Allow the facility to been seen the public')

    @property
    def current_regulatory_status(self):
        try:
            # returns in reverse chronological order so just pick the first one
            return self.regulatory_details.filter(is_confirmed=True)[0]
        except IndexError:
            return []

    @property
    def is_regulated(self):
        if self.current_regulatory_status:
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
    def regulary_status_name(self):
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

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_next_code_sequence()
        super(Facility, self).save(*args, **kwargs)

    @property
    def is_approved(self):
        approvals = FacilityApproval.objects.filter(facility=self).count()
        if approvals:
            return True
        else:
            False

    def __unicode__(self):
        return self.name

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'facilities'


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


@reversion.register
class FacilityApproval(AbstractBase):
    """
    Before a facility is visible to the public it is first approved
    at the county level.
    The user who approves a facility will be the same as the created_by field.
    """
    facility = models.ForeignKey(Facility)
    comment = models.TextField()

    def __unicode__(self):
        return "{}: {}".format(self.facility, self.created_by)


@reversion.register
class FacilityUnit(AbstractBase):
    """
    Autonomous units within a facility that are regulated differently from the
    facility.

    For example AKUH  is a facility and licenced by KMPDB.
    In AKUH there are other units such as its pharmacy which is licensed by
    PPB.
    The pharmacy will in this case be treated as a facilty unit.
    """
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField(
        help_text='A short summary of the facility unit.')

    def __unicode__(self):
        return self.facility.name + ": " + self.name


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

    class Meta(AbstractBase.Meta):
        verbose_name_plural = 'service categories'


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
        help_text="The classification that the service lies in.")

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


class ServiceOption(AbstractBase):
    """
    One service can have multiple options to be selected
    this is for defining the available choices for a service.
    """
    service = models.ForeignKey(Service)
    option = models.ForeignKey(Option)

    def __unicode__(self):
        return "{}: {}".format(self.service, self.option)


class FacilityService(AbstractBase):
    """
    A facility can have zero or more services.
    """
    facility = models.ForeignKey(Facility)
    selected_option = models.ForeignKey(ServiceOption)
    is_confirmed = models.BooleanField(
        default=False,
        help_text='Indiates whether a service has been approved by the CHRIO')
    is_cancelled = models.BooleanField(
        default=False,
        help_text='Indicates whether a service has been cancelled by the '
        'CHRIO')

    def __unicode__(self):
        return "{}: {}".format(self.facility, self.selected_option)


class ServiceRating(AbstractBase):
    """
    The scale for rating the facility service.
    """
    facility_service = models.ForeignKey(FacilityService)
    cleanliness = models.BooleanField(default=True)
    attitude = models.BooleanField(default=True)
    will_return = models.BooleanField(default=True)
    occupation = models.CharField(max_length=100)
    comment = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{}: {}".format(self.facility_service, self.created_by)
