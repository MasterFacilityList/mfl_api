import json

from django.utils import timezone

from common.models import Contact, ContactType
from common.serializers import ContactSerializer

from facilities.models import (
    FacilityContact,
    Facility,
    FacilityOfficer,
    JobTitle,
    Officer,
    OfficerContact)

from facilities.serializers import (
    FacilityUnitSerializer,
    FacilityServiceSerializer,
    FacilityOfficerSerializer,
    FacilityContactSerializer
)


inlining_errors = []


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
            Contact.objects.get(contact=contact_data["contact"])
        except Contact.DoesNotExist:
            contact_data = inject_audit_fields(contact_data, validated_data)
            contact = ContactSerializer(data=contact_data)
            return contact.save() if contact.is_valid() else \
                inlining_errors.append(json.dumps(contact.errors))
        except KeyError:
            inlining_errors.append(
                {"contact": ["Contact was not supplied"]})


def create_facility_contacts(instance, contact_data, validated_data):
        contact = create_contact(contact_data, validated_data)
        if contact:
            facility_contact_data = {
                "contact": contact.id,
                "facility": instance.id
            }
            facility_contact_data_with_audit = inject_audit_fields(
                facility_contact_data, validated_data)
            try:
                FacilityContact.objects.get(**facility_contact_data)
            except FacilityContact.DoesNotExist:
                fac_contact = FacilityContactSerializer(
                    data=facility_contact_data_with_audit)
                if fac_contact.is_valid():
                    fac_contact.save()
                else:
                    inlining_errors.append(fac_contact.errors)
                # FacilityContact.objects.create(
                #     **facility_contact_data_with_audit)


def create_facility_units(instance, unit_data, validated_data):
        unit_data['facility'] = instance.id
        unit_data = inject_audit_fields(unit_data, validated_data)
        unit = FacilityUnitSerializer(data=unit_data)
        if unit.is_valid():
            return unit.save()
        else:
            inlining_errors.append((json.dumps(unit.errors)))


def create_facility_services(instance, service_data, validated_data):
        service_data['facility'] = instance.id
        service_data = inject_audit_fields(
            service_data, validated_data)
        f_service = FacilityServiceSerializer(data=service_data)
        f_service.save() if f_service.is_valid() else \
            inlining_errors.append(json.dumps(f_service.errors))


class CreateFacilityOfficerMixin(object):

    """Mixin to create facility officers."""

    def _validate_required_fields(self, data):
        errs = {}
        if data.get('facility_id', None) is None:
            errs["facility_id"] = ["Facility is required"]
        if data.get('name', None) is None:
            errs["name"] = ["Name is Required"]
        if data.get('title', None) is None:
            errs["title"] = ["Job title is required"]

        return errs

    def _validate_facility(self, data):
        try:
            Facility.objects.get(id=data.get('facility_id', None))
        except Facility.DoesNotExist:
            error_message = {
                "facility_id": ["Facility provided does not exist"]
            }
            return error_message

    def _validate_job_titles(self, data):
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
        officer_dict = self._inject_creating_user(officer_dict)

        id_no = data.get('id_no', None)
        reg_no = data.get('reg_no', None)
        officer_dict['id_number'] = id_no if id_no else None
        officer_dict['registration_number'] = reg_no if reg_no else None

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
            contact_dict = self._inject_creating_user(contact_dict)
            OfficerContact.objects.create(**contact_dict)
        return facility_officer

    def create_officer(self, data):
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
