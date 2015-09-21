from django.test import TestCase

from model_mommy import mommy

from ..models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact
)


class TestCommunityHealthUnit(TestCase):

    def test_save(self):
        mommy.make(CommunityHealthUnit)
        self.assertEquals(1, CommunityHealthUnit.objects.count())

    def test_save_with_code(self):
        mommy.make(CommunityHealthUnit, code='7800')
        self.assertEquals(1, CommunityHealthUnit.objects.count())


class TestCommunityHealthWorkerModel(TestCase):

    def test_save(self):
        mommy.make(CommunityHealthWorker, id_number='12345678')
        self.assertEquals(1, CommunityHealthWorker.objects.count())


class TestCommunityHealthWorkerContact(TestCase):

    def test_save(self):
        mommy.make(CommunityHealthWorkerContact)
        self.assertEquals(1, CommunityHealthWorkerContact.objects.count())


class TestModels(TestCase):

    def test_save(self):
        models = [
            CommunityHealthUnit, CommunityHealthWorker,
            CommunityHealthWorkerContact, Status,
            CommunityHealthUnitContact
        ]

        for model_cls in models:
            mommy.make(model_cls)
            self.assertNotEquals(0, len(model_cls.objects.all()))
