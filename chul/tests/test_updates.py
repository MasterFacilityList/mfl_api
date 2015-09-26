from django.core.urlresolvers import reverse

from common.tests.test_views import LoginMixin
from rest_framework.test import APITestCase

from model_mommy import mommy

from facilities.models import Facility

from ..models import (CommunityHealthUnit, ChuUpdateBuffer, Status)


class TestCHUpdatesApproval(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:chul:community_health_units_list")
        self.approve_url = reverse("api:chul:chu_updatebufers_list")
        super(TestCHUpdatesApproval, self).setUp()

    def test_updates_chu_not_approved(self):
        chu = mommy.make(CommunityHealthUnit)
        name = 'Some Name'
        data = {
            "name": name,
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(chu_refetched.name, name)
        self.assertEquals(0, ChuUpdateBuffer.objects.count())

    def test_updates_chu_approved(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        name = 'Some Name'
        data = {
            "name": name,
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertNotEquals(chu_refetched.name, name)
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertNotNone(update.health_unit)
        self.assertNotNone(update.basic)
        self.assertNone(update.contacts)
        self.assertNone(update.workers)

    def test_update_and_approve_basic_details(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        name = 'Some Name'
        data = {
            "name": name,
            "facility": str(facility.id),
            "status": str(status.id)
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertNotEquals(chu_refetched.name, name)
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertNotNone(update.health_unit)
        self.assertNotNone(update.basic)
        self.assertNone(update.contacts)
        self.assertNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_approved": True

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(chu.name, name)
        self.assertEquals(chu_refetched.facility, facility)
        self.assertEquals(chu_refetched.status, status)

    def test_update_chews(self):
        pass

    def test_update_contacts(self):
        pass

    def test_all_updates_combined(self):
        pass

    def test_approved_updates(self):
        pass

    def test_reject_updates(self):
        pass

    def test_approve_chew_updates_with_ids(self):
        pass

    def test_approve_contact_updates(self):
        pass

    def test_basic_details_with_error(self):
        pass

    def test_chews_with_error(self):
        pass

    def test_contacts_with_error(self):
        pass
