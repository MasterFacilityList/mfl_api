from __future__ import division
import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from model_mommy import mommy

from common.tests.test_models import BaseTestCase
from common.models import (
    Contact,
    Ward,
    ContactType,
    County,
    Constituency,
    Town
)

from ..models import (
    FacilityExportExcelMaterialView,
    OwnerType,
    Owner,
    JobTitle,
    Officer,
    OfficerContact,
    FacilityStatus,
    FacilityType,
    RegulatingBody,
    RegulationStatus,
    Facility,
    FacilityRegulationStatus,
    FacilityContact,
    FacilityUnit,
    FacilityServiceRating,
    ServiceCategory,
    Service,
    FacilityService,
    FacilityApproval,
    FacilityOperationState,
    RegulatingBodyContact,
    Option,
    FacilityOfficer,
    RegulatoryBodyUser,
    FacilityUnitRegulation,
    FacilityUpdates,
    FacilityUpgrade,
    KephLevel,
    OptionGroup,
    FacilityLevelChangeReason,
    FacilityDepartment,
    RegulatorSync
)


class TestRegulatorSync(BaseTestCase):

    def test_save(self):
        county = mommy.make(County, code=1999)
        mommy.make(RegulatorSync, county=county.code)
        self.assertEquals(1, RegulatorSync.objects.count())

    def test_county_exists(self):
        with self.assertRaises(ValidationError):
            mommy.make(RegulatorSync, county="1889759")

    def test_county_name(self):
        county = mommy.make(County, code=1999)
        sync = mommy.make(RegulatorSync, county="1999")
        self.assertEquals(county.name, sync.county_name)

    def test_unicode(self):
        county = mommy.make(County, code=1999)
        sync = mommy.make(
            RegulatorSync,
            name="Clinic ya Musa", county=county.code)
        self.assertEquals("Clinic ya Musa", sync.__str__())

    def test_probable_matches_without_name(self):
        fac_type = mommy.make(FacilityType)
        owner = mommy.make(Owner)
        ward = mommy.make(Ward)
        reg = mommy.make(RegulatingBody)

        for i in ["Test facility", "facility test", "fac tet", "tes t f"]:
            mommy.make(
                Facility, official_name=i, facility_type=fac_type,
                ward=ward, owner=owner, regulatory_body=reg
            )
        mommy.make(
            Facility, official_name="test",
            facility_type=mommy.make(FacilityType),
            ward=ward, owner=owner, regulatory_body=reg
        )
        mommy.make(
            Facility, official_name="test",
            facility_type=fac_type, ward=ward, owner=mommy.make(Owner)
        )
        sync = RegulatorSync(
            owner=owner, facility_type=fac_type,
            county=ward.constituency.county.code, registration_number="342",
            regulatory_body=reg
        )
        matches = sync.probable_matches
        self.assertListEqual(
            sorted([str(i['official_name']) for i in matches]),
            sorted(
                [
                    "Test facility", "facility test",
                    "fac tet", "tes t f", "test"
                ]
            )
        )

    def test_probable_matches_without_mflcode(self):
        fac_type = mommy.make(FacilityType)
        owner = mommy.make(Owner)
        ward = mommy.make(Ward)
        reg = mommy.make(RegulatingBody)

        for i in ["Test facility", "facility test", "fac tst", "tes t f"]:
            mommy.make(
                Facility, official_name=i, facility_type=fac_type,
                ward=ward, owner=owner, regulatory_body=reg
            )
        mommy.make(
            Facility, official_name="test",
            facility_type=mommy.make(FacilityType),
            ward=ward, owner=owner, regulatory_body=reg
        )
        mommy.make(
            Facility, official_name="test",
            facility_type=fac_type, ward=ward, owner=mommy.make(Owner)
        )
        sync = RegulatorSync.objects.create(
            name="test facility", owner=owner, facility_type=fac_type,
            county=ward.constituency.county.code, registration_number="342",
            regulatory_body=reg
        )
        matches = sync.probable_matches
        self.assertListEqual(
            sorted([str(i['official_name']) for i in matches]),
            sorted(["Test facility", "facility test", "test"])
        )

    def test_probable_matches_with_mflcode(self):
        fac_type = mommy.make(FacilityType)
        owner = mommy.make(Owner)
        ward = mommy.make(Ward)
        reg = mommy.make(RegulatingBody)

        for i in ["Test facility", "a facility test", "fac test", "tes t f"]:
            mommy.make(
                Facility, official_name=i, facility_type=fac_type,
                ward=ward, owner=owner, regulatory_body=reg
            )
        mommy.make(
            Facility, official_name="test",
            facility_type=mommy.make(FacilityType),
            ward=ward, owner=owner, regulatory_body=reg
        )
        mommy.make(
            Facility, official_name="test", regulatory_body=reg,
            facility_type=fac_type, ward=ward, owner=mommy.make(Owner)
        )
        mommy.make(
            Facility, official_name="Test di facility", code=1234,
            facility_type=fac_type, ward=ward, owner=mommy.make(Owner)
        )
        sync = RegulatorSync.objects.create(
            name="test facility", owner=owner, facility_type=fac_type,
            county=ward.constituency.county.code, mfl_code=1234,
            regulatory_body=reg, registration_number=290324
        )
        matches = sync.probable_matches
        self.assertListEqual(
            [i['official_name'] for i in matches], ["Test di facility"]
        )

    def test_update_facility(self):
        fac = mommy.make(Facility)
        county = mommy.make(County, code=8923)
        sync = mommy.make(RegulatorSync, county=county.code)
        sync.update_facility(fac)
        fac = Facility.objects.get(id=fac.id)
        sync = RegulatorSync.objects.get(id=sync.id)
        self.assertEqual(fac.registration_number, sync.registration_number)
        self.assertEqual(fac.code, sync.mfl_code)


