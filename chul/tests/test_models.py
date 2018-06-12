from __future__ import division
from datetime import datetime, timedelta

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
        mommy.make(ChuUpdateBuffer, basic="{'name': 'new name'}")
        self.assertEquals(1, ChuUpdateBuffer.objects.count())

    def test_str(self):
        chu_update = mommy.make(ChuUpdateBuffer, basic="{'name': 'new name'}")
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        self.assertEquals(chu_update.__str__(), chu_update.health_unit.name)

    def test_chu_update_basic_not_edited(self):
        chu_update = mommy.make(
            ChuUpdateBuffer,
            workers='[{"first_name": "jina"}]'
        )
        self.assertIsNone(chu_update.updates.get('basic'))

    def test_atleast_one_thing_editted(self):
        with self.assertRaises(ValidationError):
            mommy.make(
                ChuUpdateBuffer, basic=None, workers=None, contacts=None)


class TestCommunityHealthUnit(TestCase):

    def test_save(self):
        mommy.make(CommunityHealthUnit)
        self.assertEquals(1, CommunityHealthUnit.objects.count())

    def test_date_operational_less_than_date_established(self):
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        with self.assertRaises(ValidationError):
            mommy.make(
                CommunityHealthUnit,
                date_established=today, date_operational=last_week)

    def test_date_established_not_in_future(self):
        today = datetime.now().date()
        next_month = today + timedelta(days=30)
        with self.assertRaises(ValidationError):
            mommy.make(
                CommunityHealthUnit,
                date_established=today, date_operational=next_month)

    def test_valid_dates(self):
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        mommy.make(
            CommunityHealthUnit,
            date_established=last_week, date_operational=today)
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
        # test rejecting an approve chu
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

    def test_rating_count(self):
        chu = mommy.make(CommunityHealthUnit)
        chu2 = mommy.make(CommunityHealthUnit)
        ratings = [4, 3, 2, 4, 5, 1]
        for i in ratings:
            mommy.make(CHURating, chu=chu2, rating=i)

        self.assertEqual(chu.rating_count, 0)
        self.assertEqual(chu2.rating_count, len(ratings))

    def test_contacts(self):
        chu = mommy.make(CommunityHealthUnit)
        mommy.make(
            CommunityHealthUnitContact, health_unit=chu)
        self.assertIsInstance(chu.contacts, list)

    def test_latest_update(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        update = mommy.make(
            ChuUpdateBuffer,
            health_unit=chu,
            basic='{"name": "some new name"}')
        self.assertEquals(chu.latest_update, update)

    def test_pending_upates(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        update = mommy.make(
            ChuUpdateBuffer,
            health_unit=chu,
            basic='{"name": "some new name"}')
        self.assertEquals(chu.latest_update, update)
        self.assertIsInstance(chu.pending_updates, dict)

    def test_has_edits_true(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        mommy.make(
            ChuUpdateBuffer,
            health_unit=chu,
            basic='{"name": "some new name"}')
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertTrue(chu_refetched.has_edits)

    def test_has_edits_false_afater_approval(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        update = mommy.make(
            ChuUpdateBuffer,
            health_unit=chu,
            basic='{"name": "some new name"}')
        update.is_approved = True
        update.save()
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertFalse(chu_refetched.has_edits)

    def test_has_edits_false_after_rejection(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        update = mommy.make(
            ChuUpdateBuffer,
            health_unit=chu,
            basic='{"name": "some new name"}')
        update.is_rejected = True
        update.save()
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertFalse(chu_refetched.has_edits)

    def test_chu_workers(self):
        chu = mommy.make(CommunityHealthUnit)
        mommy.make(CommunityHealthWorker, health_unit=chu)
        self.assertIsInstance(chu.workers, list)


class TestCommunityHealthWorkerModel(TestCase):

    def test_save(self):
        mommy.make(CommunityHealthWorker)
        self.assertEquals(1, CommunityHealthWorker.objects.count())

    def test_name(self):
        worker = mommy.make(
            CommunityHealthWorker,
            first_name='Test', last_name='Test')
        self.assertEquals('Test Test', worker.name)

        worker = mommy.make(
            CommunityHealthWorker,
            first_name='Test', last_name=None)
        self.assertEquals('Test', worker.name)


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
