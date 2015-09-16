from django.test import TestCase
from model_mommy import mommy

from common.tests import ModelReprMixin
from facilities import models


class TestModelRepr(ModelReprMixin, TestCase):

    def test_keph_level(self):
        self.check_repr(models.KephLevel(name="kl"), "kl")

    def test_owner_type(self):
        self.check_repr(models.OwnerType(name="ownertype"), "ownertype")

    def test_owner(self):
        self.check_repr(mommy.make(models.Owner, name="owner"), "owner")

    def test_job_title(self):
        self.check_repr(mommy.make(models.JobTitle, name="job"), "job")

    def test_officer(self):
        self.check_repr(mommy.make(models.Officer, name="yah"), "yah")

    def test_officer_contact(self):
        of = mommy.make(models.Officer, name="Y")
        ct = models.Contact._meta.get_field(
            "contact_type").related_model.objects.create(name="twirra")
        con = models.Contact.objects.create(contact="@m", contact_type=ct)
        self.check_repr(mommy.make(
            models.OfficerContact, officer=of, contact=con
        ), "Y: (twirra: @m)")

    def test_facility_status(self):
        self.check_repr(mommy.make(models.FacilityStatus, name="yah"), "yah")

    def test_facility_type(self):
        self.check_repr(mommy.make(models.FacilityType, name="yah"), "yah")

    def test_regulating_body(self):
        self.check_repr(mommy.make(models.RegulatingBody, name="yah"), "yah")

    def test_regulating_body_contact(self):
        r = mommy.make(models.RegulatingBody, name="na")
        ct = models.Contact._meta.get_field(
            "contact_type").related_model.objects.create(name="twirra")
        c = models.Contact.objects.create(contact="@m", contact_type=ct)
        self.check_repr(mommy.make(
            models.RegulatingBodyContact, regulating_body=r, contact=c
        ), "na: (twirra: @m)")

    def test_regulating_body_user(self):
        r = mommy.make(models.RegulatingBody, name="na", )
        u = mommy.make(
            models.settings.AUTH_USER_MODEL, first_name="fname",
            last_name="lname"
        )
        self.check_repr(
            models.RegulatoryBodyUser(user=u, regulatory_body=r),
            "na: fname lname"
        )

    def test_regulation_status(self):
        self.check_repr(mommy.make(models.RegulationStatus, name="yah"), "yah")

    def test_facility_regulation_status(self):
        f = mommy.make(models.Facility, name="hhh")
        rs = mommy.make(models.RegulationStatus, name="ok")
        self.check_repr(
            mommy.make(
                models.FacilityRegulationStatus,
                regulation_status=rs, facility=f
            ),
            "hhh: ok"
        )

    def test_facility_contact(self):
        f = mommy.make(models.Facility, name="na")
        ct = models.Contact._meta.get_field(
            "contact_type").related_model.objects.create(name="twirra")
        c = models.Contact.objects.create(contact="@m", contact_type=ct)
        self.check_repr(mommy.make(
            models.FacilityContact, facility=f, contact=c
        ), "na: (twirra: @m)")

    def test_facility(self):
        self.check_repr(mommy.make(models.Facility, name="yah"), "yah")

    def test_facility_updates(self):
        f = mommy.make(models.Facility, name="yah")
        self.check_repr(
            models.FacilityUpdates(
                facility=f, approved=True,
                cancelled=False, facility_updates="{}"
            ),
            "yah: approved"
        )
        self.check_repr(
            models.FacilityUpdates(
                facility=f, approved=False,
                cancelled=False, facility_updates="{}"
            ),
            "yah: pending"
        )
        self.check_repr(
            models.FacilityUpdates(
                facility=f, approved=True,
                cancelled=True, facility_updates="{}"
            ),
            "yah: rejected"
        )
        self.check_repr(
            models.FacilityUpdates(
                facility=f, approved=False,
                cancelled=True, facility_updates="{}"
            ),
            "yah: rejected"
        )

    def test_facility_operation_status(self):
        f = mommy.make(models.Facility, name="ops")
        os = mommy.make(models.FacilityStatus, name="ok")
        self.check_repr(
            mommy.make(
                models.FacilityOperationState, facility=f, operation_status=os
            ),
            "ops: ok"
        )

    def test_facility_level_change_reason(self):
        self.check_repr(
            mommy.make(models.FacilityLevelChangeReason, reason="yah"), "yah"
        )

    def test_facility_upgrade(self):
        f = mommy.make(models.Facility, name="yah")
        ft = mommy.make(models.FacilityType, name="hu")
        r = mommy.make(models.FacilityLevelChangeReason, reason="ha")
        self.check_repr(
            mommy.make(
                models.FacilityUpgrade, facility=f, reason=r, facility_type=ft
            ),
            "yah: hu (ha)"
        )

    def test_facility_approval(self):
        f = mommy.make(models.Facility, name="ah")
        self.check_repr(
            mommy.make(
                models.FacilityApproval, facility=f, is_cancelled=False
            ),
            "ah: approved"
        )

        self.check_repr(
            mommy.make(
                models.FacilityApproval, facility=f, is_cancelled=True
            ),
            "ah: rejected"
        )

    def test_facility_unit_regulation(self):
        f = mommy.make(models.Facility, name="fe")
        department = mommy.make(models.FacilityDepartment, name='jina')
        fu = mommy.make(models.FacilityUnit, unit=department, facility=f)
        rs = mommy.make(models.RegulationStatus, name="ok")
        self.check_repr(
            mommy.make(
                models.FacilityUnitRegulation, facility_unit=fu,
                regulation_status=rs
            ),
            "fe: jina: ok"
        )

    def test_facility_unit(self):
        f = mommy.make(models.Facility, name='io')
        department = mommy.make(models.FacilityDepartment, name='some')
        self.check_repr(
            mommy.make(
                models.FacilityUnit,
                unit=department, facility=f),
            "io: some"
        )

    def test_service_category(self):
        self.check_repr(mommy.make(models.ServiceCategory, name="yah"), "yah")

    def test_option_group(self):
        self.check_repr(mommy.make(models.OptionGroup, name="yah"), "yah")

    def test_option(self):
        self.check_repr(
            mommy.make(
                models.Option, option_type="INTEGER", display_text="yah"
            ),
            "INTEGER: yah"
        )

    def test_service(self):
        self.check_repr(mommy.make(models.Service, name="yah"), "yah")

    def test_facility_service(self):
        f = mommy.make(models.Facility, name="jk")
        s1 = mommy.make(models.Service, name="srv1")
        s2 = mommy.make(models.Service, name="srv2")
        o = mommy.make(models.Option, option_type="INTEGER", display_text="iq")
        self.check_repr(
            mommy.make(models.FacilityService, facility=f, service=s1),
            "jk: srv1"
        )
        self.check_repr(
            mommy.make(
                models.FacilityService, facility=f, service=s2, option=o
            ),
            "jk: srv2 (INTEGER: iq)"
        )

    def test_facility_service_rating(self):
        f = mommy.make(models.Facility, name="jk")
        s1 = mommy.make(models.Service, name="srv1")
        s2 = mommy.make(models.Service, name="srv2")
        o = mommy.make(models.Option, option_type="INTEGER", display_text="iq")
        fs1 = mommy.make(models.FacilityService, facility=f, service=s1)
        fs2 = mommy.make(
            models.FacilityService, facility=f, service=s2, option=o
        )
        self.check_repr(
            mommy.make(
                models.FacilityServiceRating, facility_service=fs1, rating=3
            ),
            "jk: srv1 - 3"
        )
        self.check_repr(
            mommy.make(
                models.FacilityServiceRating, facility_service=fs2, rating=4
            ),
            "jk: srv2 (INTEGER: iq) - 4"
        )

    def test_facility_officer(self):
        f = mommy.make(models.Facility, name="jjj")
        o = mommy.make(models.Officer, name="qqq")
        self.check_repr(
            mommy.make(models.FacilityOfficer, facility=f, officer=o),
            "jjj: qqq"
        )

    def test_facility_department(self):
        self.check_repr(models.FacilityDepartment(name="testing"), "testing")
