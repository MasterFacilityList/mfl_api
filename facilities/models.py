from django.db import models
from common.models import AbstractBase, SubCounty, Contact
from common.sequence_helper import next_value_in_sequence


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


class Owner(AbstractBase):
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
    code = models.CharField(
        max_length=100, unique=True,
        help_text="A unique number to identify the owner."
        "Could be up to 7 characteres long.", editable=False)
    abbreviation = models.CharField(
        max_length=10, null=True, blank=True,
        help_text="Short form of the name of the owner e.g Ministry of health"
        " could be shortened as MOH")
    owner_type = models.ForeignKey(
        OwnerType,
        help_text="The classification of the owner e.g INDIVIDUAL",
        on_delete=models.PROTECT)

    def get_code_value(self):
        value = next_value_in_sequence("owner_code_seq")
        return value

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code_value()
        super(Owner, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


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
        help_text="A short summary of the job title")

    def __unicode__(self):
        return self.name


class OfficerIncharge(AbstractBase):
    """
     Identify the officer in-charge of a facility.
    """

    name = models.CharField(
        max_length=150,
        help_text="the name of the officer in-charge e.g Roselyne Wiyanga ")
    job_title = models.ForeignKey(JobTitle, on_delete=models.PROTECT)
    registration_number = models.CharField(
        max_length=100,
        help_text="This is the licence number of the officer. e.g for a nurse"
        " use the NCK registration number.")

    def __unicode__(self):
        return self.name


class OfficerIchargeContact(AbstractBase):
    """
    The contact details of the officer incharge.

    The officer incharge may have as many mobile numbers as possible.
    Also the number of email addresses is not limited.
    """

    officer = models.ForeignKey(
        OfficerIncharge,
        help_text="The is the officer in charge", on_delete=models.PROTECT)
    contact = models.ForeignKey(
        Contact,
        help_text="The contact of the officer incharge may it be email, "
        " mobile number etc", on_delete=models.PROTECT)

    def __unicode__(self):
        return "{}: {}".format(self.officer.name, self.contact.contact)


class ServiceCategory(AbstractBase):
    """
    Categorisation of health services.

    The categorisation of services could either be:
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

    name = models.CharField(
        max_length=100,
        help_text="What is the name of the category? ")

    def __unicode__(self):
        return self.name


class Service(AbstractBase):
    """
    A health service.

    The definition of services has attempted to describe the actual components
    of the services provided, the basic infrastructure required to effectively
    provide the service, and human resource required. For example,
    Comprehensive Dental Services cannot be said to be provided unless there is
    a dental chair with its accessories and a dentist. If any of this is
    missing then the service is not provided. However, some services
    definitions are quite complex and will require involvement of the technical
    person attached to the district to work with the DHRIO in order to collect
    the data. For example, the laboratory equipment may require the presence
    of a District Laboratory Technologist
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=100, unique=True, editable=False)

    def get_code_value(self):
        value = next_value_in_sequence("service_code_seq")
        return value

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code_value()
        super(Service, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


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
        help_text="A short explanation of what the status entails.")

    def __unicode__(self):
        return self.name


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

    class Meta:
        unique_together = ('name', 'sub_division', )


