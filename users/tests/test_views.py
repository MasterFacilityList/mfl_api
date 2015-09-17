import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from model_mommy import mommy

from common.models import County, Constituency, UserCounty, UserConstituency
from common.tests.test_views import LoginMixin
from ..models import MflUser, CustomGroup
from ..serializers import _lookup_groups, GroupSerializer


class TestLogin(APITestCase):

    def setUp(self):
        mommy.make(Group, name='Facility Viewing Group')
        self.user = MflUser.objects.create_user(
            email='user@test.com', first_name='test name',
            password='password1233', employee_number='7784448445'
        )
        self.login_url = reverse("api:rest_auth:rest_login")
        self.logout_url = reverse("api:rest_auth:rest_logout")
        super(TestLogin, self).setUp()

    def test_login(self):
        data = {
            "username": self.user.employee_number,
            "password": 'password1233'
        }
        response = self.client.post(self.login_url, data)
        self.assertTrue(self.user.is_authenticated())
        self.assertEquals(200, response.status_code)

    def test_inactive_user_login(self):
        user = MflUser.objects.create_user(
            email='user2@test.com', first_name='test first name',
            employee_number='test user name', password='pass_long124124'
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
            "employee_number": "1224467890",
            "password": "rubbishpass12424"
        }
        response = self.client.post(create_url, post_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual("Ruhusa", response.data["last_name"])

    def test_create_user_is_staff(self):
        create_url = reverse('api:users:mfl_users_list')
        group = Group.objects.create(name="Test Group")
        mommy.make(CustomGroup, group=group, regulator=True)
        post_data = {
            "groups": [{"id": group.id, "name": "Test Group"}],
            "email": "hakunaruhusa@mfltest.slade360.co.ke",
            "first_name": "Hakuna",
            "last_name": "Ruhusa",
            "other_names": "",
            "employee_number": "1224467890",
            "password": "rubbishpass12424"
        }
        response = self.client.post(create_url, post_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual("Ruhusa", response.data["last_name"])
        user = MflUser.objects.get(email="hakunaruhusa@mfltest.slade360.co.ke")
        self.assertTrue(user.is_staff)

    def test_update_user(self):
        user = MflUser.objects.create(
            email='user@test.com', first_name='pass',
            employee_number='9448855555', password='pass_long12424'
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

    def test_user_is_staff_for_regulator(self):
        user = MflUser.objects.create(
            email='user@test.com', first_name='pass',
            employee_number='9448855555', password='pass_long12424'
        )
        group = Group.objects.create(name="Test Group")
        CustomGroup.objects.create(group=group, regulator=True)
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

        user_refetched = MflUser.objects.get(email='user@test.com')
        self.assertTrue(user_refetched.is_staff)

    def test_user_is_staff_for_chrio(self):
        user = MflUser.objects.create(
            email='user@test.com', first_name='pass',
            employee_number='9448855555', password='pass_long12424'
        )
        group = Group.objects.create(name="Test Group")
        CustomGroup.objects.create(group=group, administrator=True)
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

        user_refetched = MflUser.objects.get(email='user@test.com')
        self.assertTrue(user_refetched.is_staff)

    def test_user_is_staff_for_schrio(self):
        user = MflUser.objects.create(
            email='user@test.com', first_name='pass',
            employee_number='9448855555', password='pass_long12424'
        )
        group = Group.objects.create(name="Test Group")
        CustomGroup.objects.create(group=group, county_level=True)
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
        user_refetched = MflUser.objects.get(email='user@test.com')
        self.assertTrue(user_refetched.is_staff)

    def test_user_is_staff_for_national_admins(self):
        user = MflUser.objects.create(
            email='user@test.com', first_name='pass',
            employee_number='9448855555', password='pass_long12424'
        )
        group = Group.objects.create(name="Test Group")
        CustomGroup.objects.create(group=group, national=True)
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

        user_refetched = MflUser.objects.get(email='user@test.com')
        self.assertTrue(user_refetched.is_staff)

    def test_update_user_pwd(self):
        user = MflUser.objects.create(
            email='user@test.com', first_name='pass',
            employee_number='6444444444', password='pass12r12r12r'
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
            "employee_number": "yusa",
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
        user = mommy.make(MflUser)
        user.set_password('strong1344')
        user.save()
        self.client.logout()
        self.client.force_authenticate(user)
        url = "/api/rest-auth/password/change/"
        data = {
            "old_password": "strong1344",
            "new_password1": "weak",
            "new_password2": "weak"
        }
        response = self.client.post(url, data)
        self.assertEquals(400, response.status_code)
        data = {
            "old_password": "strong1344",
            "new_password1": "#weakMadeStrong999",
            "new_password2": "#weakMadeStrong999"
        }

        response = self.client.post(url, data)
        self.assertEquals(200, response.status_code)

    def test_password_quality_missing_fields(self):
        user = mommy.make(MflUser)
        user.set_password('strong1344')
        user.save()
        self.client.logout()
        self.client.force_authenticate(user)

        url = "/api/rest-auth/password/change/"
        # old_password1 field is left out
        data = {
            "old_password": "strong13443463",
            "new_password2": "weak"
        }
        response = self.client.post(url, data)
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
            "is_national": True,
            "is_regulator": True,
            "is_administrator": True,
            "permissions": [
                {
                    "name": "Can add email address",
                    "codename": "add_emailaddress"
                },
                {
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
                "is_national": True,
                "is_regulator": False,
                "is_administrator": True,
                "permissions": [
                    {
                        "name": "Can add email address",
                        "codename": "add_emailaddress"
                    }
                ]
            }
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(len(update_response.data['permissions']), 1)

    def test_custom_group_does_not_exist(self):
        group = mommy.make(Group)
        self.assertEquals(0, CustomGroup.objects.count())
        update_url = reverse(
            'api:users:group_detail', kwargs={'pk': group.id})
        data = {
            "is_national": True,
            "is_regulator": False,
            "is_administrator": True,
        }
        self.client.patch(update_url, data)
        self.assertEquals(1, CustomGroup.objects.count())

    def test_failed_create(self):
        data = {
            "name": "Documentation Example Group",
            "is_national": True,
            "is_regulator": True,
            "is_administrator": True,
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

    def test_delete_group_with_custom_group(self):
        group = mommy.make(Group)
        mommy.make(CustomGroup, group=group)
        user = mommy.make(MflUser)
        user.groups.add(group)
        self.assertEquals(1, user.groups.all().count())
        url = reverse("api:users:groups_list")
        url = url + "{}/".format(group.id)

        self.client.delete(url)
        # the login mixin somes with one preconfigured group
        self.assertEquals(1, Group.objects.count())
        self.assertEquals(0, user.groups.all().count())

    def test_delete_group_without_custom_group(self):
        group = mommy.make(Group)
        url = reverse("api:users:groups_list")
        url = url + "{}/".format(group.id)

        self.client.delete(url)
        # the login mixin somes with one preconfigured group
        self.assertEquals(1, Group.objects.count())


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
    def setUp(self):
        mommy.make(Group, name='Facility Viewing Group')
        self.url = reverse("api:users:mfl_users_list")
        super(TestUserFiltering, self).setUp()

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
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(3, len(response.data.get("results")))

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
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)

        self.assertEquals(4, len(response.data.get("results")))

    def test_users_with_no_priviledges_see_no_user(self):
        user = mommy.make(MflUser)
        mommy.make(MflUser)
        mommy.make(MflUser)
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        self.assertEquals([], response.data.get("results"))

    def test_superuser_sees_all_users(self):
        user = mommy.make(MflUser, is_superuser=True)
        self.client.force_authenticate(user)
        mommy.make(MflUser)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get("count"))
        self.assertEquals(2, len(response.data.get('results')))

    def test_subcounty_users_does_not_see_users_in_own_sub_county(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        user = mommy.make(MflUser)
        user_2 = mommy.make(MflUser)
        mommy.make(UserCounty, county=county, user=user)
        mommy.make(
            UserConstituency, constituency=constituency,
            user=user_2, created_by=user, updated_by=user)
        user_3 = mommy.make(MflUser)
        mommy.make(
            UserConstituency, constituency=constituency,
            user=user_3, created_by=user_2, updated_by=user_2)
        self.client.force_authenticate(user_2)
        response = self.client.get(self.url)
        self.assertEquals(0, response.data.get('count'))
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, len(response.data.get('results')))

    def test_sub_county_user_sees_the_facility_incharges_created(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        user = mommy.make(MflUser)
        user_2 = mommy.make(MflUser)
        mommy.make(UserCounty, county=county, user=user)
        mommy.make(
            UserConstituency, constituency=constituency,
            user=user_2, created_by=user, updated_by=user)
        user_3 = mommy.make(MflUser, created_by=user_2)
        user_4 = mommy.make(MflUser, created_by=user_2)
        group = Group.objects.get(name="Facility Viewing Group")
        CustomGroup.objects.create(group=group, sub_county_level=True)
        group_2 = Group.objects.create(name="Some other group")
        CustomGroup.objects.create(group=group_2, county_level=True)
        user_4.groups.add(group)
        mommy.make(
            UserConstituency, constituency=constituency,
            user=user_3, created_by=user_2, updated_by=user_2)
        self.client.force_authenticate(user_2)
        response = self.client.get(self.url)
        self.assertEquals(2, response.data.get('count'))
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, len(response.data.get('results')))


class TestGroupFilters(LoginMixin, APITestCase):
    def setUp(self):
        self.groups_list_url = reverse("api:users:groups_list")
        super(TestGroupFilters, self).setUp()

    def test_county_level_true(self):
        group = mommy.make(Group)
        mommy.make(Group)
        mommy.make(CustomGroup, group=group, county_level=True)
        url = self.groups_list_url + "?is_county_level=true"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

    def test_county_level_false(self):
        mommy.make(Group)
        mommy.make(Group)
        url = self.groups_list_url + "?is_county_level=false"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, response.data.get('count'))

    def test_sub_county_level_true(self):
        group = mommy.make(Group)
        mommy.make(Group)
        mommy.make(CustomGroup, group=group, sub_county_level=True)
        url = self.groups_list_url + "?is_sub_county_level=true"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

    def test_sub_county_level_false(self):
        mommy.make(Group)
        mommy.make(Group)
        url = self.groups_list_url + "?is_sub_county_level=false"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, response.data.get('count'))

    def test_regulator_true(self):
        group = mommy.make(Group)
        mommy.make(Group)
        mommy.make(CustomGroup, group=group, regulator=True)
        url = self.groups_list_url + "?is_regulator=true"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

    def test_regulator_false(self):
        group = mommy.make(Group)
        mommy.make(Group)
        mommy.make(CustomGroup, group=group)
        url = self.groups_list_url + "?is_regulator=false"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

    def test_national_level_true(self):
        group = mommy.make(Group)
        mommy.make(Group)
        mommy.make(CustomGroup, group=group, national=True)
        url = self.groups_list_url + "?is_national_level=true"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

    def test_national_level_false(self):
        group = mommy.make(Group)
        mommy.make(Group)
        mommy.make(CustomGroup, group=group)
        url = self.groups_list_url + "?is_national_level=false"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

    def test_filter_group_by_name(self):
        group = mommy.make(Group, name='group ya ajabu')
        mommy.make(Group, name='jina tu')
        url = self.groups_list_url + "?name=ajabu"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        expected_data = [
            GroupSerializer(group).data
        ]
        self.assertEquals(response.data.get('results'), expected_data)
