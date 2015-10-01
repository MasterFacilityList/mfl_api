from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import LoginMixin

from common.models import (
    Ward,
    ContactType,
    Town,
    Contact)

from ..models import (
    OwnerType,
    Owner,
    FacilityStatus,
    Facility,
    FacilityType,
    Service,
    Option,
    RegulatingBody,
    KephLevel,
    JobTitle,
    FacilityService,
    FacilityContact,
    FacilityUnit,
    FacilityDepartment,
    FacilityOfficer,
    Officer,
    OfficerContact
)


class TestInlinedFacilityCreation(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:facilities:facilities_list")
        super(TestInlinedFacilityCreation, self).setUp()

    def test_post_inlined_facility(self):
        ward = mommy.make(Ward)
        town = mommy.make(Town, name="Some name")
        facility_type = mommy.make(FacilityType)
        operation_status = mommy.make(FacilityStatus)
        regulator = mommy.make(RegulatingBody)
        contact_type = mommy.make(ContactType, name="EMAIL")
        contact_type_2 = mommy.make(ContactType, name="PHONE")
        keph_level = mommy.make(KephLevel)

        contacts = [
            {
                "contact_type": contact_type.id,
                "contact": "mamalucy@gmail.com"
            },
            {
                "contact_type": contact_type_2.id,
                "contact": "0714681919",
            }

        ]
        mommy.make(
            Contact, contact_type=contact_type, contact="x@y.com")
        contacts_with_error = [
            {
                "contact_type": contact_type.id
            },
            {
                "contact_type": contact_type_2.id
            },
            {
                "contact_type": contact_type.id,
                "contact": "x@y.com"
            }

        ]
        physical_address_with_error = {
        }
        physical_address = {
            "town": town.id,
            "nearest_landmark": "It is near the green M-PESA",
            "plot_number": "9080/78/",
            "location_desc": "Along The beast avenue"
        }
        owner_type = mommy.make(OwnerType)
        # owner = mommy.make(Owner, owner_type=owner_type)
        new_owner = {
            "owner_type": owner_type.id,
            "name": "Musa Kamaa",
            "description": "A private owner based in Kiambu",
            "abbreviation": "MK",

        }
        new_owner_2 = {

        }
        job_title = mommy.make(JobTitle)
        officer_in_charge = {
            "name": "Brenda Makena",
            "id_no": "545454545",
            "reg_no": "DEN/90/2000",
            "title": str(job_title.id),
            "contacts": [
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                },
                {
                    "type": str(contact_type.id),
                    "contact": "0823583941"
                }
            ]
        }
        officer_in_charge_with_errors = {
            "name": "Brenda Makena",
            "title": str(job_title.id),
            "contacts": [
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                }
            ]
        }

        service = mommy.make(Service)
        service_1 = mommy.make(Service)
        service_2 = mommy.make(Service)
        option = mommy.make(Option)
        facility_services = [
            {
                "service": service.id,
            },
            {
                "service": service_1.id,
            },
            {
                "option": option.id,
                "service": service_2.id
            }

        ]
        regulating_body = mommy.make(RegulatingBody)
        department = mommy.make(
            FacilityDepartment,
            regulatory_body=regulating_body, name='The lab')
        facility_units = [
            {
                "unit": str(department.id)
            }
        ]
        facility_units_with_error = [
            {
                "name": "The Facilities Pharmacy",

            }
        ]
        data = {
            "name": "First Mama Lucy Medical Clinic",
            "official_name": "First Mama Lucy",
            "abbreviation": "MLMC",
            "description": "This is an awesome hospital",
            "number_of_cots": 100,
            "number_of_beds": 90,
            "open_whole_day": True,
            "open_weekends": True,
            "open_public_holidays": True,
            "facility_type": facility_type.id,
            "ward": ward.id,
            "operation_status": operation_status.id,
            "new_owner": new_owner,
            "location_data": physical_address,
            "regulatory_body": regulator.id,
            "facility_contacts": contacts,
            "keph_level": keph_level.id,
            "units": facility_units,
            "facility_services": facility_services,
            "officer_in_charge": officer_in_charge
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, Facility.objects.count())
        self.assertEquals(1, Owner.objects.count())

        data_with_errors = {
            "name": "Second Mama Lucy Medical Clinic",
            "official_name": "Second Mama Lucy",
            "abbreviation": "MLMC",
            "description": "This is an awesome hospital",
            "number_of_cots": 100,
            "number_of_beds": 90,
            "open_whole_day": True,
            "open_weekends": True,
            "open_public_holidays": True,
            "facility_type": facility_type.id,
            "ward": ward.id,
            "operation_status": operation_status.id,
            "new_owner": new_owner_2,
            "location_data": physical_address_with_error,
            "regulatory_body": regulator.id,
            "facility_contacts": contacts_with_error,
            "keph_level": keph_level.id,
            "units": facility_units_with_error,
            "facility_services": facility_services,
            "officer_in_charge": officer_in_charge_with_errors
        }
        response = self.client.post(self.url, data_with_errors)
        self.assertEquals(400, response.status_code)
        self.assertEquals(1, Facility.objects.count())
        self.assertEquals(1, Owner.objects.count())
        self.assertEquals(1, FacilityOfficer.objects.count())

        data_with_errors = {
            "name": "Another Mama Lucy Medical Clinic",
            "official_name": "Another Mama Lucy",
            "abbreviation": "MLMC",
            "description": "This is an awesome hospital",
            "number_of_cots": 100,
            "number_of_beds": 90,
            "open_whole_day": True,
            "open_weekends": True,
            "open_public_holidays": True,
            "facility_type": facility_type.id,
            "ward": ward.id,
            "operation_status": operation_status.id,
            "new_owner": new_owner,
            "location_data": physical_address_with_error,
            "regulatory_body": regulator.id,
            "facility_contacts": contacts_with_error,
            "keph_level": keph_level.id,
            "units": facility_units_with_error,
            "facility_services": facility_services,
            "officer_in_charge": officer_in_charge_with_errors
        }

        response = self.client.post(self.url, data_with_errors)
        self.assertEquals(400, response.status_code)
        self.assertEquals(1, Facility.objects.count())
        self.assertEquals(1, Owner.objects.count())

    def test_update_inlined_facility(self):
        ward = mommy.make(Ward)
        town = mommy.make(Town, name="Some name")
        facility_type = mommy.make(FacilityType)
        operation_status = mommy.make(FacilityStatus)
        regulator = mommy.make(RegulatingBody)
        contact_type = mommy.make(ContactType, name="EMAIL")
        contact_type_2 = mommy.make(ContactType, name="PHONE")
        keph_level = mommy.make(KephLevel)

        contacts = [
            {
                "contact_type": contact_type.id,
                "contact": "mamalucy@gmail.com"
            },
            {
                "contact_type": contact_type_2.id,
                "contact": "0714681919",
            }

        ]
        contacts_with_error = [
            {
                "contact_type": contact_type.id
            },
            {
                "contact_type": contact_type_2.id
            }

        ]
        physical_address = {
            "town": town.id,
            "nearest_landmark": "It is near the green M-PESA",
            "plot_number": "9080/78/",
            "location_desc": "Along The beast avenue"
        }
        owner_type = mommy.make(OwnerType)
        # owner = mommy.make(Owner, owner_type=owner_type)
        new_owner = {
            "owner_type": owner_type.id,
            "name": "Musa Kamaa",
            "description": "A private owner based in Kiambu",
            "abbreviation": "MK",

        }
        job_title = mommy.make(JobTitle)

        service = mommy.make(Service)
        service_1 = mommy.make(Service)
        service_2 = mommy.make(Service)
        option = mommy.make(Option)
        facility_services = [
            {
                "service": service.id,
            },
            {
                "service": service_1.id,
            },
            {
                "option": option.id,
                "service": service_2.id
            }

        ]
        regulating_body = mommy.make(RegulatingBody)
        department = mommy.make(
            FacilityDepartment,
            regulatory_body=regulating_body, name='Kapharmacy')
        facility_units = [
            {
                "unit": str(department.id)

            }
        ]
        officer_in_charge = {
            "name": "Brenda Makena",
            "id_no": "545454545",
            "reg_no": "DEN/90/2000",
            "title": str(job_title.id),
            "contacts": [
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                },
                {
                    "type": str(contact_type.id),
                    "contact": "0823583941"
                }
            ]
        }
        officer_in_charge_with_errors = {
            "name": "Brenda Makena",
            "contacts": [
                {
                    "type": str(contact_type.id),
                    "contact": "08235839"
                }
            ]
        }

        data = {
            "name": "First Mama Lucy Medical Clinic",
            "official_name": "First Mama Lucy",
            "abbreviation": "MLMC",
            "description": "This is an awesome hospital",
            "number_of_cots": 100,
            "number_of_beds": 90,
            "open_whole_day": True,
            "open_weekends": True,
            "open_public_holidays": True,
            "facility_type": facility_type.id,
            "ward": ward.id,
            "operation_status": operation_status.id,
            "new_owner": new_owner,
            "location_data": physical_address,
            "regulatory_body": regulator.id,
            "contacts": contacts,
            "keph_level": keph_level.id,
            "units": facility_units,
            "facility_services": facility_services
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, Facility.objects.count())
        self.assertEquals(1, Owner.objects.count())
        facility_id = response.data.get("id")

        updating_data_1 = {
            "name": "Facility name editted"
        }
        updating_data_2 = {
            "contacts": contacts
        }
        updating_data_3 = {
            "units": facility_units
        }
        updating_data_4 = {
            "services": facility_services
        }
        updating_data_5 = {
            "officer_in_charge": officer_in_charge
        }
        url = self.url + "{}/".format(facility_id)
        response = self.client.patch(url, updating_data_1)
        self.assertEquals(200, response.status_code)
        response = self.client.patch(url, updating_data_2)
        self.assertEquals(200, response.status_code)
        response = self.client.patch(url, updating_data_3)
        self.assertEquals(200, response.status_code)
        response = self.client.patch(url, updating_data_4)
        self.assertEquals(200, response.status_code)
        response = self.client.patch(url, updating_data_5)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, FacilityContact.objects.count())
        self.assertEquals(1, FacilityUnit.objects.count())
        self.assertEquals(3, FacilityService.objects.count())
        self.assertEquals(2, FacilityContact.objects.count())

        facility_units_with_error = [
            {
                "name": ("A very long nameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                         "ee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                         "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                         "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                         "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                         "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"),
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "regulating_body": regulating_body.id
            }
        ]
        facility_services_with_error = [
            {
                "service": "4db387fe-27da-46a9-8761-644889713acd",
            }

        ]
        data_with_errors_1 = {
            "contacts": contacts_with_error
        }
        data_with_errors_2 = {
            "units": facility_units_with_error
        }
        data_with_errors_3 = {
            "services": facility_services_with_error
        }
        data_with_errors_4 = {
            "officer_in_charge": officer_in_charge_with_errors
        }
        response = self.client.patch(url, data_with_errors_1)
        self.assertEquals(400, response.status_code)
        response = self.client.patch(url, data_with_errors_2)
        self.assertEquals(400, response.status_code)
        response = self.client.patch(url, data_with_errors_3)
        self.assertEquals(400, response.status_code)

        response = self.client.patch(url, data_with_errors_4)
        self.assertEquals(400, response.status_code)

    def test_update_facility_units(self):
        facility = mommy.make(Facility)
        department = mommy.make(FacilityDepartment)
        units = [
            {
                "unit": str(department.id)
            }
        ]
        url = reverse("api:facilities:facilities_list")
        url = url + "{}/".format(facility.id)
        data = {
            "units": units
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        response_2 = self.client.patch(url, data)
        self.assertEquals(400, response_2.status_code)

    def test_update_facility_units_badly_formed_uuid(self):
        facility = mommy.make(Facility)
        units = [
            {
                "unit": None
            }
        ]
        url = reverse("api:facilities:facilities_list")
        url = url + "{}/".format(facility.id)
        data = {
            "units": units
        }
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)

    def test_update_facility_unit_does_not_exist(self):
        facility = mommy.make(Facility)
        units = [
            {
                "unit": "8e502606-1db3-47c2-94c2-8aea5dd6649e"
            }
        ]
        url = reverse("api:facilities:facilities_list")
        url = url + "{}/".format(facility.id)
        data = {
            "units": units
        }
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)


