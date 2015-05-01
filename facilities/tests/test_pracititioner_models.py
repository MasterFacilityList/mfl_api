from django.test import TestCase

from model_mommy import mommy

from ..models import (
    PracticeType,
    Speciality,
    Qualification,
    PractitionerQualification,
    PractitionerContact,
    PractitionerFacility,
    Practitioner,
    ServiceCategory,
    Option,
    Service,
    FacilityService,
    ServiceOption,
    ServiceRating,
    FacilityApproval,
    RegulatingBody,
    RegulatingBodyContact
)


class TestModels(TestCase):
    def test_save(self):
        models = [
            PracticeType, Speciality, Qualification,
            PractitionerQualification, PractitionerContact,
            PractitionerFacility, Practitioner, ServiceCategory, Option,
            Service, FacilityService, ServiceOption, ServiceRating,
            FacilityApproval, RegulatingBodyContact
        ]

        for model_cls in models:
            if model_cls == RegulatingBodyContact:
                rb = mommy.make(RegulatingBody, name='KMPDB')
                obj = mommy.make(RegulatingBodyContact, regulating_body=rb)
            obj = mommy.make(model_cls)
            self.assertNotEquals(0, len(model_cls.objects.all()))

            #  a naive way to test unicodes for coverage purposes only
            try:
                self.assertIsInstance(obj.__unicode__(), str)
            except AssertionError:
                self.assertIsInstance(obj.__unicode__(), unicode)
