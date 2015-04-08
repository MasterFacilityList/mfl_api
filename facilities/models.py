import random
from django.db import models
from common.models import AbstractBase, SubCounty, Contact


class OwnerTypes(AbstractBase):
    """
    Sub divisions of owners of facilities.

    Owners of facilities could be classified into several categories.
    E.g we could have individual owners, corporate owners, faith based owners
    private owners.
    """

    name = models.CharField(
        max_length=100,
        help_text="Short unique name for a particular type of owners. "
        "e.g INDIVIDUAL")
    description = models.TextField(
        null=True, blank=True,
        help_text="A brief summary of the particular type of owner.")


class Owner(AbstractBase):
    """
    Entity that has exclusive legal rights to the facility.

    For the master facility list, ownership especially for the faith-based
    facilities will be broadened to also include the body that coordinates
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
        "Could be up to 7 characteres long.")
    abbreviation = models.CharField(
        max_length=10, null=True, blank=True,
        help_text="Short form of the name of the owner e.g Ministry of health"
        " could be shortened as MOH")
    owner_type = models.ForeignKey(
        OwnerTypes,
        help_text="The classification of the owner e.g INDIVIDUAL")

    def __unicode__(self):
        return self.name

    def generate_code(self):
        return "{}{}".format("OWNER", str(self.id))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super(Owner, self).save(*args, **kwargs)


class Service(AbstractBase):
    """
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    def generate_code(self):
        return "{}{}".format(self.name, str(self.id))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super(Service, self).save(*args, **kwargs)


class FacilityStatus(AbstractBase):
    """
    Facility Operational Status covers the following elements:
    whether the facility
        1. has been approved to operate
        2. is operating
        3. is temporarily non-operational
        4. is closed down.
    """

    name = models.CharField(max_length=100, unique=True)

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
        help_text="The name of the regulatin body")
    abbreviation = models.CharField(
        max_length=10, null=True, blank=True,
        help_text="A shortform of the name of the regulating body e.g Nursing"
        "Council of Kenya could be abbreviated as NCK.")

    def __unicode__(self):
        return self.name


class RegulationStatus(AbstractBase):
    """
    Indicates whether the facililty has been approved.

    The rulation states could be
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
            known as „pending gazettement‟.
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
        help_text='A sequential number allocated to each facility')
    description = models.TextField(help_text="A brief summary of the Facility")
    regulating_body = models.ForeignKey(
        RegulatingBody, null=True, blank=True,
        help_text="The National Regulatory Body responsible for licensing"
        " or gazettement of the facility")
    facility_type = models.OneToOneField(
        FacilityType,
        help_text="This depends on who owns the facilty. For MOH facilities,"
        "type is the gazetted classification of the facilty."
        "For Non-MOH check under the respective owners.")
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
        " respective National Regulatory Body.")
    sub_county = models.ForeignKey(SubCounty)
    owner = models.ForeignKey(Owner)

    def generate_code(self):
        random_number = random.randint(10000, 1000000)
        try:
            self.__class__.objects.get(code=random_number)
            self.generate_code()
        except:
            return random_number

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Facilities'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super(Service, self).save(*args, **kwargs)


class FacitlityGIS(AbstractBase):
    """
    """

    facility = models.OneToOneField(Facility)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    is_classified = models.BooleanField(default=False)

    def __unicode___(self):
        return self.facility.name


class FacilityService(AbstractBase):
    """
    """

    facility = models.ForeignKey(Facility, related_name='facility_services')
    service = models.ForeignKey(Service)

    def __unicode__(self):
        return "{}::{}".format(self.facility.name, self.service.name)


class FacilityContact(AbstractBase):
    """
    """

    facility = models.ForeignKey(Facility)
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return "{}::{}::{}".format(
            self.facility.name, self.contact.contact_type,
            str(self.contact.id))