class TestOptionGroup(BaseTestCase):

    def test_save(self):
        mommy.make(OptionGroup)
        mommy.make(OptionGroup)
        mommy.make(OptionGroup)
        self.assertEquals(3, OptionGroup.objects.count())


class TestFacilityLevelChangeReason(BaseTestCase):

    def test_save(self):
        mommy.make(FacilityLevelChangeReason)
        self.assertEquals(1, FacilityLevelChangeReason.objects.count())


class TestKephLevel(BaseTestCase):

    def test_save(self):
        mommy.make(KephLevel)
        self.assertEquals(1, KephLevel.objects.count())

    def test_filtering_facility_keph_levels(self):
        mommy.make(KephLevel, is_facility_level=False)
        self.assertEquals(0, KephLevel.objects.count())
        self.assertEquals(1, KephLevel.everything.count())

        mommy.make(KephLevel)
        self.assertEquals(1, KephLevel.objects.count())
        self.assertEquals(2, KephLevel.everything.count())


class TestFacilityOperationState(BaseTestCase):

    def test_save(self):
        status = mommy.make(FacilityStatus, name='PENDING_OPENING')
        facility = mommy.make(
            Facility, name='Nai hosi', operation_status=status)
        status_2 = mommy.make(FacilityStatus, name='OPERATIONAL')
        facility_operation_state = mommy.make(
            FacilityOperationState, facility=facility,
            operation_status=status_2)
        self.assertEquals(1, FacilityOperationState.objects.count())
        self.assertEquals(facility_operation_state.facility, facility)


class TestServiceCategory(BaseTestCase):

    def test_service_count_in_category(self):
        category = mommy.make(ServiceCategory)
        mommy.make(Service, category=category)
        self.assertEquals(1, category.services_count)


class TestFacilityService(BaseTestCase):

    def test_unicode(self):
        f = Facility(name='thifitari')
        s = Service(name='savis')
        o = Option(option_type='BOOLEAN', display_text='Yes/No')
        facility_service = FacilityService(facility=f, option=o, service=s)
        self.assertEqual(
            str(facility_service), 'thifitari: savis (BOOLEAN: Yes/No)'
        )
        self.assertEquals('Yes/No', facility_service.option_display_value)
        self.assertEquals('savis', facility_service.service_name)

    def test_number_of_ratings(self):
        service = mommy.make(Service)
        fs = mommy.make(FacilityService, service=service)
        self.assertEquals(0, fs.number_of_ratings)
        service = mommy.make(Service, name="some name")
        fs_2 = mommy.make(FacilityService, service=service)
        mommy.make(FacilityServiceRating, facility_service=fs_2, rating=1)
        mommy.make(FacilityServiceRating, facility_service=fs_2, rating=5)
        mommy.make(FacilityServiceRating, facility_service=fs_2, rating=3)
        self.assertEquals(3, fs_2.number_of_ratings)

    def test_facility_service(self):
        facility = mommy.make(Facility, name='thifitari')
        service_category = mommy.make(ServiceCategory, name='a good service')
        service = mommy.make(Service, name='savis', category=service_category)
        option = mommy.make(
            Option, option_type='BOOLEAN', display_text='Yes/No')
        facility_service = mommy.make(
            FacilityService, facility=facility, service=service, option=option
        )
        self.assertTrue(facility_service.service_has_options)
        expected_data = [
            {
                "id": facility_service.id,
                "service_id": service.id,
                "service_name": service.name,
                "option_name": option.display_text,
                "option": str(option.id),
                "category_name": service_category.name,
                "category_id": service_category.id,
                "average_rating": facility_service.average_rating,
                "number_of_ratings": 0,
                "service_code": service.code
            }
        ]
        self.assertEquals(expected_data, facility.get_facility_services)

    def test_average_rating(self):
        facility1 = mommy.make(Facility)
        service1, service2 = mommy.make(Service), mommy.make(Service)

        fs1, fs2 = (
            mommy.make(
                FacilityService, facility=facility1, service=service1,
            ),
            mommy.make(
                FacilityService, facility=facility1, service=service2
            )
        )
        fs1_ratings = [
            mommy.make(FacilityServiceRating, rating=2, facility_service=fs1),
            mommy.make(FacilityServiceRating, rating=3, facility_service=fs1),
            mommy.make(FacilityServiceRating, rating=4, facility_service=fs1),
        ]
        fs2_ratings = [
            mommy.make(FacilityServiceRating, rating=4, facility_service=fs2),
            mommy.make(FacilityServiceRating, rating=3, facility_service=fs2),
            mommy.make(FacilityServiceRating, rating=4, facility_service=fs2),
        ]

        # add some noise
        facility2 = mommy.make(Facility)
        service3, service4 = mommy.make(Service), mommy.make(Service)

        fs3, fs4 = (
            mommy.make(
                FacilityService, facility=facility2, service=service3
            ),
            mommy.make(
                FacilityService, facility=facility2, service=service4
            )
        )

        mommy.make(FacilityServiceRating, rating=2, facility_service=fs3),
        mommy.make(FacilityServiceRating, rating=3, facility_service=fs3),
        mommy.make(FacilityServiceRating, rating=4, facility_service=fs3),
        mommy.make(FacilityServiceRating, rating=4, facility_service=fs4),
        mommy.make(FacilityServiceRating, rating=3, facility_service=fs4),
        mommy.make(FacilityServiceRating, rating=4, facility_service=fs4),

        # test calculations
        self.assertEqual(
            fs1.average_rating,
            sum([i.rating for i in fs1_ratings]) / len(fs1_ratings)
        )
        self.assertEqual(
            fs2.average_rating,
            sum([i.rating for i in fs2_ratings]) / len(fs2_ratings)
        )
        self.assertEqual(
            facility1.average_rating,
            (fs1.average_rating + fs2.average_rating) / 2
        )

    def test_validate_either_options_or_service_okay(self):
        service = mommy.make(Service)
        fs = mommy.make(FacilityService, service=service)
        self.assertEquals(1, FacilityService.objects.count())
        self.assertFalse(fs.service_has_options)

    def test_get_service_name_from_service(self):
        service = mommy.make(Service, name="service name")
        facility_service = mommy.make(FacilityService, service=service)
        self.assertEquals("service name", facility_service.service_name)

    def test_get_service_name_from_service_options(self):
        service = mommy.make(Service, name="TB Culture")
        option = mommy.make(Option)
        fs = mommy.make(
            FacilityService, option=option, service=service)
        self.assertEquals("TB Culture", fs.service_name)
        self.assertTrue(fs.service_has_options)

    def test_validate_unique_service_or_service_option_with_for_facility(self):
        service = mommy.make(Service, name="TB Culture")
        facility = mommy.make(Facility)
        option = mommy.make(Option)

        # test validation with option
        mommy.make(
            FacilityService, facility=facility, option=option, service=service)
        with self.assertRaises(ValidationError):
            mommy.make(
                FacilityService, facility=facility,
                option=option, service=service)

    def test_delete_service(self):
        service = mommy.make(Service, name="TB Culture")
        facility = mommy.make(Facility)
        option = mommy.make(Option)

        # test validation with option
        fs = mommy.make(
            FacilityService, facility=facility, option=option, service=service)
        fs.delete()


