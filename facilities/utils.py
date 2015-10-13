"""
Module containing useful functions for validating a facility's in-lined and
many to many attributes before they are saved
"""

import json
import uuid

from django.utils import timezone

from common.models import Contact, ContactType
from common.serializers import ContactSerializer

from facilities.models import (
    FacilityContact,
    Service,
    FacilityDepartment,
    Facility,
    FacilityOfficer,
    JobTitle,
    Officer,
    OfficerContact,
    FacilityUnit
)


inlining_errors = []


def _is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except (ValueError, TypeError):
        return False


def _validate_services(services):
    errors = []
    for service in services:
        if not _is_valid_uuid(service.get('service', None)):
            errors.append("Service has a badly formed uuid")
            return errors
        try:
            Service.objects.get(id=service['service'])
        except (ValueError, TypeError, KeyError, Service.DoesNotExist):
            errors.append("service with id {} not found".format(
                service.get('service')))

    return errors


def _validate_units(units):
    errors = []
    for unit in units:
        if not _is_valid_uuid(unit.get('unit', None)):
            errors.append("Please provide a proper facility department")
            return errors
        try:
            FacilityDepartment.objects.get(id=unit.get('unit'))
        except FacilityDepartment.DoesNotExist:
            errors.append("The facility department provided does not exist")

    return errors


def _validate_contacts(contacts):
    errors = []
    for contact in contacts:
        if not _is_valid_uuid(contact.get('contact_type', None)):
            errors.append("Contact has a badly formed uuid")
        try:
            ContactType.objects.get(id=contact.get('contact_type'))
        except ContactType.DoesNotExist:
            errors.append("Contact type with the id {} was not found".format(
                contact))
        except (KeyError, ValueError, TypeError):
            errors.append("Key contact type is missing")
        if contact.get('contact') is None:
            errors.append("The contact field is missing")

    return errors


def inject_audit_fields(dict_a, validated_data):
    audit_data = {
        "created_by": validated_data['created_by'],
        "updated_by": validated_data['updated_by'],
        "created": (
            validated_data['created'] if
            validated_data.get('created') else timezone.now()),
        "updated": (
            validated_data['updated'] if
            validated_data.get('updated') else timezone.now())
    }
    dict_a.update(audit_data)
    return dict_a


def create_contact(contact_data, validated_data):
    try:
        return Contact.objects.get(contact=contact_data["contact"])
    except Contact.DoesNotExist:
        contact_data = inject_audit_fields(contact_data, validated_data)
        contact = ContactSerializer(data=contact_data)
        return contact.save() if contact.is_valid() else \
            inlining_errors.append(json.dumps(contact.errors))


def create_facility_contacts(instance, contact_data, validated_data):
    from facilities.serializers import FacilityContactSerializer
    contact = create_contact(contact_data, validated_data)
    facility_contact_data = {
        "contact": contact.id,
        "facility": instance.id
    }
    facility_contact_data_with_audit = inject_audit_fields(
        facility_contact_data, validated_data)
    try:
        FacilityContact.objects.get(
            contact_id=facility_contact_data.get('contact'),
            facility_id=facility_contact_data.get('facility')
        )
    except FacilityContact.DoesNotExist:
        fac_contact = FacilityContactSerializer(
            data=facility_contact_data_with_audit)
        fac_contact.save() if fac_contact.is_valid() else \
            inlining_errors.append(fac_contact.errors)


def create_facility_units(instance, unit_data, validated_data):
    from facilities.serializers import FacilityUnitSerializer
    unit_data.pop('department_name', None)
    unit_data.pop('regulating_body_name', None)
    unit_data['facility'] = instance.id
    unit_data = inject_audit_fields(unit_data, validated_data)
    try:
        FacilityUnit.objects.get(**unit_data)
    except FacilityUnit.DoesNotExist:
        unit = FacilityUnitSerializer(data=unit_data)
        return unit.save() if unit.is_valid() else inlining_errors.append((
            json.dumps(unit.errors)))


def create_facility_services(instance, service_data, validated_data):
    from facilities.serializers import FacilityServiceSerializer

    service_data['facility'] = instance.id
    service_data = inject_audit_fields(
        service_data, validated_data)
    f_service = FacilityServiceSerializer(data=service_data)
    f_service.save() if f_service.is_valid() else \
        inlining_errors.append(json.dumps(f_service.errors))


