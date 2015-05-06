from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from model_mommy import mommy

from common.tests.test_models import BaseTestCase
from common.models import Contact, Ward, PhysicalAddress, ContactType

from ..models import (
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
    ServiceCategory,
    Service,
    ServiceOption,
    FacilityService,
    FacilityApproval,
    FacilityOperationState,
    FacilityUpgrade,
    RegulatingBodyContact,
    Option,
    ServiceRating
)


class TestFacilityUpgrade(BaseTestCase):
    def test_upgrade_moh_facility_correctly(self):
        owner_type = mommy.make(OwnerType, name='MOH')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility_type = mommy.make(FacilityType, name='DISPENSARY')
        facility_type_upgrade = mommy.make(FacilityType, name='HEALTH_CENTER')
        facility = mommy.make(
            Facility, name='Mbagathi hosi', facility_type=facility_type,
            owner=owner)

        mommy.make(
            FacilityUpgrade, facility_type=facility_type_upgrade,
            facility=facility)
        self.assertEquals(1, FacilityUpgrade.objects.count())
        facility_refetched = Facility.objects.get(name='Mbagathi hosi')
        self.assertEquals(
            facility_type_upgrade, facility_refetched.facility_type)

    def test_downgrade_moh_facility_correctly(self):
        owner_type = mommy.make(OwnerType, name='MOH')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility_type = mommy.make(FacilityType, name='HEALTH_CENTER')
        facility_type_downgrade = mommy.make(FacilityType, name='DISPENSARY')
        facility = mommy.make(
            Facility, name='Mbagathi hosi', facility_type=facility_type,
            owner=owner)

        mommy.make(
            FacilityUpgrade, facility_type=facility_type_downgrade,
            facility=facility)
        self.assertEquals(1, FacilityUpgrade.objects.count())
        facility_refetched = Facility.objects.get(name='Mbagathi hosi')
        self.assertEquals(
            facility_type_downgrade, facility_refetched.facility_type)

    def test_upgrade_moh_facility_with_error(self):
        owner_type = mommy.make(OwnerType, name='MOH')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility_type = mommy.make(FacilityType, name='DISPENSARY')
        facility_type_upgrade = mommy.make(
            FacilityType,
            name='SUB_DISTRICT_HOSPITAL')
        facility = mommy.make(
            Facility, name='Mbagathi hosi', facility_type=facility_type,
            owner=owner)

        with self.assertRaises(ValidationError):
            mommy.make(
                FacilityUpgrade, facility_type=facility_type_upgrade,
                facility=facility)
        facility_refetched = Facility.objects.get(name='Mbagathi hosi')
        self.assertEquals(
            facility_type, facility_refetched.facility_type)

    def test_upgrade_fbo_facility_correctly(self):
        owner_type = mommy.make(OwnerType, name='FBO')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility_type = mommy.make(FacilityType, name='HEALTH_CENTER')
        facility_type_upgrade = mommy.make(
            FacilityType, name='LOWEST_LEVEL_HOSPITAL')
        facility = mommy.make(
            Facility, name='Mbagathi hosi', facility_type=facility_type,
            owner=owner)

        mommy.make(
            FacilityUpgrade, facility_type=facility_type_upgrade,
            facility=facility)
        self.assertEquals(1, FacilityUpgrade.objects.count())
        facility_refetched = Facility.objects.get(name='Mbagathi hosi')
        self.assertEquals(
            facility_type_upgrade, facility_refetched.facility_type)

    def test_upgrade_fbo_facility_with_error(self):
        owner_type = mommy.make(OwnerType, name='FBO')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility_type = mommy.make(FacilityType, name='DISPENSARY')
        facility_type_upgrade = mommy.make(
            FacilityType,
            name='HIGHER_LEVEL_HOSPITAL')
        facility = mommy.make(
            Facility, name='Mbagathi hosi', facility_type=facility_type,
            owner=owner)

        with self.assertRaises(ValidationError):
            mommy.make(
                FacilityUpgrade, facility_type=facility_type_upgrade,
                facility=facility)
        facility_refetched = Facility.objects.get(name='Mbagathi hosi')
        self.assertEquals(
            facility_type, facility_refetched.facility_type)

    def test_upgrade_private_facility_correctly(self):
        owner_type = mommy.make(OwnerType, name='PRIVATE')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility_type = mommy.make(FacilityType, name='MEDICAL_CENTER')
        facility_type_upgrade = mommy.make(
            FacilityType, name='MATERNITY_HOME')
        facility = mommy.make(
            Facility, name='Mbagathi hosi', facility_type=facility_type,
            owner=owner)

        mommy.make(
            FacilityUpgrade, facility_type=facility_type_upgrade,
            facility=facility)
        self.assertEquals(1, FacilityUpgrade.objects.count())
        facility_refetched = Facility.objects.get(name='Mbagathi hosi')
        self.assertEquals(
            facility_type_upgrade, facility_refetched.facility_type)

    def test_upgrade_private_facility_with_error(self):
        owner_type = mommy.make(OwnerType, name='PRIVATE')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility_type = mommy.make(FacilityType, name='MEDICAL_CENTER')
        facility_type_upgrade = mommy.make(
            FacilityType,
            name='HIGHER_LEVEL_HOSPITAL')
        facility = mommy.make(
            Facility, name='Mbagathi hosi', facility_type=facility_type,
            owner=owner)

        with self.assertRaises(ValidationError):
            mommy.make(
                FacilityUpgrade, facility_type=facility_type_upgrade,
                facility=facility)
        facility_refetched = Facility.objects.get(name='Mbagathi hosi')
        self.assertEquals(
            facility_type, facility_refetched.facility_type)

    def test_upgrade_unkwon_onwer_type(self):
        owner_type = mommy.make(OwnerType, name='FUNKY OWNER')
        owner = mommy.make(Owner, owner_type=owner_type)
        facility_type = mommy.make(FacilityType, name='MEDICAL_CENTER')
        facility_type_upgrade = mommy.make(
            FacilityType,
            name='HIGHER_LEVEL_HOSPITAL')
        facility = mommy.make(
            Facility, name='Mbagathi hosi', facility_type=facility_type,
            owner=owner)

        with self.assertRaises(ValidationError):
            mommy.make(
                FacilityUpgrade, facility_type=facility_type_upgrade,
                facility=facility)
        facility_refetched = Facility.objects.get(name='Mbagathi hosi')
        self.assertEquals(
            facility_type, facility_refetched.facility_type)


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
        facility_refetched = Facility.objects.get(name='Nai hosi')
        self.assertEquals(status_2, facility_refetched.operation_status)

    def test_save_errorneous_transition(self):
        status = mommy.make(FacilityStatus, name='PENDING_OPENING')
        facility = mommy.make(
            Facility, name='Nai hosi', operation_status=status)
        status_2 = mommy.make(FacilityStatus, name='CLOSED')
        with self.assertRaises(ValidationError):
            mommy.make(
                FacilityOperationState, facility=facility,
                operation_status=status_2)


