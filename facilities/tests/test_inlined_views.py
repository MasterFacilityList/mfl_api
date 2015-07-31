import json
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import (
    LoginMixin,
    default
)
from common.models import (
    Ward, UserCounty,
    County,
    Constituency,
    Contact,
    ContactType,
    UserConstituency,
    PhysicalAddress,
    Town)

from ..serializers import (
    OwnerSerializer,
    FacilitySerializer,
    FacilityDetailSerializer,
    FacilityStatusSerializer,
    FacilityUnitSerializer,
    FacilityListSerializer,
    FacilityOfficerSerializer,
    RegulatoryBodyUserSerializer,
    FacilityUnitRegulationSerializer,
    FacilityUpdatesSerializer,
    ServiceSerializer
)
from ..models import (
    OwnerType,
    Owner,
    FacilityStatus,
    Facility,
    FacilityUnit,
    FacilityRegulationStatus,
    FacilityType,
    ServiceCategory,
    Service,
    Option,
    ServiceOption,
    FacilityService,
    FacilityContact,
    FacilityOfficer,
    Officer,
    RegulatingBody,
    RegulatoryBodyUser,
    FacilityUnitRegulation,
    RegulationStatus,
    FacilityApproval,
    FacilityUpdates,
    KephLevel,
    JobTitle
)

from django.contrib.auth.models import Group, Permission


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
        facility_officers = [
            {
                "job_title": job_title.id,
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
        ]
        data = {
            "name": "Mama Lucy Medical Clinic",
            "official_name": "Mama Lucy",
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
            "facility_units": facility_units,
            "facility_services": facility_services,
            "facility_officers": facility_officers
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, Facility.objects.count())
        self.assertEquals(1, Owner.objects.count())
        self.assertEquals(1, PhysicalAddress.objects.count())
        self.assertEquals(2, Contact.objects.count())
        self.assertEquals(2, FacilityContact.objects.count())
        self.assertEquals(1, FacilityUnit.objects.count())
        self.assertEquals(1, Officer.objects.count())
        self.assertEquals(1, FacilityOfficer.objects.count())
