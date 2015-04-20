from django.test import TestCase

from model_mommy import mommy

from ..models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact
)


class TestCommunityHealthUnit(TestCase):
    def test_save(self):
        health_unit = mommy.make(CommunityHealthUnit)
        self.assertEquals(1, CommunityHealthUnit.objects.count())

        # test unicode
        self.assertEquals(health_unit.__unicode__(), health_unit.name)


class TestCommunityHealthWorkerModel(TestCase):
    def test_save(self):
        health_worker = mommy.make(
            CommunityHealthWorker, id_number='12345678')

        self.assertEquals(1, CommunityHealthWorker.objects.count())

        # test unicode
        self.assertEquals('12345678', health_worker.__unicode__())


class TestCommunityHealthWorkerContact(TestCase):
    def test_save(self):
        hw_contact = mommy.make(CommunityHealthWorkerContact)
        self.assertEquals(1, CommunityHealthWorkerContact.objects.count())

        # test unicode
        expected_unicode = "{}: {}".format(
            hw_contact.health_worker, hw_contact.contact)
        self.assertEquals(expected_unicode, hw_contact.__unicode__())
