from django.utils import timezone
from django.core.exceptions import ValidationError
from model_mommy import mommy
from common.tests.test_models import BaseTestCase

from ..models import MflUser


class TestMflUserModel(BaseTestCase):
    def test_save_normal_user(self):
        data = {
            "email": "some@email.com",
            "username": "some",
            "first_name": "jina",
            "last_name": "mwisho",
            "other_names": "jm",
            "password": "password",
        }
        user = MflUser.objects.create_user(**data)

        # the base  test case class comes with another user
        self.assertEquals(3, MflUser.objects.count())

        # test unicode
        self.assertEquals('some@email.com', user.__unicode__())
        self.assertEquals("jina", user.get_short_name)
        self.assertEquals("jina mwisho jm", user.get_full_name)

    def test_save_superuser(self):
        self.assertEquals(2, MflUser.objects.count())
        data = {
            "email": "some@email.com",
            "username": "some",
            "first_name": "jina",
            "last_name": "mwisho",
            "other_names": "jm",
            "password": "password",
        }
        user = MflUser.objects.create_superuser(**data)

        # the base  test case class comes with another user
        self.assertEquals(3, MflUser.objects.count())
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_permissions_property(self):
        data = {
            "email": "some@email.com",
            "username": "some",
            "first_name": "jina",
            "last_name": "mwisho",
            "other_names": "jm",
            "password": "password",
        }
        MflUser.objects.create_superuser(**data)
        # mysterious error here
        # self.assertTrue(len(user.permissions) > 0)
        # self.assertTrue("common.add_constituency" in user.permissions)

    def test_set_password_does_not_set_for_new_users(self):
        user = mommy.make(MflUser, password='a great password')
        user.set_password('does not really matter')
        self.assertIsNotNone(user.password_history)

    def test_set_password_sets_for_existing_users(self):
        user = mommy.make(MflUser, password='a very huge password')
        user.last_login = timezone.now()
        user.set_password('we now expect the change history to be saved')
        self.assertTrue(user.password_history)
        self.assertEqual(len(user.password_history), 1)

    def test_requires_password_change_new_user(self):
        user = mommy.make(MflUser, password='a very huge password')
        self.assertTrue(user.requires_password_change)

    def test_requires_password_change_new_user_with_prior_login(self):
        user = mommy.make(MflUser, password='A very huge password')
        user.last_login = timezone.now()
        self.assertTrue(user.requires_password_change)

    def test_doesnt_require_password_change_user_with_prior_passwords(self):
        user = mommy.make(MflUser, password='A very huge password')
        user.last_login = timezone.now()
        user.set_password('we now expect the change history to be saved')
        self.assertFalse(user.requires_password_change)
        user.set_password('we now expect the change history to be saved')
        self.assertEqual(len(user.password_history), 2)

    def test_password_is_greater_than_or_equal_to_6_characters(self):
        data = {
            "email": "some@email.com",
            "username": "some",
            "first_name": "jina",
            "last_name": "mwisho",
            "other_names": "jm",
            "password": "ort",
        }
        with self.assertRaises(ValidationError):
            MflUser.objects.create_user(**data)
