from django.core.urlresolvers import reverse

from common.tests.test_views import LoginMixin
from common.models import ContactType, Contact
from rest_framework.test import APITestCase

from model_mommy import mommy

from facilities.models import Facility

from ..models import (
    CommunityHealthUnit,
    ChuUpdateBuffer,
    Status,
    CommunityHealthWorker,
    CommunityHealthUnitContact)


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
        self.assertIsNotNone(update.health_unit)
        self.assertIsNotNone(update.basic)
        self.assertIsNone(update.contacts)
        self.assertIsNone(update.workers)

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
        self.assertIsNotNone(update.health_unit)
        self.assertIsNotNone(update.basic)
        self.assertIsNone(update.contacts)
        self.assertIsNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_approved": True

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(chu_refetched.name, name)
        self.assertEquals(chu_refetched.facility, facility)
        self.assertEquals(chu_refetched.status, status)

    def test_update_and_approve_chews(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        chews = [
            {
                "first_name": "Chew wa kwanza",
                "last_name": "Jina ya pili",
            },
            {
                "first_name": "Chew wa pili",
                "last_name": "Jina ya pili ya chew wa pili",
            }
        ]
        data = {
            'health_unit_workers': chews
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(0, CommunityHealthWorker.objects.count())
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertIsNotNone(update.health_unit)
        self.assertEquals(update.basic, '{}')
        self.assertIsNone(update.contacts)
        self.assertIsNotNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_approved": True

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthWorker.objects.count())
        self.assertEquals(2, CommunityHealthWorker.objects.filter(
            health_unit=chu_refetched).count())

    def test_update_contacts(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        contact_type = mommy.make(ContactType)
        contact_type_2 = mommy.make(ContactType)
        contacts = [
            {
                "contact_type": str(contact_type.id),
                "contact": "385235725"

            },
            {
                "contact_type": str(contact_type_2.id),
                "contact": "385235725"
            }
        ]

        data = {
            'contacts': contacts
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(0, CommunityHealthUnitContact.objects.count())
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertIsNotNone(update.health_unit)
        self.assertEquals(update.basic, '{}')
        self.assertIsNotNone(update.contacts)
        self.assertIsNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_approved": True

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthUnitContact.objects.count())
        self.assertEquals(2, CommunityHealthUnitContact.objects.filter(
            health_unit=chu_refetched).count())

    def test_all_updates_combined(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        contact_type = mommy.make(ContactType)
        contact_type_2 = mommy.make(ContactType)
        name = 'Jina mpya'
        contacts = [
            {
                "contact_type": str(contact_type.id),
                "contact": "385235725"

            },
            {
                "contact_type": str(contact_type_2.id),
                "contact": "385235725"
            }
        ]
        chews = [
            {
                "first_name": "Chew wa kwanza",
                "last_name": "Jina ya pili",
            },
            {
                "first_name": "Chew wa pili",
                "last_name": "Jina ya pili ya chew wa pili",
            }
        ]
        date_established = "2015-09-23"
        date_operational = "2015-10-25"
        data = {
            'contacts': contacts,
            'health_unit_workers': chews,
            'name': name,
            'date_established': date_established,
            'date_operational': date_operational
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)

        self.assertEquals(200, response.status_code)

        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(0, CommunityHealthUnitContact.objects.count())
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertIsNotNone(update.health_unit)
        self.assertIsNotNone(update.basic)
        self.assertIsNotNone(update.contacts)
        self.assertIsNotNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_approved": True

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthUnitContact.objects.count())
        self.assertEquals(2, CommunityHealthUnitContact.objects.filter(
            health_unit=chu_refetched).count())
        self.assertEquals(2, CommunityHealthWorker.objects.count())
        self.assertEquals(2, CommunityHealthWorker.objects.filter(
            health_unit=chu_refetched).count())
        self.assertEquals(name, chu_refetched.name)
        self.assertEquals(
            date_established,
            chu_refetched.date_established.isoformat())
        self.assertEquals(
            date_operational, chu_refetched.date_operational.isoformat())

    def test_reject_updates(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        contact_type = mommy.make(ContactType)
        contact_type_2 = mommy.make(ContactType)
        name = 'Jina mpya'
        contacts = [
            {
                "contact_type": str(contact_type.id),
                "contact": "385235725"

            },
            {
                "contact_type": str(contact_type_2.id),
                "contact": "385235725"
            }
        ]
        chews = [
            {
                "first_name": "Chew wa kwanza",
                "last_name": "Jina ya pili",
            },
            {
                "first_name": "Chew wa pili",
                "last_name": "Jina ya pili ya chew wa pili",
            }
        ]
        date_established = "2015-09-23"
        date_operational = "2015-10-25"
        data = {
            'contacts': contacts,
            'health_unit_workers': chews,
            'name': name,
            'date_established': date_established,
            'date_operational': date_operational
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(0, CommunityHealthUnitContact.objects.count())
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertIsNotNone(update.health_unit)
        self.assertIsNotNone(update.basic)
        self.assertIsNotNone(update.contacts)
        self.assertIsNotNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_rejected": False

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(0, CommunityHealthUnitContact.objects.count())
        self.assertEquals(0, CommunityHealthUnitContact.objects.filter(
            health_unit=chu_refetched).count())
        self.assertEquals(0, CommunityHealthWorker.objects.count())
        self.assertEquals(0, CommunityHealthWorker.objects.filter(
            health_unit=chu_refetched).count())
        self.assertNotEquals(name, chu_refetched.name)
        self.assertNotEquals(date_established, chu_refetched.date_established)
        self.assertNotEquals(date_operational, chu_refetched.date_operational)

    def test_approve_chew_updates_with_ids(self):
        chu = mommy.make(CommunityHealthUnit)
        chew_1 = mommy.make(CommunityHealthWorker, health_unit=chu)
        chew_2 = mommy.make(CommunityHealthWorker, health_unit=chu)
        chu.is_approved = True
        chu.save()
        chews = [
            {
                "first_name": "Chew wa kwanza",
                "last_name": "Jina ya pili",
                "id": str(chew_1.id),
                'is_incharge': True,
            },
            {
                "first_name": "Chew wa pili",
                "last_name": "Jina ya pili ya chew wa pili",
                'is_incharge': False,
                "id": str(chew_2.id)
            }
        ]
        data = {
            'health_unit_workers': chews
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthWorker.objects.count())
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertIsNotNone(update.health_unit)
        self.assertEquals(update.basic, '{}')
        self.assertIsNone(update.contacts)
        self.assertIsNotNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_approved": True

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthWorker.objects.count())
        self.assertEquals(2, CommunityHealthWorker.objects.filter(
            health_unit=chu_refetched).count())

    def test_approve_chew_updates_with_ids_no_id_no_and_is_incharge(self):
        chu = mommy.make(CommunityHealthUnit)
        chew_1 = mommy.make(CommunityHealthWorker, health_unit=chu)
        chew_2 = mommy.make(CommunityHealthWorker, health_unit=chu)
        chu.is_approved = True
        chu.save()
        chews = [
            {
                "first_name": "Chew wa kwanza",
                "last_name": "Jina ya pili",
                "id": str(chew_1.id),
            },
            {
                "first_name": "Chew wa pili",
                "last_name": "Jina ya pili ya chew wa pili",
                "id": str(chew_2.id)
            }
        ]
        data = {
            'health_unit_workers': chews
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthWorker.objects.count())
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertIsNotNone(update.health_unit)
        self.assertEquals(update.basic, '{}')
        self.assertIsNone(update.contacts)
        self.assertIsNotNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_approved": True

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthWorker.objects.count())
        self.assertEquals(2, CommunityHealthWorker.objects.filter(
            health_unit=chu_refetched).count())

    def test_approve_chew_updates_without_ids(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        chews = [
            {
                "first_name": "Chew wa kwanza",
                "last_name": "Jina ya pili",
                'is_incharge': True,
            },
            {
                "first_name": "Chew wa pili",
                "last_name": "Jina ya pili ya chew wa pili",
                'is_incharge': False,
            }
        ]
        data = {
            'health_unit_workers': chews
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertIsNotNone(update.health_unit)
        self.assertEquals(update.basic, '{}')
        self.assertIsNone(update.contacts)
        self.assertIsNotNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_approved": True

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthWorker.objects.count())
        self.assertEquals(2, CommunityHealthWorker.objects.filter(
            health_unit=chu_refetched).count())

    def test_contacts_with_ids(self):
        chu = mommy.make(CommunityHealthUnit)
        chu.is_approved = True
        chu.save()
        contact_type = mommy.make(ContactType)
        contact_type_2 = mommy.make(ContactType)
        contact_1 = mommy.make(
            Contact, contact="3852357254", contact_type=contact_type)
        contact_2 = mommy.make(
            Contact, contact="385235725", contact_type=contact_type_2)
        chu_contact_1 = mommy.make(
            CommunityHealthUnitContact, health_unit=chu, contact=contact_1)
        chu_contact_2 = mommy.make(
            CommunityHealthUnitContact, health_unit=chu, contact=contact_2)
        contacts = [
            {
                "contact_type": str(contact_type.id),
                "contact": "3852357254",
                "contact_type_name": contact_type.name,
                "contact_id": str(contact_1.id),
                "id": str(chu_contact_1.id)

            },
            {
                "contact_type": str(contact_type_2.id),
                "contact": "385235725",
                "contact_type_name": contact_type_2.name,
                "contact_id": str(contact_2.id),
                "id": str(chu_contact_2.id)
            }
        ]

        data = {
            'contacts': contacts
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthUnitContact.objects.count())
        self.assertEquals(1, ChuUpdateBuffer.objects.count())
        update = ChuUpdateBuffer.objects.all()[0]
        self.assertIsNotNone(update.health_unit)
        self.assertEquals(update.basic, '{}')
        self.assertIsNotNone(update.contacts)
        self.assertIsNone(update.workers)

        approve_update_url = self.approve_url + "{}/".format(update.id)
        approve_data = {
            "is_approved": True

        }
        response = self.client.patch(approve_update_url, approve_data)
        self.assertEquals(200, response.status_code)
        chu_refetched = CommunityHealthUnit.objects.get(id=chu.id)
        self.assertEquals(2, CommunityHealthUnitContact.objects.count())
        self.assertEquals(2, CommunityHealthUnitContact.objects.filter(
            health_unit=chu_refetched).count())
