import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from common.tests.test_views import LoginMixin
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError

from ..models import MflUser
from ..serializers import _lookup_groups


class TestUserViews(LoginMixin, APITestCase):

    def test_create_user(self):
        create_url = reverse('api:users:mfl_users_list')
        group = Group.objects.create(name="Test Group")
        post_data = {
            "groups": [{"id": group.id, "name": "Test Group"}],
            "email": "hakunaruhusa@mfltest.slade360.co.ke",
            "first_name": "Hakuna",
            "last_name": "Ruhusa",
            "other_names": "",
            "username": "hakunaruhusa",
            "password": "rubbishpass"
        }
        response = self.client.post(create_url, post_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual("Ruhusa", response.data["last_name"])

    def test_update_user(self):
        user = MflUser.objects.create(
            'user@test.com', 'pass', 'pass', 'pass'
        )
        group = Group.objects.create(name="Test Group")
        update_url = reverse(
            'api:users:mfl_user_detail', kwargs={'pk': user.id})
        patch_data = {
            "other_names": "Majina Mengine",
            "groups": [
                {"id": group.id, "name": "Test Group"}
            ]
        }
        response = self.client.patch(update_url, patch_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            json.loads(json.dumps(response.data['groups']))[0]['name'],
            group.name
        )

    def test_failed_create(self):
        create_url = reverse('api:users:mfl_users_list')
        data = {
            "username": "yusa",
            "email": "yusa@yusa.com",
            "groups": [
                {
                    "id": 67897,
                    "name": "does not exist, should blow up nicely"
                }
            ]
        }
        response = self.client.post(create_url, data)
        self.assertEqual(400, response.status_code)


class TestCurrentUserDetailView(LoginMixin, APITestCase):
    url = reverse("api:users:current_user")

    def test_deny_unauthorized_access(self):
        client = self.client.__class__()
        resp = client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_current_user(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.data
        self.assertEqual(self._user.email, data['email'])
        self.assertEqual(self._user.first_name, data['first_name'])

        for i in ['password', 'password_history']:
            self.assertNotIn(i, data)


class TestGroupViews(LoginMixin, APITestCase):

    def setUp(self):
        super(TestGroupViews, self).setUp()
        self.url = reverse('api:users:groups_list')

    def test_invalid_group_lookup(self):
        with self.assertRaises(ValidationError):
            _lookup_groups(None)

    def test_create_and_update_group(self):
        data = {
            "name": "Documentation Example Group",
            "permissions": [
                {
                    "id": 61,
                    "name": "Can add email address",
                    "codename": "add_emailaddress"
                },
                {
                    "id": 62,
                    "name": "Can change email address",
                    "codename": "change_emailaddress"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.data['name'], 'Documentation Example Group')
        self.assertEqual(len(response.data['permissions']), 2)

        new_group_id = response.data['id']
        update_url = reverse(
            'api:users:group_detail', kwargs={'pk': new_group_id})
        update_response = self.client.put(
            update_url,
            {
                "name": "Documentation Example Group Updated",
                "permissions": [
                    {
                        "id": 61,
                        "name": "Can add email address",
                        "codename": "add_emailaddress"
                    }
                ]
            }
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(len(update_response.data['permissions']), 1)

    def test_failed_create(self):
        data = {
            "name": "Documentation Example Group",
            "permissions": [
                {
                    "id": 67897,
                    "name": "does not exist",
                    "codename": "query should raise an exception"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)