class RegulatingBody(AbstractBase):
    """
    Bodies responsible for licensing or gazettement of facilites.

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
        max_length=10, null=True, blank=True,
        help_text="A shortform of the name of the regulating body e.g Nursing"
        "Council of Kenya could be abbreviated as NCK.")

    def __unicode__(self):
        return self.name


class RegulationStatus(AbstractBase):
    """
    Indicates whether the facililty has been approved.

    The regulation states could be
            A facility that has been recommended by the DHMT but is
            waiting for the license from the National Regulatory Body.

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
    """

    name = models.CharField(
        max_length=100, unique=True,
        help_text="A short unique name representing a state/stage of "
        "regulation e.g. PENDING_OPENING ")
    description = models.TextField(
        help_text="A short description of the regulation state or state e.g"
        "PENDING_OPENING could be descriped as 'waiting for the license to"
        "begin operating' ")

    def __unicode__(self):
        return self.name


class Facility(AbstractBase):
    """
    A health institution in Kenya.

    The health institution considered as facilities include:
    Health Centres, Dispensaries, Hospitals etc.
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text='This is the official name of the facility')
    code = models.CharField(
        max_length=100, unique=True,
        help_text='A sequential number allocated to each facility',
        editable=False)
    description = models.TextField(help_text="A brief summary of the Facility")
    regulating_body = models.ForeignKey(
        RegulatingBody, null=True, blank=True,
        help_text="The National Regulatory Body responsible for licensing"
        " or gazettement of the facility", on_delete=models.PROTECT)
    facility_type = models.OneToOneField(
        FacilityType,
        help_text="This depends on who owns the facilty. For MOH facilities,"
        "type is the gazetted classification of the facilty."
        "For Non-MOH check under the respective owners.",
        on_delete=models.PROTECT)
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
    operation_status = models.OneToOneField(
        FacilityStatus,
        help_text="Indicates whether the facility"
        "has been approved to operate, is operating, is temporarily"
        "non-operational, or is closed down")
    regulation_status = models.ForeignKey(
        RegulationStatus, null=True, blank=True,
        help_text="Indicates whether the facility has been approved by the"
        " respective National Regulatory Body.", on_delete=models.PROTECT)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.PROTECT)
    owner = models.ForeignKey(Owner)
    location_desc = models.TextField(
        help_text="This field allows a more detailed description of how to"
        "locate the facility e.g Joy medical clinic is in Jubilee Plaza"
        "7th Floor")
    is_classified = models.BooleanField(
        default=False,
        help_text="Should the facility be visible to the public?")

    def get_code_value(self):
        value = next_value_in_sequence("facility_code_seq")
        return value

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code_value()
        super(Facility, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Facilities'


class FacilityRegulationStatus(AbstractBase):
    """
    Shows the regulation status of facility.

    It adds the extra reason field that makes it possible to give
    an explanation as to why a facility is in a certain regulation status.
    """

    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    regulation_status = models.ForeignKey(
        RegulationStatus, on_delete=models.PROTECT)
    reason = models.TextField(
        null=True, blank=True,
        help_text="e.g Why has a facility been suspended")

    def __unicode__(self):
        return "{}: {}".format(
            self.facility.name, self.regulation_status.name)


class GeoCodeSource(AbstractBase):
    """
    Where the geo-code came from.

    This is the organization collecting the code.
    For example, DHMT, the Service Availability Mapping survey (SAM),
    Kenya Medical Research Institute (KEMRI), the Regional Center for
    Mapping of Resources for Development (RCMRD), the AIDS, Population
    and Health Integrated Assistance (APHIA) II, or another source.
    It is not the individual who collected the code
    """

    name = models.CharField(
        max_length=100,
        help_text="The name of the collecting organization")
    description = models.TextField(
        help_text="A short summary of the collecting organization",
        null=True, blank=True)
    abbreviation = models.CharField(
        max_length=10, help_text="An acronym of the collecting or e.g SAM")

    def __unicode__(self):
        return self.name


class GeoCodeMethod(AbstractBase):
    """
    Method used to capture the geo-code.

    Examples:
        1= Taken with GPS device,
        2= Calculated from proximity to school, village, markets
        3= Calculated from 1:50,000 scale topographic maps,
        4= Scanned from hand-drawn maps,
        5= Centroid calculation from sub-location
        8= No geo-code
        9= Other
    """

    name = models.CharField(
        max_length=100, help_text="The name of the method.")
    description = models.TextField(
        help_text="A short description of the method",
        null=True, blank=True)

    def __unicode__(self):
        return self.name


class FacilityGPS(AbstractBase):
    """
    Location derived by the use of GPS satellites and GPS device or receivers.

    It it three dimensional.
    The three-dimensional readings from a GPS device are latitude, longitude,
    and attitude. The date/time the reading is done is also important, as
    is the source and method of the reading.
    """

    facility = models.OneToOneField(Facility)
    latitude = models.CharField(
        max_length=255,
        help_text="How far north or south a facility is from the equator")
    longitude = models.CharField(
        max_length=255,
        help_text="How far east or west one a facility is from the Greenwich"
        " Meridian")
    source = models.ForeignKey(
        GeoCodeSource,
        help_text="where the geo code came from", on_delete=models.PROTECT)
    method = models.ForeignKey(
        GeoCodeMethod,
        help_text="Method used to obtain the geo codes. e.g"
        " taken with GPS device")

    def __unicode__(self):
        return self.facility.name


class FacilityService(AbstractBase):
    """
    Service offered in a facility.

    Service is either offered all or none, i.e. they exist or do not exist.
    (YES/NO)
    """

    facility = models.ForeignKey(
        Facility, related_name='facility_services', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    service_active = models.BooleanField(
        default=True, help_text="Is the service still being offered or not.")

    def __unicode__(self):
        return "{}: {}".format(self.facility.name, self.service.name)


class FacilityContact(AbstractBase):
    """
    The facility contact.

    The facility contacts could be as many as the facility has.
    They also could be of as many different types as the facility has;
    they could be emails, phone numbers, land lines etc.
    """

    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)

    def __unicode__(self):
        return "{}: {}".format(
            self.facility.name, self.contact.contact)