class TestServiceCategory(BaseTestCase):
    def test_unicode(self):
        instance = ServiceCategory(name='test name')
        self.assertEqual(str(instance), 'test name')


class TestOption(BaseTestCase):
    def test_unicode(self):
        instance = Option(option_type='BOOLEAN', display_text='Yes/No')
        self.assertEqual(str(instance), 'BOOLEAN: Yes/No')


class TestServiceOption(BaseTestCase):
    def test_unicode(self):
        service = Service(name='savis')
        option = Option(option_type='BOOLEAN', display_text='Yes/No')
        service_option = ServiceOption(service=service, option=option)
        self.assertEqual(str(service_option), 'savis: BOOLEAN: Yes/No')


class TestFacilityService(BaseTestCase):
    def test_unicode(self):
        facility = Facility(name='thifitari')
        service = Service(name='savis')
        option = Option(option_type='BOOLEAN', display_text='Yes/No')
        service_option = ServiceOption(service=service, option=option)
        facility_service = FacilityService(
            facility=facility, selected_option=service_option)
        self.assertEqual(
            str(facility_service), 'thifitari: savis: BOOLEAN: Yes/No')


class TestServiceRating(BaseTestCase):
    def test_unicode(self):
        service = Service(name='savis')
        facility = Facility(name='thifitari')
        option = Option(option_type='BOOLEAN', display_text='Yes/No')
        service_option = ServiceOption(service=service, option=option)
        facility_service = FacilityService(
            facility=facility, selected_option=service_option)
        service_rating = ServiceRating(
            facility_service=facility_service,
            created_by=mommy.make(get_user_model(), email='yusa@yusas.org')
        )
        self.assertEqual(
            str(service_rating),
            'thifitari: savis: BOOLEAN: Yes/No: yusa@yusas.org')


