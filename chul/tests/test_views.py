from django.core.urlresolvers import reverse

from model_mommy import mommy

from common.tests import ViewTestBase


from ..models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact
)
from ..serializers import (
    CommunityHealthUnitSerializer,
    CommunityHealthWorkerSerializer,
    CommunityHealthWorkerContactSerializer
)


class TestCommunityHealthUnitView(ViewTestBase):
    def setUp(self):
        self.url = reverse("api:chul:community_health_units_list")
        super(TestCommunityHealthUnitView, self).setUp()

    def test_list_community_health_units(self):
        health_unit = mommy.make(CommunityHealthUnit)
        health_unit_2 = mommy.make(CommunityHealthUnit)

        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                CommunityHealthUnitSerializer(health_unit_2).data,
                CommunityHealthUnitSerializer(health_unit).data

            ]
        }
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)

    def test_retrieve_single_healt_unit(self):
        health_unit = mommy.make(CommunityHealthUnit)
        url = self.url + "{}/".format(health_unit.id)
        expected_data = CommunityHealthUnitSerializer(health_unit).data
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)


class TestCommunitHealthWorkerView(ViewTestBase):
    def setUp(self):
        self.url = reverse("api:chul:community_health_workers_list")
        super(TestCommunitHealthWorkerView, self).setUp()

    def test_health_workers_listing(self):
        worker_1 = mommy.make(CommunityHealthWorker)
        worker_2 = mommy.make(CommunityHealthWorker)
        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                CommunityHealthWorkerSerializer(worker_1).data,
                CommunityHealthWorkerSerializer(worker_2).data

            ]
        }
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.maxDiff = None
        self._assert_response_data_equality(expected_data, response.data)

    def test_retrieve_single_worker(self):
        worker = mommy.make(CommunityHealthWorker)
        expected_data = CommunityHealthWorkerSerializer(worker).data
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
        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                CommunityHealthWorkerContactSerializer(contact_2).data,
                CommunityHealthWorkerContactSerializer(contact_1).data

            ]
        }
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)

    def test_retrieve_single_health_worker_contact(self):
        contact = mommy.make(CommunityHealthWorkerContact)
        expected_data = CommunityHealthWorkerContactSerializer(contact).data
        url = self.url + "{}/".format(contact.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)
