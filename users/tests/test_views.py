from django.core.urlresolvers import reverse
from common.tests.test_views import LogginMixin
from rest_framework.test import APITestCase
from model_mommy import mommy

from ..models import MflUser, UserCounties


class TestLogin(APITestCase):
    def test_login(self):
        user = mommy.make(
            MflUser,
            email='user@test.com',
            password='pass',
            is_active=True)

        url = reverse("api:users:user_login")
        data = {
            "email": 'user@test.com',
            "password": 'pass'
        }
        reponse = self.client.post(url, data)
        self.assertTrue(user.is_authenticated())
        self.assertEquals(200, reponse.status_code)

    def test_logout(self):
        user = mommy.make(MflUser)
        login_url = reverse("api:users:user_login")
        data = {
            "email": user.email,
            "password": user.password
        }
        self.client.post(login_url, data)
        self.assertTrue(user.is_authenticated())
        logout_url = reverse("api:users:user_logout")
        self.client.get(logout_url)
        self.assertFalse(user.is_authenticated())
