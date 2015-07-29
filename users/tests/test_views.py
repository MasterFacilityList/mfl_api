import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from common.tests.test_views import LoginMixin

from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from model_mommy import mommy

from ..models import MflUser
from ..serializers import _lookup_groups


class TestLogin(APITestCase):

    def setUp(self):
        self.user = MflUser.objects.create_user(
            email='user@test.com', first_name='test name',
            password='password1233', username='username'
        )
        self.login_url = reverse("api:rest_auth:rest_login")
        self.logout_url = reverse("api:rest_auth:rest_logout")
        super(TestLogin, self).setUp()

    def test_login(self):
        data = {
            "username": 'user@test.com',
            "password": 'password1233'
        }
        response = self.client.post(self.login_url, data)
        self.assertTrue(self.user.is_authenticated())
        self.assertEquals(200, response.status_code)

    def test_inactive_user_login(self):
        user = MflUser.objects.create_user(
            email='user2@test.com', first_name='test first name',
            username='test user name', password='pass_long124124'
        )
        user.is_active = False
        user.save()
        response = self.client.post(
            self.login_url,
            {
                "username": user.email,
                "password": 'pass_long124124'
            }
        )
        self.assertEquals(400, response.status_code)
        self.assertEquals(
            {'non_field_errors': ['User account is disabled.']},
            response.data
        )

    def test_login_user_does_not_exist(self):
        data = {
            "username": "non_existent@email.com",
            "password": 'pass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(
            {
                'non_field_errors': [
                    'Unable to log in with provided credentials.']
            },
            response.data
        )


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
            "password": "rubbishpass12424"
        }
        response = self.client.post(create_url, post_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual("Ruhusa", response.data["last_name"])

    def test_update_user(self):
        user = MflUser.objects.create(
            email='user@test.com', first_name='pass',
            username='pass', password='pass_long12424'
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

    def test_update_user_pwd(self):
        user = MflUser.objects.create(
            email='user@test.com', first_name='pass',
            username='pass', password='pass12r12r12r'
        )
        update_url = reverse(
            'api:users:mfl_user_detail', kwargs={'pk': user.id})
        patch_data = {
            "first_name": "Phyll",
            "password": "yeah_longerr1r12",
        }
        response = self.client.patch(update_url, patch_data)
        self.assertEqual(200, response.status_code)

        user = MflUser.objects.get(id=user.id)
        self.assertTrue(user.check_password(patch_data['password']))
        self.assertEqual(user.first_name, patch_data["first_name"])

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

    def test_password_quality_during_reset(self):
        user = mommy.make(MflUser, password='strong1344')
        url = reverse('api:users:mfl_users_list') + "{}/".format(user.id)
        data = {
            "password": "weak"
        }
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)


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


class TestDeleting(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse('api:users:mfl_users_list')
        super(TestDeleting, self).setUp()

    def test_delete_county(self):
        user = mommy.make(MflUser)
        url = self.url + '{}/'.format(user.id)
        response = self.client.delete(url)
        # assert status code due to cache time of 15 seconds
        self.assertEquals(200, response.status_code)
        # self.assertEquals("Not Found", response.data.get('detail'))

        with self.assertRaises(MflUser.DoesNotExist):
            MflUser.objects.get(id=user.id)

        self.assertEquals(1, MflUser.everything.filter(id=user.id).count())


class TestUserFiltering(APITestCase):
    def test_get_users_in_county(self):
        from common.models import (
            UserCounty, County, Constituency, UserConstituency)

        user = mommy.make(MflUser)

        user_2 = mommy.make(MflUser)
        user_3 = mommy.make(MflUser)
        user_4 = mommy.make(MflUser)
        user_5 = mommy.make(MflUser)
        user_6 = mommy.make(MflUser)

        county = mommy.make(County)
        county_2 = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        const_2 = mommy.make(Constituency, county=county_2)

        mommy.make(UserCounty, user=user, county=county)
        mommy.make(UserCounty, user=user_2, county=county)
        mommy.make(UserCounty, user=user_3, county=county)
        mommy.make(UserCounty, user=user_4, county=county_2)
        mommy.make(
            UserConstituency, user=user_5, created_by=user,
            updated_by=user, constituency=const)
        mommy.make(
            UserConstituency, user=user_6, created_by=user_4,
            updated_by=user_4, constituency=const_2)

        self.client.force_authenticate(user)
        url = reverse("api:users:mfl_users_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(4, len(response.data.get("results")))

    def test_national_user_sees_all_users(self):
        from common.models import UserCounty, County

        user = mommy.make(MflUser)
        user.is_national = True
        user.save()

        user_2 = mommy.make(MflUser)
        user_3 = mommy.make(MflUser)
        user_4 = mommy.make(MflUser)

        county = mommy.make(County)
        county_2 = mommy.make(County)

        mommy.make(UserCounty, user=user, county=county)
        mommy.make(UserCounty, user=user_2, county=county)
        mommy.make(UserCounty, user=user_3, county=county)
        mommy.make(UserCounty, user=user_4, county=county_2)

        self.client.force_authenticate(user)
        url = reverse("api:users:mfl_users_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

        self.assertEquals(5, len(response.data.get("results")))