class TestServiceModel(BaseTestCase):
    def test_save_without_code(self):
        service = mommy.make(Service, name='some name')
        self.assertEquals(1, Service.objects.count())

        # test unicode
        self.assertEquals('some name', service.__unicode__())

    def test_save_with_code(self):
        service = mommy.make(Service, code='1341')
        self.assertEquals(1341, service.code)


class TestOwnerTypes(BaseTestCase):
    def test_save(self):
        data = {
            "name": "FBO",
            "description": "The the faith based organisation owners"
        }
        data = self.inject_audit_fields(data)
        owner_type = OwnerType.objects.create(**data)
        self.assertEquals(1, OwnerType.objects.count())

        # test unicode
        self.assertEquals("FBO", owner_type.__unicode__())


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

        # test unicode
        self.assertEquals("CHAK", owner.__unicode__())
        self.assertIsNotNone(owner.code)

    def test_owner_code_sequence(self):
        # make code none so that mommy does not supply it
        owner_1 = mommy.make(Owner, code=None)
        owner_2 = mommy.make(Owner, code=None)
        owner_2_code = int(owner_1.code) + 1
        self.assertEquals(owner_2.code, owner_2_code)


class TestJobTitleModel(BaseTestCase):
    def test_save(self):
        data = {
            "name": "Nurse officer incharge",
            "description": "some good description"
        }
        data = self.inject_audit_fields(data)
        jt = JobTitle.objects.create(**data)
        self.assertEquals(1, JobTitle.objects.count())

        # test unicode
        self.assertEquals("Nurse officer incharge", jt.__unicode__())


class TestOfficer(BaseTestCase):
    def test_save(self):
        jt = mommy.make(JobTitle, name='Nursing officer incharge')
        data = {
            "name": "Kimani Maruge",
            "registration_number": "78736790",
            "job_title": jt
        }
        data = self.inject_audit_fields(data)
        officer = Officer.objects.create(**data)
        self.assertEquals(1, Officer.objects.count())

        # test unicode
        self.assertEquals("Kimani Maruge", officer.__unicode__())


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

        # test unicode
        expected = "Maruge: maruge@gmail.com"
        self.assertEquals(expected, contact.__unicode__())


class TestFacilityStatusModel(BaseTestCase):
    def test_save(self):
        data = {
            "name": "OPERATIONAL",
            "description": "The Facility is operating normally"
        }
        data = self.inject_audit_fields(data)
        fs = FacilityStatus.objects.create(**data)

        # test unicode
        self.assertEquals('OPERATIONAL', fs.__unicode__())


class TestFacilityTypeModel(BaseTestCase):
    def test_save(self):
        data = {
            "name": "Hospital",
            "sub_division": "District Hospital"
        }
        data = self.inject_audit_fields(data)
        facility_type = FacilityType.objects.create(**data)
        self.assertEquals(1, FacilityType.objects.count())

        # test unicode
        self.assertEquals("Hospital", facility_type.__unicode__())


