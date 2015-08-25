from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from common.tests.test_views import LoginMixin

from facilities.models import Option, OptionGroup


class TestPostOptionGroupWithOptions(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:facilities:post_option_group_with_options")
        super(TestPostOptionGroupWithOptions, self).setUp()

    def test_post_option_group_invalid_data(self):

        data = {
            "option_group": "test 6",
            "options": [
                {
                    "value": "LEVEL 6 test ",
                    "display_text": "LEVEL 6 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data)

        self.assertEquals(201, response.status_code)

        # try posting the same data again
        data = {
            "option_group": "test 6",
            "options": [
                {
                    "value": "LEVEL 6 test ",
                    "display_text": "LEVEL 6 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(400, response.status_code)

    def test_post_invalid_option(self):
        data = {
            "option_group": "test 4",
            "options": [
                {
                    # value key is missing
                    "display_text": "LEVEL 6 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(400, response.status_code)