class TestServiceModel(BaseTestCase):

    def test_save_without_code(self):
        mommy.make(Service, name='some name')
        self.assertEquals(1, Service.objects.count())

    def test_save_with_code(self):
        service = mommy.make(Service, code='1341')
        self.assertEquals(1341, service.code)

    def test_service_category_name(self):
        category = mommy.make(ServiceCategory)
        service = mommy.make(Service, category=category)
        self.assertEquals(category.name, service.category_name)


class TestOwnerTypes(BaseTestCase):

    def test_save(self):
        data = {
            "name": "FBO",
            "description": "The the faith based organisation owners"
        }
        data = self.inject_audit_fields(data)
        OwnerType.objects.create(**data)
        self.assertEquals(1, OwnerType.objects.count())


class TestOwnerModel(BaseTestCase):

    def test_save(self):
        owner_type = mommy.make(OwnerType, name="FBO")
        data = {
            "owner_type": owner_type,
            "name": "CHAK",
            "description": "this is some description",
            "abbreviation": "CHAK"
        }
        data = self.inject_audit_fields(data)
        owner = Owner.objects.create(**data)
        self.assertEquals(1, Owner.objects.count())

        owner_with_no_code = mommy.make(Owner, code=None)
        self.assertTrue(owner_with_no_code.code >= 1)

        owner_with_code = mommy.make(Owner, code=679879)
        self.assertTrue(owner_with_code.code >= 1)

        self.assertIsNotNone(owner.code)

    def test_owner_code_sequence(self):
        # make code none so that mommy does not supply it
        owner_1 = mommy.make(Owner, code=None)
        owner_2 = mommy.make(Owner, code=None)
        owner_2_code = int(owner_1.code) + 1
        self.assertEquals(owner_2.code, owner_2_code)


class TestJobTitleModel(BaseTestCase):

    def test_save(self):
        mommy.make(JobTitle)
        self.assertEquals(1, JobTitle.objects.count())


class TestOfficer(BaseTestCase):

    def test_save(self):
        jt = mommy.make(JobTitle, name='Nursing officer incharge')
        data = {
            "name": "Kimani Maruge",
            "registration_number": "78736790",
            "job_title": jt
        }
        data = self.inject_audit_fields(data)
        Officer.objects.create(**data)
        self.assertEquals(1, Officer.objects.count())


class TestOfficerContactModel(BaseTestCase):

    def test_save(self):
        officer = mommy.make(Officer, name='Maruge')
        contact = mommy.make(Contact, contact='maruge@gmail.com')
        data = {
            "officer": officer,
            "contact": contact
        }
        data = self.inject_audit_fields(data)
        contact = OfficerContact.objects.create(**data)
        self.assertEquals(1, OfficerContact.objects.count())