class TestRegulatingBodyModel(BaseTestCase):
    def test_save(self):
        data = {
            "name": "Director of Medical Services",
            "abbreviation": "DMS"
        }
        data = self.inject_audit_fields(data)
        regulating_body = RegulatingBody.objects.create(**data)
        self.assertEquals(1, RegulatingBody.objects.count())

        # test unicode
        self.assertEquals(
            "Director of Medical Services",
            regulating_body.__unicode__())

    def test_regulating_body_postal_address(self):
        postal = mommy.make(ContactType, name='POSTAL')
        contact = mommy.make(Contact, contact_type=postal)
        regulating_body = mommy.make(RegulatingBody, name='KMPDB')
        mommy.make(
            RegulatingBodyContact, regulating_body=regulating_body,
            contact=contact)
        self.assertEquals(contact, regulating_body.postal_address.contact)


class TestFacility(BaseTestCase):
    def test_save(self):
        facility_type = mommy.make(FacilityType, name="DISPENSARY")
        operation_status = mommy.make(FacilityStatus, name="OPERATIONAL")
        officer_in_charge = mommy.make(Officer, name='Dr Burmuriat')
        regulating_body = mommy.make(RegulatingBody, name='KMPDB')
        owner = mommy.make(Owner, name="MOH")
        ward = mommy.make(Ward)
        address = mommy.make(PhysicalAddress)
        data = {
            "name": "Forces Memorial",
            "description": "Hospital for the armed forces",
            "facility_type": facility_type,
            "number_of_beds": 100,
            "number_of_cots": 1,
            "open_whole_day": True,
            "open_whole_week": True,
            "operation_status": operation_status,
            "ward": ward,
            "owner": owner,
            "location_desc": "it is located along Moi Avenue Nairobi",
            "officer_in_charge": officer_in_charge,
            "physical_address": address
        }
        data = self.inject_audit_fields(data)
        facility = Facility.objects.create(**data)
        facility_reg_status = mommy.make(
            FacilityRegulationStatus, facility=facility,
            regulating_body=regulating_body)
        self.assertEquals(1, Facility.objects.count())

        # Bloody branch misses
        mommy.make(Facility, code=89778)
        mommy.make(Facility, code=None)

        #  test unicode
        self.assertEquals("Forces Memorial", facility.__unicode__())
        self.assertIsNotNone(facility.code)
        self.assertEquals(
            facility_reg_status,
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


class TestFacilityContact(BaseTestCase):
    def test_save(self):
        facility = mommy.make(Facility, name="Nairobi Hospital")
        contact = mommy.make(Contact, contact="075689267")
        data = {
            "facility": facility,
            "contact": contact
        }
        data = self.inject_audit_fields(data)
        facility_contact = FacilityContact.objects.create(**data)

        # test unicode
        expected = "Nairobi Hospital: 075689267"
        self.assertEquals(expected, facility_contact.__unicode__())


class TestRegulationStatus(BaseTestCase):
    def test_save(self):
        data = {
            "name": "OPERATIONAL",
            "description": "The facility is operating normally."
        }
        data = self.inject_audit_fields(data)
        regulation_status = RegulationStatus.objects.create(**data)
        self.assertEquals(1, RegulationStatus.objects.count())

        # test unicode
        self.assertEquals("OPERATIONAL", regulation_status.__unicode__())


class TestFacilityRegulationStatus(BaseTestCase):
    def test_save(self):
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
        facility_reg_status = FacilityRegulationStatus.objects.create(**data)
        self.assertEquals(1, FacilityRegulationStatus.objects.count())

        #  test unicode
        expected = "Nairobi Hospital: SUSPENDED"
        self.assertEquals(expected, facility_reg_status.__unicode__())


class TestFacilityUnitModel(BaseTestCase):

    def test_string_representation(self):
        facility = mommy.make(Facility, name='AKUH')
        data = {
            "facility": facility,
            "name": "Pharmacy",
            "description": "This is the AKUH Pharmacy section."
        }
        data = self.inject_audit_fields(data)
        facility_unit = FacilityUnit.objects.create(**data)
        self.assertEquals(1, FacilityUnit.objects.count())
        self.assertEquals(str(facility_unit), 'AKUH: Pharmacy')