class CreateFacilityOfficerMixin(object):

    """Mixin to create facility officers."""

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)
        super(CreateFacilityOfficerMixin, self).__init__(*args, **kwargs)

    def _validate_required_fields(self, data):
        """
        Ensure that the officer's facility, name and title are provided
        """
        errs = {}
        if data.get('facility_id', None) is None:
            errs["facility_id"] = ["Facility is required"]
        if data.get('name', None) is None:
            errs["name"] = ["Name is Required"]
        if data.get('title', None) is None:
            errs["title"] = ["Job title is required"]

        if data.get('reg_no', None) is None:
            errs["registration_number"] = ["Registration Number is required"]

        return errs

    def _validate_facility(self, data):
        """
        Confirm that the provided facility exists
        """
        try:
            Facility.objects.get(id=data.get('facility_id', None))
        except Facility.DoesNotExist:
            error_message = {
                "facility_id": ["Facility provided does not exist"]
            }
            return error_message

    def _validate_job_titles(self, data):
        """
        Confirm that the provided job title exist
        """
        try:
            JobTitle.objects.get(id=data.get('title', None))
        except JobTitle.DoesNotExist:
            error_message = {
                "title": ["Job title provided does not exist"]
            }
            return error_message

    def data_is_valid(self, data):
        errors = [
            self._validate_required_fields(data),
            self._validate_facility(data),
            self._validate_job_titles(data)
        ]
        errors = [error for error in errors if error]
        if errors:
            return errors
        else:
            return True

    def _inject_creating_user(self, attributes_dict):
        attributes_dict['created_by'] = self.user
        attributes_dict['updated_by'] = self.user
        return attributes_dict

    def _create_contacts(self, data):
        contacts = data.get('contacts', [])
        created_contacts = []

        for contact in contacts:
            contact_type = ContactType.objects.get(id=contact.get('type'))
            contact_dict = {
                "contact_type": contact_type,
                "contact": contact.get('contact')
            }
            try:
                created_contacts.append(Contact.objects.get(**contact_dict))
            except Contact.DoesNotExist:
                contact_dict = self._inject_creating_user(contact_dict)
                contact_dict = self._inject_creating_user(contact_dict)
                created_contacts.append(Contact.objects.create(**contact_dict))

        return created_contacts

    def _create_facility_officer(self, data):
        facility = Facility.objects.get(id=data['facility_id'])
        job_title = JobTitle.objects.get(id=data['title'])

        officer_dict = {
            "name": data['name'],
            "job_title": job_title,
        }
        id_no = data.get('id_no', None)
        reg_no = data.get('reg_no', None)
        officer_dict['id_number'] = id_no if id_no else None
        officer_dict['registration_number'] = reg_no if reg_no else None
        officer_dict = self._inject_creating_user(officer_dict)

        try:
            officer = Officer.objects.get(registration_number=reg_no)
            officer.job_title = job_title
            officer.name = data['name']
            officer.save()
            facility_officer = FacilityOfficer.objects.get(
                facility=facility, officer=officer)
        except Officer.DoesNotExist:

            officer = Officer.objects.create(**officer_dict)
            facility_officer_dict = {
                "facility": facility,
                "officer": officer
            }
            facility_officer_dict = self._inject_creating_user(
                facility_officer_dict)
            facility_officer = FacilityOfficer.objects.create(
                **facility_officer_dict)

        # link the officer to the contacts
        created_contacts = self._create_contacts(data)
        for contact in created_contacts:
            contact_dict = {
                "officer": officer,
                "contact": contact
            }
            try:
                OfficerContact.objects.get(**contact_dict)
            except OfficerContact.DoesNotExist:
                contact_dict = self._inject_creating_user(contact_dict)

                OfficerContact.objects.create(**contact_dict)
        return facility_officer

    def create_officer(self, data):
        from facilities.serializers import FacilityOfficerSerializer
        valid_data = self.data_is_valid(data)

        if valid_data is not True:
            return {
                "created": False,
                "detail": valid_data
            }

        facility_officer = self._create_facility_officer(data)
        serialized_officer = FacilityOfficerSerializer(facility_officer).data
        return {
            "created": True,
            "detail": serialized_officer
        }


def _officer_data_is_valid(officer_data):
    create_officer_instance = CreateFacilityOfficerMixin()
    validated_data = create_officer_instance.data_is_valid(officer_data)
    if validated_data is True:
        return True
    else:
        return validated_data


def _create_officer(officer_data, user):
    create_officer_instance = CreateFacilityOfficerMixin(user=user)
    create_officer_instance._create_facility_officer(officer_data)
