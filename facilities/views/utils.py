from common.models import Contact, ContactType


from ..models import (
    Facility,
    OfficerContact,
    FacilityOfficer,
    JobTitle,
    Officer
)

from ..serializers import FacilityOfficerSerializer


class CreateFacilityOfficerHelper(object):
    """
    A custom view for creating facility officers.
    Make it less painful to create facility officers via the frontend.
    """
    def __init__(self, user):
        self.user = user

    def _validate_required_fields(self, data):
        facility_id = data.get('facility_id', None)
        name = data.get('name', None)
        title = data.get('title', None)
        id_number = data.get('id_no', None)
        if not facility_id or not name or not title or not id_number:
            error_message = "Facility id , name, ID number and"\
                            "job title of the officer are "\
                            "required"
            return error_message

    def _validate_facility(self, data):
        try:
            Facility.objects.get(id=data.get('facility_id', None))
        except Facility.DoesNotExist:
            error_message = {
                "facility": "Facility provided does not exist"
            }
            return error_message

    def _validate_job_titles(self, data):
        try:
            JobTitle.objects.get(id=data['title'])
        except JobTitle.DoesNotExist:
            error_message = {
                "job title": "JobTitle with id {} does not exist".format(
                    data['title'])
            }
            return error_message

    def data_is_valid(self, data):
        errors = [
            self._validate_required_fields(data),
            self._validate_facility(data),
            self._validate_job_titles(data)
        ]
        errors = [error for error in errors if error is not None]
        if errors:
            return errors
        else:
            return True

    def _inject_creating_user(self, attributes_dict):
        attributes_dict['created_by'] = self.user
        attributes_dict['updated_by'] = self.user
        return attributes_dict

    def _create_contacts(self, data):
        contacts = data.get('contacts', None)
        created_contacts = []
        if contacts:
            for contact in contacts:

                contact_type = ContactType.objects.get(
                    id=contact.get('type'))
                contact_dict = {
                    "contact_type": contact_type,
                    "contact": contact.get('contact')
                }
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
        else:
            facility_officer = self._create_facility_officer(data)
            serialized_officer = FacilityOfficerSerializer(
                facility_officer).data
            return {
                "created": True,
                "detail": serialized_officer
            }
