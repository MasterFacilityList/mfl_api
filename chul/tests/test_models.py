from django.test import TestCase

from model_mommy import mommy

from ..models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact,
    Approver,
    CommunityHealthUnitApproval,
    CommunityHealthWorkerApproval,
    ApprovalStatus
)


class TestCommunityHealthUnit(TestCase):
    def test_save(self):
        health_unit = mommy.make(CommunityHealthUnit)
        self.assertEquals(1, CommunityHealthUnit.objects.count())

        # test unicode
        self.assertEquals(health_unit.__unicode__(), health_unit.name)

    def test_save_with_code(self):
        mommy.make(CommunityHealthUnit, code='7800')
        self.assertEquals(1, CommunityHealthUnit.objects.count())


class TestCommunityHealthWorkerModel(TestCase):
    def test_save(self):
        health_worker = mommy.make(
            CommunityHealthWorker, id_number='12345678')

        self.assertEquals(1, CommunityHealthWorker.objects.count())

        # test unicode
        self.assertEquals('12345678', health_worker.__unicode__())

    def test_name(self):
        worker = mommy.make(
            CommunityHealthWorker,
            first_name='Dorcas',
            last_name='Omwansa',
            surname='Kibukosya')
        self.assertEquals('Dorcas Omwansa Kibukosya', worker.name)


class TestCommunityHealthWorkerContact(TestCase):
    def test_save(self):
        hw_contact = mommy.make(CommunityHealthWorkerContact)
        self.assertEquals(1, CommunityHealthWorkerContact.objects.count())

        # test unicode
        expected_unicode = "{}: {}".format(
            hw_contact.health_worker, hw_contact.contact)
        self.assertEquals(expected_unicode, hw_contact.__unicode__())


class TestModels(TestCase):
    def test_save(self):
        models = [
            CommunityHealthUnit, CommunityHealthWorker,
            CommunityHealthWorkerContact, Status,
            CommunityHealthUnitContact, Approver, CommunityHealthUnitApproval,
            CommunityHealthWorkerApproval, ApprovalStatus
        ]

        for model_cls in models:
            obj = mommy.make(model_cls)
            self.assertNotEquals(0, len(model_cls.objects.all()))

            #  a naive way to test unicodes for coverage purposes only
            try:
                self.assertIsInstance(obj.__unicode__(), str)
            except AssertionError:
                self.assertIsInstance(obj.__unicode__(), unicode)
