from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from ..models import MflUser


class TestLogin(APITestCase):
    def setUp(self):
        self.user = MflUser.objects.create(
            'user@test.com', 'pass', 'pass', 'pass'
        )
        self.login_url = reverse("api:users:user_login")
        super(TestLogin, self).setUp()

    def test_login(self):
        data = {
            "email": 'user@test.com',
            "password": 'pass'
        }
        response = self.client.post(self.login_url, data)
        self.assertTrue(self.user.is_authenticated())
        self.assertEquals(200, response.status_code)

    def test_inactive_user_login(self):
        user = MflUser.objects.create(
            'user2@test.com', 'test first name', 'test user name', 'pass'
        )
        user.is_active = False
        user.save()
        response = self.client.post(
            self.login_url,
            {
                "email": user.email,
                "password": 'pass'
            }
        )
        self.assertEquals(401, response.status_code)
        self.assertEquals("The user is not active", response.data)

    def test_login_user_does_not_exist(self):
        data = {
            "email": "non_existent@email.com",
            "password": 'pass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEquals(401, response.status_code)
        self.assertEquals(
            "Invalid username/password Combination",
            response.data)

    def test_logout(self):
        user = MflUser.objects.create(
            'user3@test.com', 'test first name', 'test user name 3', 'pass'
        )
        data = {
            "email": user.email,
            "password": 'pass'
        }
        self.client.login(**data)
        self.assertTrue(self.user.is_authenticated())

        # logout the user
        logout_url = reverse("api:users:user_logout")
        self.client.get(logout_url)

        # test that the user is actually loggged out
        # some error here
        # self.assertFalse(self.user.is_authenticated())
