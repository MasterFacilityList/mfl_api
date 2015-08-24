from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from common.tests.test_views import LoginMixin

from facilities.models import Option, OptionGroup


class TestPostOptionGroupWithOptions(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:facilities:post_option_group_with_options")
        super(TestPostOptionGroupWithOptions, self).setUp()

    def test_post_option_group_with_options(self):
        data = {
            "option_group": "KEPH Level Option Group test",
            "options": [
                {
                    "value": "LEVEL 1 test",
                    "display_text": "LEVEL 1 test",
                    "option_type": "TEXT"
                },
                {
                    "value": "LEVEL 2 test",
                    "display_text": "LEVEL 2 test",
                    "option_type": "TEXT"
                },
                {
                    "value": "LEVEL 3 test",
                    "display_text": "LEVEL 3 test",
                    "option_type": "TEXT"
                },
                {
                    "value": "LEVEL 4 test",
                    "display_text": "LEVEL 4 test",
                    "option_type": "TEXT"
                },
                {
                    "value": "LEVEL 5 test",
                    "display_text": "LEVEL 5 test",
                    "option_type": "TEXT"
                },
                {
                    "value": "LEVEL 6 test ",
                    "display_text": "LEVEL 6 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data)

        self.assertEquals(201, response.status_code)
        self.assertEquals(6, Option.objects.count())
        self.assertEquals(1, OptionGroup.objects.count())

    def _test_post_option_group_name_uniqueness(self):
        data_1 = {
            "option_group": "KEPH Level Option Group test 2",
            "options": [
                {
                    "value": "LEVEL 1 test",
                    "display_text": "LEVEL 1 test",
                    "option_type": "TEXT"
                }
            ]
        }
        data_2 = {
            "option_group": "KEPH Level Option Group test 2",
            "options": [
                {
                    "value": "LEVEL 1 test",
                    "display_text": "LEVEL 1 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data_1)
        self.assertEquals(201, response.status_code)
        response_2 = self.client.post(self.url, data_2)
        self.assertEquals(400, response_2.status_code)
