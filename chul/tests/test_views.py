from django.core.urlresolvers import reverse

from model_mommy import mommy

from common.tests import ViewTestBase


from ..models import (
    Status,
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact
)
from ..serializers import (
    CommunityHealthUnitSerializer,
    CommunityHealthWorkerSerializer,
    CommunityHealthWorkerContactSerializer
)
from facilities.models import Facility


class TestCommunityHealthUnitView(ViewTestBase):

    def setUp(self):
        self.url = reverse("api:chul:community_health_units_list")
        super(TestCommunityHealthUnitView, self).setUp()

    def test_post_chu(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        data = {
            "facility": facility.id,
            "name": "test community",
            "status": status.id,
            "households_monitored": 100,
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, CommunityHealthUnit.objects.count())

    def test_post_chu_inlined_chew(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        data = {
            "facility": facility.id,
            "name": "test community",
            "status": status.id,
            "households_monitored": 100,
            "health_unit_workers": [
                {
                    "first_name": "Muuguzi",
                    "last_name": "Mnoma",
                    "id_number": "3477757",
                    "is_incharge": True
                }
            ]
        }
        response = self.client.post(self.url, data)

        self.assertEquals(201, response.status_code)
        self.assertEquals(1, CommunityHealthUnit.objects.count())

    def test_patch_chu_inlined_chew(self):
        chu = mommy.make(CommunityHealthUnit)
        chew = mommy.make(CommunityHealthWorker, health_unit=chu)
        data = {
            "households_monitored": 100,
            "health_unit_workers": [
                {
                    "id": str(chew.id),
                    "first_name": "Muuguzi tabibu",
                    "last_name": "Mnoma",
                    "id_number": "3477757",
                    "is_incharge": True
                }
            ]
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, CommunityHealthUnit.objects.count())
        self.assertEquals(
            CommunityHealthWorker.objects.all()[0].first_name,
            "Muuguzi tabibu")

    def test_post_chu_inlined_chew_invalid_data(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        data = {
            "facility": facility.id,
            "name": "test community",
            "status": status.id,
            "households_monitored": 100,
            "health_unit_workers": [
                {
                    "is_incharge": True
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(400, response.status_code)

    def test_list_community_health_units(self):
        health_unit = mommy.make(CommunityHealthUnit)
        health_unit_2 = mommy.make(CommunityHealthUnit)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                CommunityHealthUnitSerializer(
                    health_unit_2,
                    context={
                        'request': response.request
                    }
                ).data,
                CommunityHealthUnitSerializer(
                    health_unit,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(
            expected_data['results'], response.data['results']
        )

    def test_retrieve_single_health_unit(self):
        health_unit = mommy.make(CommunityHealthUnit)
        url = self.url + "{}/".format(health_unit.id)
        response = self.client.get(url)
        expected_data = CommunityHealthUnitSerializer(
            health_unit,
            context={
                'request': response.request
            }
        ).data

        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)


class TestCommunityHealthWorkerView(ViewTestBase):

    def setUp(self):
        self.url = reverse("api:chul:community_health_workers_list")
        super(TestCommunityHealthWorkerView, self).setUp()

    def test_health_workers_listing(self):
        worker_1 = mommy.make(CommunityHealthWorker)
        worker_2 = mommy.make(CommunityHealthWorker)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                CommunityHealthWorkerSerializer(
                    worker_2,
                    context={
                        'request': response.request
                    }
                ).data,
                CommunityHealthWorkerSerializer(
                    worker_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.maxDiff = None
        self._assert_response_data_equality(
            expected_data['results'], response.data['results']
        )

    def test_retrieve_single_worker(self):
        worker = mommy.make(CommunityHealthWorker)
        expected_data = CommunityHealthWorkerSerializer(
            worker, context={
                'request': {
                    "REQUEST_METHOD": "None"
                }
            }
        ).data
        url = self.url + "{}/".format(worker.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)


class TestCommunityHealthWokerContactView(ViewTestBase):

    def setUp(self):
        self.url = reverse("api:chul:community_health_worker_contacts_list")
        super(TestCommunityHealthWokerContactView, self).setUp()

    def test_health_workers_contact_list(self):
        contact_1 = mommy.make(CommunityHealthWorkerContact)
        contact_2 = mommy.make(CommunityHealthWorkerContact)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                CommunityHealthWorkerContactSerializer(
                    contact_2,
                    context={
                        'request': response.request
                    }
                ).data,
                CommunityHealthWorkerContactSerializer(
                    contact_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(
            expected_data['results'], response.data['results']
        )

    def test_retrieve_single_health_worker_contact(self):
        contact = mommy.make(CommunityHealthWorkerContact)
        url = self.url + "{}/".format(contact.id)
        response = self.client.get(url)
        expected_data = CommunityHealthWorkerContactSerializer(
            contact,
            context={
                'request': response.request
            }
        ).data
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)
