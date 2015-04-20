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
)


class TestModels(TestCase):
    def test_save(self):
        models = [
            PracticeType, Speciality, Qualification,
            PractitionerQualification, PractitionerContact,
            PractitionerFacility, Practitioner
        ]

        for model_cls in models:
            obj = mommy.make(model_cls)
            self.assertNotEquals(0, len(model_cls.objects.all()))

            #  a naive way to test unicodes for coverage purposes only
            try:
                self.assertIsInstance(obj.__unicode__(), str)
            except AssertionError:
                self.assertIsInstance(obj.__unicode__(), unicode)
