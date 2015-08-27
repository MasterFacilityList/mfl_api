from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from facilities.models import RegulationStatus


class TestAuditableViewMixin(APITestCase):

    def setUp(self):
        password = 'mtihani124'
        self.user = get_user_model().objects.create_superuser(
            email='tester@ehealth.or.ke',
            first_name='Test',
            employee_number='124144124124',
            password=password,
            is_national=True
        )
        self.client.login(email='tester@ehealth.or.ke', password=password)

        resp = self.client.post(self._get_list_url(), {"name": "Test status"})
        self.assertEqual(resp.status_code, 201)
        self.status_id = resp.data['id']

    def _get_list_url(self):
        return reverse("api:facilities:regulation_statuses_list")

    def _get_detail_url(self, pk):
        return reverse(
            "api:facilities:regulation_status_detail", kwargs={"pk": pk}
        )

    def test_response_with_no_audit(self):
        url = self._get_detail_url(self.status_id)

        # First, fetch with no audit
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertNotIn("revisions", response.data)

    def test_response_with_audit(self):
        url = self._get_detail_url(self.status_id) + "?include_audit=t"

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEqual(response.data["revisions"], [])

    def test_response_with_audit_empty_change(self):
        url = self._get_detail_url(self.status_id)
        resp = self.client.patch(url, {})
        self.assertEqual(resp.status_code, 200)

        response = self.client.get(url + "?include_audit=t")
        self.assertEquals(200, response.status_code)
        self.assertEqual(response.data["revisions"], [])

    def test_response_with_audit_single_change(self):
        url = self._get_detail_url(self.status_id)

        old_val = RegulationStatus.objects.get(pk=self.status_id).name
        resp = self.client.patch(url, {"name": "changed"})
        self.assertEqual(resp.status_code, 200)

        response = self.client.get(url + '?include_audit=true')
        self.assertEquals(200, response.status_code)
        self.assertEqual(len(response.data["revisions"]), 1)
        self.assertEqual(len(response.data["revisions"][0]["updates"]), 1)

        diff = response.data["revisions"][0]["updates"][0]

        self.assertEqual(diff["name"], "name")
        self.assertEqual(diff["old"], old_val)
        self.assertEqual(diff["new"], "changed")

    def test_response_with_audit_two_changes(self):
        url = self._get_detail_url(self.status_id)

        init_data = RegulationStatus.objects.values(
            'name', 'id').get(pk=self.status_id)

        resp = self.client.patch(url, {"name": 'Kaunti'})
        self.assertEqual(resp.status_code, 200)

        response = self.client.get(url + '?include_audit=true')
        self.assertEquals(200, response.status_code)
        self.assertEqual(len(response.data["revisions"]), 1)

        resp = self.client.patch(url, {"name": 'yeahhh'})
        self.assertEqual(resp.status_code, 200)

        response = self.client.get(url + '?include_audit=true')
        self.assertEquals(200, response.status_code)
        self.assertEqual(len(response.data["revisions"]), 2)
        self.assertEqual(len(response.data["revisions"][0]["updates"]), 1)
        self.assertEqual(len(response.data["revisions"][1]["updates"]), 1)

        diff1 = response.data["revisions"][0]["updates"]
        diff2 = response.data["revisions"][1]["updates"]

        self.assertEqual(
            [{"name": "name", "old": init_data['name'], "new": "Kaunti"}],
            diff2
        )

        self.assertEqual(
            [{"name": "name", "old": "Kaunti", "new": "yeahhh"}],
            diff1
        )

    def test_response_with_audit_one_fk_change(self):
        url = self._get_detail_url(self.status_id)

        create_resp = self.client.post(
            self._get_list_url(), {"name": "previous status"}
        )
        self.assertEqual(create_resp.status_code, 201)

        patch_resp = self.client.patch(
            url, {"previous_status": create_resp.data['id']}
        )
        self.assertEqual(patch_resp.status_code, 200)

        response = self.client.get(url + '?include_audit=true')
        self.assertEquals(200, response.status_code)
        self.assertEqual(len(response.data["revisions"]), 1)
        self.assertEqual(len(response.data["revisions"][0]["updates"]), 1)

        diff = response.data["revisions"][0]["updates"][0]

        self.assertEqual(diff["name"], "previous_status")
        self.assertEqual(diff["old"], None)
        self.assertEqual(diff["new"], "previous status")

    def test_response_with_audit_two_fk_changes(self):
        url = self._get_detail_url(self.status_id)

        create_resp1 = self.client.post(
            self._get_list_url(), {"name": "previous status"}
        )
        self.assertEqual(create_resp1.status_code, 201)

        create_resp2 = self.client.post(
            self._get_list_url(), {"name": "next status"}
        )
        self.assertEqual(create_resp2.status_code, 201)

        patch_resp = self.client.patch(
            url, {
                "name": "haha",
                "previous_status": create_resp1.data['id'],
                "next_status": create_resp2.data['id']
            }
        )
        self.assertEqual(patch_resp.status_code, 200)

        response = self.client.get(url + '?include_audit=true')
        self.assertEquals(200, response.status_code)
        self.assertEqual(len(response.data["revisions"]), 1)
        self.assertEqual(len(response.data["revisions"][0]["updates"]), 3)

        diff = response.data["revisions"][0]["updates"]

        self.assertEqual([
            {"name": "name", "old": "Test status", "new": "haha"},
            {"name": "previous_status", "old": None, "new": "previous status"},
            {"name": "next_status", "old": None, "new": "next status"},
        ], diff)