class TestFacilityStatusModel(BaseTestCase):

    def test_save(self):
        data = {
            "name": "OPERATIONAL",
            "description": "The Facility is operating normally"
        }
        data = self.inject_audit_fields(data)
        FacilityStatus.objects.create(**data)


class TestFacilityTypeModel(BaseTestCase):

    def test_save(self):
        data = {
            "name": "Hospital",
            "sub_division": "District Hospital"
        }
        data = self.inject_audit_fields(data)
        FacilityType.objects.create(**data)
        self.assertEquals(1, FacilityType.objects.count())


class TestRegulatingBodyModel(BaseTestCase):

    def test_save(self):
        reg_status = mommy.make(RegulationStatus)
        data = {
            "name": "Director of Medical Services",
            'default_status': reg_status,
            "abbreviation": "DMS",
            "regulation_verb": "Gazette"
        }
        data = self.inject_audit_fields(data)
        RegulatingBody.objects.create(**data)
        self.assertEquals(1, RegulatingBody.objects.count())

    def test_regulating_body_postal_address(self):
        postal = mommy.make(ContactType, name='POSTAL')
        contact = mommy.make(Contact, contact_type=postal)
        regulating_body = mommy.make(RegulatingBody, name='KMPDB')
        mommy.make(
            RegulatingBodyContact, regulating_body=regulating_body,
            contact=contact)
        self.assertEquals(contact, regulating_body.postal_address.contact)
        self.assertIsInstance(regulating_body.contacts, list)


