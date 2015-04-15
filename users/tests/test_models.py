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
        self.assertEquals(1, MflUser.objects.count())
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
