from django.db import models
from common.models import AbstractBase, Ward, Contact
from .facility_models import Facility


class PracticeType(AbstractBase):
    """
    The different types of practitioners.

    Practitioners can be of many  types e.g General Practioner, Dentist etc
    """
    name = models.CharField(
        max_length=50,
        help_text='A short name for the practioner type e.g DENTIST',
        unique=True)
    description = models.TextField(
        null=True, blank=True,
        help_text='A description of the practitioner type')

    def __unicode__(self):
        return self.name


class Speciality(AbstractBase):
    """
    The specilization of a pracitioner e.g  Dentist can specialize in
    Endodontics.
    """
    name = models.CharField(
        max_length=50,
        help_text='A short name for the specilization e.g Endodontics')
    practice_type = models.ForeignKey(PracticeType)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'practice_type',)
        verbose_name_plural = 'specialities'


class Qualification(AbstractBase):
    """
    The awards that a practitioner has been accorded.
    e.g M B ch(Moi) 2003
    """
    name = models.CharField(
        max_length=100, unique=True,
        help_text='A name for the Qualification e.ff MBChB(Kampla) 2011')
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class PractitionerQualification(AbstractBase):
    """
    A practitioner can have more than one qualification.
    """
    practitioner = models.ForeignKey('Practitioner')
    qualification = models.ForeignKey(Qualification)

    def __unicode__(self):
        return "{}: {}".format(self.practitioner, self.qualification)


class PractitionerContact(AbstractBase):
    """
    The different contacts that a practitioner has e.g email, phone numbers etc
    """
    practitioner = models.ForeignKey('Practitioner')
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return "{}: {}".format(self.practitioner, self.contact)


class PractitionerFacility(AbstractBase):
    """
    The facilities that a practitioner attends to.

    This also caters for the fact that some practitioner also own facilities.
    """
    practitioner = models.ForeignKey('Practitioner')
    facility = models.ForeignKey(Facility)
    is_owner = models.BooleanField(
        default=False, help_text='Does the practitioner own the facility?')

    def __unicode__(self):
        return "{}: {}".format(self.practitioner, self.facility)

    class Meta:
        verbose_name_plural = 'practitioner_facilities'


class Practitioner(AbstractBase):
    """
    A medical practitioner
    """
    name = models.CharField(max_length=150)
    registration_number = models.CharField(
        max_length=20, unique=True,
        help_text='The registration_number of the practitioner.')
    ward = models.ForeignKey(
        Ward, null=True, blank=True,
        help_text='The ward where the practitioner comes from.')
    qualifications = models.ManyToManyField(
        Qualification, through=PractitionerQualification,
        help_text='Practitioner qualifications')
    contacts = models.ManyToManyField(
        Contact, through=PractitionerContact,
        help_text='Practitioner contacts emails, phone numbers etc.')
    facilities = models.ManyToManyField(
        Facility, through=PractitionerFacility)

    # can the practitioner have more than one speciality?
    speciality = models.ForeignKey(Speciality)

    def __unicode__(self):
        return self.name
