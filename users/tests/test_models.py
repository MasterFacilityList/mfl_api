from django.core.exceptions import ValidationError
from model_mommy import mommy

from common.tests.test_models import BaseTestCase
from common.models import County

from ..models import MflUser, UserCounties


class TestMflUserModel(BaseTestCase):
    def test_save_normal_user(self):
        data = {
            "email": "some@email.com",
            "username": "some",
            "first_name": "jina",
            "last_name": "mwisho",
            "other_names": "jm",
            "password": "pass",
        }
        user = MflUser.objects.create(**data)

        # the base  test case class comes with another user
        self.assertEquals(2, MflUser.objects.count())

        # test unicode
        self.assertEquals('some@email.com', user.__unicode__())
        self.assertEquals("jina", user.get_short_name)
        self.assertEquals("jina mwisho jm", user.get_full_name)

    def test_save_superuser(self):
            data = {
                "email": "some@email.com",
                "username": "some",
                "first_name": "jina",
                "last_name": "mwisho",
                "other_names": "jm",
                "password": "pass",
            }
            user = MflUser.objects.create_superuser(**data)

            # the base  test case class comes with another user
            self.assertEquals(2, MflUser.objects.count())
            self.assertTrue(user.is_superuser)
            self.assertTrue(user.is_staff)


class TestUserCountiesModel(BaseTestCase):
    def test_save(self):
        user = mommy.make(MflUser)
        county = mommy.make(County)
        data = {
            "user": user,
            "county": county

        }
        user_county = UserCounties.objects.create(**data)
        self.assertEquals(1, UserCounties.objects.count())
        expected_unicode = "{}: {}".format(user.email, county.name)
        self.assertEquals(expected_unicode, user_county.__unicode__())

    def test_user_is_only_active_in_one_count(self):
        user = mommy.make(MflUser)
        county_1 = mommy.make(County)
        county_2 = mommy.make(County)
        UserCounties.objects.create(
            user=user,
            county=county_1
        )
        with self.assertRaises(ValidationError):
            UserCounties.objects.create(
                user=user,
                county=county_2
            )
