from __future__ import division
from django.test import TestCase
from django.core.exceptions import ValidationError

from model_mommy import mommy

from facilities.models import Facility
from ..models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    CommunityHealthUnitContact,
    CHUService,
    CHURating,
    ChuUpdateBuffer
)


class TestChuUpdateBuffer(TestCase):
    def test_save(self):
        mommy.make(ChuUpdateBuffer)
        self.assertEquals(1, ChuUpdateBuffer.objects.count())

    def test_str(self):
        chu_update = mommy.make(ChuUpdateBuffer)
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        self.assertEquals(chu_update.__str__(), chu_update.facility.name)

    def test_atleast_one_thing_editted(self):
        with self.assertRaises(ValidationError):
            mommy.make(
                ChuUpdateBuffer, basic=None, workers=None, contacts=None)


class TestCommunityHealthUnit(TestCase):

    def test_save(self):
        mommy.make(CommunityHealthUnit)
        self.assertEquals(1, CommunityHealthUnit.objects.count())

    def test_save_with_code(self):
        mommy.make(CommunityHealthUnit, code='7800')
        self.assertEquals(1, CommunityHealthUnit.objects.count())

    def test_facility_is_not_closed(self):
        facility = mommy.make(Facility, closed=True)
        with self.assertRaises(ValidationError):
            mommy.make(CommunityHealthUnit, facility=facility)

    def test_chu_approval_or_rejection_and_not_both(self):
        with self.assertRaises(ValidationError):
            mommy.make(CommunityHealthUnit, is_approved=True, is_rejected=True)
        # test rejecting an approvec chu
        chu = mommy.make(CommunityHealthUnit, is_approved=True)
        chu.is_rejected = True
        chu.is_approved = False
        chu.save()

        chu_2 = mommy.make(CommunityHealthUnit, is_rejected=True)
        chu_2.is_approved = True
        chu_2.is_rejected = False
        chu_2.save()

    def test_average_rating(self):
        chu = mommy.make(CommunityHealthUnit)
        chu2 = mommy.make(CommunityHealthUnit)
        ratings = [4, 3, 2, 4, 5, 1]
        for i in ratings:
            mommy.make(CHURating, chu=chu2, rating=i)

        self.assertEqual(chu.average_rating, 0)
        self.assertEqual(chu2.average_rating, sum(ratings, 0) / len(ratings))

    def test_contacts(self):
        chu = mommy.make(CommunityHealthUnit)
        mommy.make(
            CommunityHealthUnitContact, health_unit=chu)
        self.assertIsInstance(chu.contacts, list)

    def test_latest_update(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        update = mommy.make(ChuUpdateBuffer, health_unit=chu)
        self.assertEquals(chu.latest_update, update)

    def test_pending_upates(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        update = mommy.make(ChuUpdateBuffer, health_unit=chu)
        self.assertEquals(chu.latest_update, update)
        self.assertIsInstance(chu.pending_updates, dict)


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
            CommunityHealthUnitContact, CHUService
        ]

        for model_cls in models:
            mommy.make(model_cls)
            self.assertNotEquals(0, len(model_cls.objects.all()))