class TestFacilityContacts(LoginMixin, APITestCase):
    def test_saving_inlined_contacts(self):
        facility = mommy.make(Facility)
        contact_type = mommy.make(ContactType)
        contact_type_2 = mommy.make(ContactType)
        contacts = [
            {
                "contact_type": str(contact_type.id),
                "contact": "20358"
            },
            {
                "contact_type": str(contact_type_2.id),
                "contact": "long contact" * 400
            }
        ]
        data = {
            "contacts": contacts
        }
        url = reverse(
            "api:facilities:facilities_list")
        url = url + "{}/".format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)


class TestFacilityOfficerCreationAndUpdating(LoginMixin, APITestCase):
    def test_save_and_update_facility_officer(self):
        facility = mommy.make(Facility)
        job_title = mommy.make(JobTitle)
        contact_type_1 = mommy.make(ContactType)
        contact_type_2 = mommy.make(ContactType)
        officer_in_charge = {
            "name": "Kishina Kibibi",
            "reg_no": "P15/2010",
            "title": str(job_title.id),
            "contacts": [
                {
                    "type": str(contact_type_1.id),
                    "contact": "08235839"
                },
                {
                    "type": str(contact_type_2.id),
                    "contact": "0823583941"
                }
            ]
        }
        data = {
            "officer_in_charge": officer_in_charge
        }
        url = reverse("api:facilities:facilities_list")
        url = url + '{}/'.format(facility.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, Officer.objects.count())
        self.assertEquals(1, FacilityOfficer.objects.count())
        self.assertEquals(2, OfficerContact.objects.count())

        officer_in_charge_updated = {
            "name": "Kishina Kibibi Updatedi",
            "reg_no": "P15/2010",
            "title": str(job_title.id),
            "contacts": [
                {
                    "type": str(contact_type_1.id),
                    "contact": "08235839"
                },
                {
                    "type": str(contact_type_2.id),
                    "contact": "0823583941"
                },
                {
                    "type": str(contact_type_2.id),
                    "contact": "020-13957857"
                }
            ]
        }
        data = {
            "officer_in_charge": officer_in_charge_updated
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, Officer.objects.count())
        self.assertEquals(1, FacilityOfficer.objects.count())
        self.assertEquals(3, OfficerContact.objects.count())
        officer = Officer.objects.all()[0]
        self.assertEquals(officer_in_charge_updated.get('name'), officer.name)
