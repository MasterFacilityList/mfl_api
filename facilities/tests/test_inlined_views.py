from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import LoginMixin

from common.models import (
    Ward,
    ContactType,
    PhysicalAddress,
    Town)

from ..models import (
    OwnerType,
    Owner,
    FacilityStatus,
    Facility,
    FacilityType,
    Service,
    Option,
    ServiceOption,
    RegulatingBody,
    KephLevel,
    JobTitle,
    FacilityService,
    FacilityContact,
    FacilityUnit
)


class TestInlinedFacilityCreation(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:facilities:facilities_list")
        super(TestInlinedFacilityCreation, self).setUp()

    def test_post_inlined_facility(self):
        ward = mommy.make(Ward)
        town = mommy.make(Town, ward=ward, name="Some name")
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
        facility_officers = [
            {
                "job_title": job_title.id,
                "name": "Kiprotich Kipngeno",
                "registration_number": "NURS189/1990"
            }
        ]
        facility_officers_with_error = [
            {
                "job_title": 41910510,
                "name": "Kiprotich Kipngeno",
                "registration_number": "NURS189/1990"
            }
        ]
        service = mommy.make(Service)
        service_1 = mommy.make(Service)
        service_2 = mommy.make(Service)
        option = mommy.make(Option)
        service_option = mommy.make(
            ServiceOption, service=service_2, option=option)
        facility_services = [
            {
                "service": service.id,
            },
            {
                "service": service_1.id,
            },
            {
                "selected_option": service_option.id,
            }

        ]
        regulating_body = mommy.make(RegulatingBody)
        facility_units = [
            {
                "name": "The Facilities Pharmacy",
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "regulating_body": regulating_body.id
            }
        ],
        facility_units_with_error = [
            {
                "name": "The Facilities Pharmacy",
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "regulating_body": 11561857195
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
            "facility_officers": facility_officers
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, Facility.objects.count())
        self.assertEquals(1, Owner.objects.count())
        self.assertEquals(1, PhysicalAddress.objects.count())

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
            "facility_officers": facility_officers_with_error
        }
        response = self.client.post(self.url, data_with_errors)
        self.assertEquals(400, response.status_code)
        self.assertEquals(1, Facility.objects.count())
        self.assertEquals(1, Owner.objects.count())
        self.assertEquals(1, PhysicalAddress.objects.count())

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
            "facility_officers": facility_officers_with_error
        }

        response = self.client.post(self.url, data_with_errors)
        self.assertEquals(400, response.status_code)
        self.assertEquals(1, Facility.objects.count())
        self.assertEquals(1, Owner.objects.count())
        self.assertEquals(1, PhysicalAddress.objects.count())

    def test_update_inlined_facility(self):
        ward = mommy.make(Ward)
        town = mommy.make(Town, ward=ward, name="Some name")
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
        service_option = mommy.make(
            ServiceOption, service=service_2, option=option)
        facility_services = [
            {
                "service": service.id,
            },
            {
                "service": service_1.id,
            },
            {
                "selected_option": service_option.id,
            }

        ]
        regulating_body = mommy.make(RegulatingBody)
        facility_units = [
            {
                "name": "The Facilities Pharmacy",
                "description": (
                    "This is the Pharmacy belonging to the hospital"),
                "regulating_body": regulating_body.id
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
        self.assertEquals(1, PhysicalAddress.objects.count())
        facility_id = response.data.get("id")
        updating_data = {
            "name": "Facility name editted",
            "contacts": contacts,
            "units": facility_units,
            "services": facility_services,
            "officer_in_charge": officer_in_charge
        }
        url = self.url + "{}/".format(facility_id)
        response = self.client.patch(url, updating_data)
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
                "service": "19811899",
            }

        ]
        data_with_errors = {
            "contacts": contacts_with_error,
            "units": facility_units_with_error,
            "services": facility_services_with_error
        }
        response = self.client.patch(url, data_with_errors)
        self.assertEquals(400, response.status_code)