class TestFacility(BaseTestCase):

    def test_save(self):
        facility_type = mommy.make(FacilityType, name="DISPENSARY")
        operation_status = mommy.make(FacilityStatus, name="OPERATIONAL")
        regulating_body = mommy.make(RegulatingBody, name='KMPDB')
        owner = mommy.make(Owner, name="MOH")
        ward = mommy.make(Ward)
        town = mommy.make(Town, name="Kapchorua")
        data = {
            "name": "Forces Memorial",
            "description": "Hospital for the armed forces",
            "facility_type": facility_type,
            "number_of_beds": 100,
            "number_of_cots": 1,
            "open_public_holidays": True,
            "open_weekends": True,
            "open_whole_day": True,
            "operation_status": operation_status,
            "ward": ward,
            "owner": owner,
            "town": town,
            "regulatory_body": regulating_body
        }
        user = mommy.make(get_user_model())
        regulator = mommy.make(RegulatingBody)
        mommy.make(RegulatoryBodyUser, user=user, regulatory_body=regulator)
        data = self.inject_audit_fields(data)
        facility = Facility.objects.create(**data)
        facility_reg_status = mommy.make(
            FacilityRegulationStatus, facility=facility,
            regulating_body=regulating_body,
            created_by=user)
        self.assertEquals(1, Facility.objects.count())

        mommy.make(Facility, code=89778)
        mommy.make(Facility, code=None)

        self.assertIsNotNone(facility.code)
        self.assertEquals(
            facility_reg_status.regulation_status.name,
            facility.current_regulatory_status)

    def test_working_of_facility_code_sequence(self):
        # make code none so that mommy does not supply it
        facility_1 = mommy.make(Facility, code=None)
        facility_2 = mommy.make(Facility, code=None)
        facility_2_code = int(facility_1.code) + 1
        self.assertEquals(int(facility_2.code), facility_2_code)

    def test_facility_not_approved(self):
        facility = mommy.make(Facility)
        self.assertFalse(facility.is_approved)

    def test_facility_approved(self):
        facility = mommy.make(Facility)
        facility_approval = mommy.make(
            FacilityApproval,
            facility=facility,
            comment='It meets all the registration requirements')
        self.assertTrue(facility.is_approved)
        self.assertEquals(facility, facility_approval.facility)
        self.assertEquals(
            facility_approval.comment,
            'It meets all the registration requirements')

    def test_facility_rejection(self):
        facility = mommy.make(Facility)
        mommy.make(
            FacilityApproval, facility=facility, is_cancelled=True)
        self.assertTrue(facility.rejected)

    def test_county(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        facility = mommy.make(Facility, ward=ward)
        self.assertEquals(county.name, facility.county)

    def test_constituency(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        facility = mommy.make(Facility, ward=ward)
        self.assertEquals(constituency.name, facility.constituency)

    def test_operations_status_name(self):
        operation_status = mommy.make(FacilityStatus)
        facility = mommy.make(Facility, operation_status=operation_status)
        self.assertEquals(
            facility.operation_status_name, operation_status.name)

    def test_regulatory_status_name(self):
        facility = mommy.make(Facility)
        user = mommy.make(get_user_model())
        regulator = mommy.make(RegulatingBody)
        mommy.make(RegulatoryBodyUser, user=user, regulatory_body=regulator)
        facility_reg_status = mommy.make(
            FacilityRegulationStatus, facility=facility, created_by=user)
        self.assertEquals(
            facility.current_regulatory_status,
            facility_reg_status.regulation_status.name)

    def test_owner_type_name(self):
        owner_type = mommy.make(OwnerType, name='GAVA')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility = mommy.make(Facility, owner=owner)
        self.assertEquals(owner.name, facility.owner_name)

    def test_owner_name(self):
        owner_type = mommy.make(OwnerType, name='GAVA')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility = mommy.make(Facility, owner=owner)
        self.assertEquals(owner_type.name, facility.owner_type_name)

    def test_facility_type_name(self):
        facility_type = mommy.make(FacilityType, name='District')
        facility = mommy.make(Facility, facility_type=facility_type)
        self.assertEquals(facility.facility_type_name, facility_type.name)

    def test_is_regulated_is_true(self):
        user = mommy.make(get_user_model())
        regulator = mommy.make(RegulatingBody)
        mommy.make(RegulatoryBodyUser, user=user, regulatory_body=regulator)
        facility = mommy.make(Facility)
        mommy.make(
            FacilityRegulationStatus, facility=facility,
            created_by=user)
        self.assertTrue(facility.is_regulated)

    def test_facility_get_properties(self):
        town = mommy.make(Town, name='Londiani')
        county = mommy.make(County, name='Bomet')
        constituency = mommy.make(Constituency, county=county, name='Pokot')
        ward = mommy.make(Ward, name='Chepalungu', constituency=constituency)
        facility = mommy.make(
            Facility, ward=ward, town=town)

        # test county
        self.assertEquals('Bomet', facility.get_county)
        self.assertEquals('Pokot', facility.get_constituency)
        self.assertEquals('Chepalungu', facility.ward_name)

    def test_only_one_facility_updated_till_acknowledged(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        facility.name = 'The name has been changed'
        facility.save()
        with self.assertRaises(ValidationError):
            mommy.make(FacilityUpdates, facility=facility, is_new=True)

    def test_null_coordinates(self):
        facility = mommy.make(Facility)
        self.assertIsNone(facility.coordinates)

    def test_null_lat_long(self):
        fac = mommy.make(Facility)
        self.assertIsNone(fac.lat_long)

    def test_lat_long(self):
        fc = mommy.make_recipe('mfl_gis.tests.facility_coordinates_recipe')
        ans = fc.facility.lat_long
        self.assertIsInstance(ans, list)

    def test_latest_approval(self):
        facility = mommy.make(Facility)
        approval = mommy.make(FacilityApproval, facility=facility)
        self.assertEquals(approval.id, facility.latest_approval.id)

    def test_no_latest_approval(self):
        facility = mommy.make(Facility)
        self.assertIsNone(facility.latest_approval)

    def test_no_update_approval_before_approving_facility(self):
        facility = mommy.make(Facility)
        facility.name = "a good name"
        facility.save()
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertEquals("a good name", facility_refetched.name)

    def test_boundaries(self):
        facility = mommy.make(Facility)
        with self.assertRaises(ObjectDoesNotExist):
            facility.boundaries

    def test_facility_publishing(self):
        facility = mommy.make(Facility, is_published=False)
        mommy.make(FacilityApproval, facility=facility)
        facility.is_published = True
        facility.save()
        facility_retched = Facility.objects.get(id=facility.id)
        self.assertTrue(facility_retched.is_published)
        self.assertEquals(
            0, FacilityUpdates.objects.filter(facility=facility).count())

    def test_save_facility_twice(self):
        facility = mommy.make(Facility, name="name")
        facility.name = "name"
        facility.save()

    def test_facility_official_name_not_given(self):
        facility = mommy.make(Facility)
        self.assertEquals(facility.name, facility.official_name)

    def test_facility_official_name_given(self):
        facility = mommy.make(Facility, official_name='jina official')
        self.assertNotEquals(facility.name, facility.official_name)
        self.assertEquals(facility.official_name, 'jina official')

    def test_service_catalogue_active_true(self):
        operation_status = mommy.make(FacilityStatus, name="OPERATIONAL")
        facility = mommy.make(Facility, operation_status=operation_status)
        self.assertTrue(facility.service_catalogue_active)

    def test_service_catalogue_active_false(self):
        operation_status = mommy.make(FacilityStatus, name="NON OPERATIONAL")
        facility = mommy.make(Facility, operation_status=operation_status)
        self.assertFalse(facility.service_catalogue_active)

    def test_facility_officer_in_charge_none(self):
        facility = mommy.make(Facility)
        self.assertIsNone(facility.officer_in_charge)

    def test_facility_officer_in_charge_without_contacts(self):
        facility = mommy.make(Facility)
        officer = mommy.make(Officer)
        mommy.make(FacilityOfficer, facility=facility, officer=officer)
        self.assertIsNotNone(facility.officer_in_charge)
        expected = {
            "name": officer.name,
            "reg_no": officer.registration_number,
            "id_number": officer.id_number,
            "title": officer.job_title.id,
            "title_name": officer.job_title.name,
            "contacts": []
        }
        self.assertEquals(expected, facility.officer_in_charge)

    def test_facility_officer_incharge_with_contacts(self):
        facility = mommy.make(Facility)
        officer = mommy.make(Officer)
        contact = mommy.make(Contact)
        officer_contact = mommy.make(
            OfficerContact, officer=officer, contact=contact)
        mommy.make(FacilityOfficer, facility=facility, officer=officer)
        self.assertIsNotNone(facility.officer_in_charge)
        expected = {
            "name": officer.name,
            "reg_no": officer.registration_number,
            "id_number": officer.id_number,
            "title": officer.job_title.id,
            "title_name": officer.job_title.name,
            "contacts": [
                {
                    "officer_contact_id": officer_contact.id,
                    "type": contact.contact_type.id,
                    "contact_type_name": contact.contact_type.name,
                    "contact": contact.contact,
                    "contact_id": contact.id
                }
            ]
        }

        self.assertEquals(expected, facility.officer_in_charge)

    def test_closing_facility(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        facility.closed = True
        now = timezone.now()
        facility.closed_date = now
        facility.closing_reason = "A good reason for closing"
        facility.save()
        self.assertEquals(0, FacilityUpdates.objects.count())
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertTrue(facility_refetched.closed)
        self.assertEquals(facility_refetched.closed_date, now)
        self.assertEquals(
            facility_refetched.closing_reason, "A good reason for closing")

    def test_opening_closed_facility(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        facility.closed = True
        now = timezone.now()
        facility.closed_date = now
        facility.closing_reason = "A good reason for closing"
        facility.save()
        self.assertEquals(0, FacilityUpdates.objects.count())
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertTrue(facility_refetched.closed)
        self.assertEquals(facility_refetched.closed_date, now)
        self.assertEquals(
            facility_refetched.closing_reason, "A good reason for closing")

        facility.closed = False
        facility.closing_reason = "A good reason for opening the facility"
        facility.save()

        self.assertEquals(0, FacilityUpdates.objects.count())
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertFalse(facility_refetched.closed)
        self.assertEquals(
            facility_refetched.closing_reason,
            "A good reason for opening the facility")

    def test_facility_latest_approval_or_rejection(self):
        facility = mommy.make(Facility)
        fa = mommy.make(
            FacilityApproval, facility=facility, comment="some reason")
        self.assertEquals(
            {
                "id": str(fa.id),
                "comment": str(fa.comment)
            },
            facility.latest_approval_or_rejection
        )

    def test_facility_latest_approval_or_rejection_none(self):
        facility = mommy.make(Facility)
        self.assertIsNone(
            facility.latest_approval_or_rejection
        )

    def test_facility_is_regulated_false(self):
        facility = mommy.make(Facility)
        self.assertFalse(facility.is_regulated)

    def test_close_facility_closed_date_not_supplied(self):

        """
        Test that a facility closing date is supplied during
        closing a facility if it is not supplied
        """
        facility = mommy.make(Facility)
        facility.closed = True
        facility.save()
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertTrue(facility_refetched.closed)
        self.assertIsNotNone(facility_refetched.closed_date)

    def test_close_facility_invalid_closing_date(self):

        """
        Test that facility's closing date cannot be in the future
        """
        facility = mommy.make(Facility)
        now = timezone.now()
        tomorrow = now + timedelta(days=1)
        facility.closed = True
        facility.closed_date = tomorrow
        with self.assertRaises(ValidationError):
            facility.save()


class TestFacilityContact(BaseTestCase):

    def test_save(self):
        contact_type = mommy.make(ContactType)
        facility = mommy.make(
            Facility, name="Nairobi Hospital")
        contact = mommy.make(
            Contact, contact="075689267", contact_type=contact_type)
        data = {
            "facility": facility,
            "contact": contact
        }
        data = self.inject_audit_fields(data)
        facility_contact = FacilityContact.objects.create(**data)

        expected_data = [
            {
                "id": facility_contact.id,
                "contact_id": contact.id,
                "contact": contact.contact,
                "contact_type_name": contact_type.name
            }
        ]
        self.assertEquals(expected_data, facility.get_facility_contacts)


class TestRegulationStatus(BaseTestCase):

    def test_save(self):
        data = {
            "name": "OPERATIONAL",
            "description": "The facility is operating normally."
        }
        data = self.inject_audit_fields(data)
        RegulationStatus.objects.create(**data)
        self.assertEquals(2, RegulationStatus.objects.count())

    def test_only_one_default_regulation_status(self):
        # the is already a default regulation status from the base class
        with self.assertRaises(ValidationError):
            mommy.make(RegulationStatus, is_default=True)


class TestFacilityRegulationStatus(BaseTestCase):

    def test_save(self):
        user = mommy.make(get_user_model())
        regulator = mommy.make(RegulatingBody)
        mommy.make(RegulatoryBodyUser, user=user, regulatory_body=regulator)
        facility = mommy.make(Facility, name="Nairobi Hospital")
        status = mommy.make(RegulationStatus, name="SUSPENDED")
        regulator = mommy.make(RegulatingBody, name='KMPDB')
        data = {
            "facility": facility,
            "regulation_status": status,
            "reason": "Reports of misconduct by the doctor",
            "regulating_body": regulator,
            "created_by": user
        }
        data = self.inject_audit_fields(data)
        FacilityRegulationStatus.objects.create(**data)
        self.assertEquals(1, FacilityRegulationStatus.objects.count())

    def test_save_regulatory_by_not_provided(self):
        facility = mommy.make(Facility, name="Nairobi Hospital")
        status = mommy.make(RegulationStatus, name="SUSPENDED")
        regulator = mommy.make(RegulatingBody, name='KMPDB')
        data = {
            "facility": facility,
            "regulation_status": status,
            "reason": "Reports of misconduct by the doctor",
            "regulating_body": regulator
        }
        data = self.inject_audit_fields(data)
        FacilityRegulationStatus.objects.create(**data)
        self.assertEquals(1, FacilityRegulationStatus.objects.count())


class TestFacilityUnitModel(BaseTestCase):

    def test_string_representation(self):
        facility = mommy.make(Facility, name='AKUH')
        department = mommy.make(FacilityDepartment, name='some')
        data = {
            "facility": facility,
            "unit": department
        }
        data = self.inject_audit_fields(data)
        facility_unit = FacilityUnit.objects.create(**data)
        self.assertEquals(1, FacilityUnit.objects.count())
        self.assertEquals(str(facility_unit), 'AKUH: some')

    def test_regulation_status(self):
        facility_unit = mommy.make(FacilityUnit)
        reg_status = mommy.make(RegulationStatus)
        obj = mommy.make(
            FacilityUnitRegulation,
            facility_unit=facility_unit, regulation_status=reg_status)
        self.assertEquals(reg_status, obj.regulation_status)

    def test_unique_facility_unit(self):
        facility = mommy.make(Facility)
        department = mommy.make(FacilityDepartment)
        mommy.make(FacilityUnit, unit=department, facility=facility)
        with self.assertRaises(ValidationError):
            mommy.make(FacilityUnit, unit=department, facility=facility)


class TestRegulationStatusModel(BaseTestCase):

    def test_save(self):
        mommy.make(RegulationStatus)
        self.assertEquals(2, RegulationStatus.objects.count())

    def test_validate_only_one_initial_state(self):
        mommy.make(
            RegulationStatus, is_initial_state=True, is_final_state=False)
        with self.assertRaises(ValidationError):
            mommy.make(
                RegulationStatus, is_initial_state=True, is_final_state=False)

    def test_only_one_final_state(self):
        mommy.make(RegulationStatus, is_final_state=True)
        with self.assertRaises(ValidationError):
            mommy.make(RegulationStatus, is_final_state=True)

    def test_previous_state_name(self):
        status = mommy.make(RegulationStatus, is_final_state=True)
        prev_state = mommy.make(RegulationStatus, previous_status=status)
        self.assertEquals(status.name, prev_state.previous_state_name)

    def test_next_state_name(self):
        status = mommy.make(RegulationStatus, is_initial_state=True)
        next_state = mommy.make(RegulationStatus, next_status=status)
        self.assertEquals(status.name, next_state.next_state_name)

    def test_previous_state_name_is_null(self):
        status = mommy.make(RegulationStatus, is_initial_state=True)
        self.assertEquals("", status.previous_state_name)

    def test_next_state_name_is_null(self):
        status = mommy.make(RegulationStatus, is_final_state=True)
        self.assertEquals("", status.next_state_name)


class TestFacilityOfficer(BaseTestCase):

    def test_saving(self):
        mommy.make(FacilityOfficer)
        self.assertEquals(1, FacilityOfficer.objects.count())


class TestRegulatoryBodyUserModel(BaseTestCase):

    def test_saving(self):
        reg_body = mommy.make(RegulatoryBodyUser)
        self.assertEquals(1, RegulatoryBodyUser.objects.count())

        # test the user is a national user
        self.assertTrue(reg_body.user.is_national)

        # test the user is a regulator
        self.assertIsNotNone(reg_body.user.regulator)
        self.assertEquals(reg_body.user.regulator, reg_body.regulatory_body)

    def test_validate_one_user_one_regulator(self):
        user = mommy.make(get_user_model())
        regulatory_body = mommy.make(RegulatingBody)
        mommy.make(
            RegulatoryBodyUser, user=user,
            regulatory_body=regulatory_body, active=True)
        with self.assertRaises(ValidationError):
            mommy.make(
                RegulatoryBodyUser, user=user,
                regulatory_body=regulatory_body, active=True)


class TestFacilityUnitRegulation(BaseTestCase):

    def test_saving(self):
        mommy.make(FacilityUnitRegulation)
        self.assertEquals(1, FacilityUnitRegulation.objects.count())


class TestFacilityUpdates(BaseTestCase):

    def test_saving(self):
        facility = mommy.make(Facility)
        mommy.make(
            FacilityUpdates,
            facility=facility,
            facility_updates=json.dumps(
                [
                    {
                        "actual_value": "Halafu sasa",
                        "display_value": "Halafu sasa",
                        "field_name": "name",
                        "human_field_name": "name"
                    }
                ]
            )
        )
        self.assertEquals(1, FacilityUpdates.objects.count())

    def test_edit_facility_with_fks_with_fields_called_name(self):
        regulatory_body = mommy.make(RegulatingBody)
        regulatory_body_2 = mommy.make(RegulatingBody)
        facility = mommy.make(Facility, regulatory_body=regulatory_body)
        mommy.make(FacilityApproval, facility=facility)
        facility.regulatory_body = regulatory_body_2
        facility.save()
        self.assertEquals(1, FacilityUpdates.objects.count())

    def test_edit_facility_with_fks_with_boolean_fields_false_first(self):
        facility = mommy.make(Facility, is_classified=False)
        mommy.make(FacilityApproval, facility=facility)
        facility.is_classified = True
        facility.save()
        self.assertEquals(1, FacilityUpdates.objects.count())

    def test_edit_facility_with_fks_with_boolean_fields_true_first(self):
        facility = mommy.make(Facility, is_classified=True)
        mommy.make(FacilityApproval, facility=facility)
        facility.is_classified = False
        facility.save()
        self.assertEquals(1, FacilityUpdates.objects.count())

    def test_facility_updates(self):
        original_name = 'Some facility name'
        updated_name = 'The name has been editted'
        town = mommy.make(Town, name="Kirigiti")
        facility = mommy.make(
            Facility,
            name=original_name, town=town,
            id='cafb2fb8-c6a3-419e-a120-8522634ace73')
        mommy.make(FacilityApproval, facility=facility)

        facility.name = updated_name
        facility.town = town
        facility.save()
        self.assertEquals(1, FacilityUpdates.objects.count())
        facility_refetched = Facility.objects.get(
            id='cafb2fb8-c6a3-419e-a120-8522634ace73')
        self.assertEquals(original_name, facility_refetched.name)

        # approve the facility_updates
        facility_update = FacilityUpdates.objects.all()[0]
        facility_update.approved = True
        facility_update.save()
        facility_refetched_2 = Facility.objects.get(
            id='cafb2fb8-c6a3-419e-a120-8522634ace73')
        self.assertEquals(updated_name, facility_refetched_2.name)

    def test_updating_forbidden_fields(self):
        user = mommy.make(get_user_model())
        regulator = mommy.make(RegulatingBody)
        mommy.make(RegulatoryBodyUser, user=user, regulatory_body=regulator)
        facility_type = mommy.make(FacilityType)
        regulation_status = mommy.make(
            FacilityRegulationStatus, created_by=user)
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        facility.regulatory_status = regulation_status
        facility.facility_type = facility_type
        facility.save()
        self.assertEquals(0, FacilityUpdates.objects.count())

    def test_approve_and_cancel_validation(self):
        with self.assertRaises(ValidationError):
            mommy.make(FacilityUpdates, approved=True, cancelled=True)

    def test_facility_updated_json(self):
        update = [
            {
                "actual_value": "Halafu sasa",
                "display_value": "Halafu sasa",
                "field_name": "name",
                "human_field_name": "name"
            }
        ]
        facility_update = mommy.make(
            FacilityUpdates,
            facility_updates=json.dumps(update))
        self.assertIsInstance(
            facility_update.facility_updated_json(), dict)

    def test_update_facility_has_edits(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        self.assertFalse(facility.has_edits)

        facility.name = 'Facility name has been editted'
        facility.save()
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertTrue(facility_refetched.has_edits)

        facility_updates = FacilityUpdates.objects.all()[0]
        facility_updates.approved = True
        facility_updates.save()
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertFalse(facility_refetched.has_edits)

    def test_update_facility_has_edits_cancel_scenario(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        self.assertFalse(facility.has_edits)

        facility.name = 'Facility name has been editted'
        facility.save()
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertTrue(facility_refetched.has_edits)

        facility_updates = FacilityUpdates.objects.all()[0]
        facility_updates.cancelled = True
        facility_updates.save()
        facility_refetched = Facility.objects.get(id=facility.id)
        self.assertFalse(facility_refetched.has_edits)


class TestFacilityUpgrade(BaseTestCase):

    def test_saving(self):
        k = mommy.make(KephLevel)
        facility = mommy.make(Facility, keph_level=k)
        mommy.make(FacilityUpgrade, keph_level=k, facility=facility)
        self.assertEquals(1, FacilityUpgrade.objects.count())

    def test_only_one_facility_upgrade_at_a_time(self):
        keph_level = mommy.make(KephLevel)
        facility = mommy.make(Facility, keph_level=keph_level)
        facility_type = mommy.make(FacilityType)
        facility_type_2 = mommy.make(FacilityType)
        k = mommy.make(KephLevel)
        first_level_change = mommy.make(
            FacilityUpgrade, facility=facility, facility_type=facility_type,
            keph_level=k
        )
        with self.assertRaises(ValidationError):
            mommy.make(
                FacilityUpgrade, facility=facility,
                facility_type=facility_type_2)

        # confirm the first level/type change and there is no error
        # raised during subsequest level /type change

        first_level_change.is_confirmed = True
        first_level_change.save()
        mommy.make(
            FacilityUpgrade, facility=facility,
            facility_type=facility_type_2, keph_level=k
        )

    def test_cancelling(self):
        k = mommy.make(KephLevel)
        facility = mommy.make(Facility, keph_level=k)
        facility_level_change = mommy.make(
            FacilityUpgrade, facility=facility, keph_level=k)
        self.assertEquals(1, FacilityUpgrade.objects.count())
        facility_level_change.is_cancelled = True
        facility_level_change.save()


class TestFacilityMaterializedModel(BaseTestCase):
    def test_query(self):
        self.assertEquals(
            0,
            FacilityExportExcelMaterialView.objects.count()
        )
