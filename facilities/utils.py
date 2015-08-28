import json
import uuid

from django.utils import timezone

from common.models import Contact, ContactType
from common.serializers import ContactSerializer

from facilities.models import (
    FacilityContact,
    Service,
    RegulatingBody,
)

from facilities.serializers import (
    FacilityUnitSerializer,
    FacilityServiceSerializer,
    FacilityContactSerializer
)


inlining_errors = []


def _is_valid_uuid(field):
    try:
        uuid.UUID(field)
        return True
    except ValueError:
        return False


def _validate_services(services):
    errors = []
    for service in services:
        if not _is_valid_uuid(service.get('service', None)):
            return errors.append("Service has a badly formed uuid")
        try:
            Service.objects.get(id=service.get('service'))
        except Service.DoesNotExist:
            errors.append("service with id {} not found".format(
                service.get('service')))
        except KeyError:
            errors.append("Key service was not found")

    return errors


def _validate_units(units):
    errors = []
    for unit in units:
        if not _is_valid_uuid(unit.get('regulating_body', None)):
            return errors.append("Regulating body has a badly formed uuid")
        try:
            RegulatingBody.objects.get(id=unit.get('regulating_body'))
        except RegulatingBody.DoesNotExist:
            errors.append(
                "The regulating_body with the id {} was not "
                "found".format(unit.get("regulating_body")))
        except KeyError:
            errors.append(
                "Key regulating_body is missing")

    return errors


def _validate_contacts(contacts):
    errors = []
    for contact in contacts:
        if not _is_valid_uuid(contact.get('contact_type', None)):
            return errors.append("Contact has a badly formed uuid")
        try:
            ContactType.objects.get(id=contact.get('contact_type'))
        except ContactType.DoesNotExist:
            errors.append("Contact type with the id {} was not found".format(
                contact))
        except KeyError:
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
