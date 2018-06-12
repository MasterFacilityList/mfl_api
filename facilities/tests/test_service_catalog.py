from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import LoginMixin
from facilities.models import Option, OptionGroup, ServiceCategory, Service


class TestPostOptionGroupWithOptions(LoginMixin, APITestCase):

    def setUp(self):
        self.url = reverse("api:facilities:post_option_group_with_options")
        super(TestPostOptionGroupWithOptions, self).setUp()

    def test_post_option_group_invalid_data(self):
        self.assertEquals(0, OptionGroup.objects.count())
        data = {
            "name": "test 6",
            "options": [
                {
                    "value": "LEVEL 7 test ",
                    "display_text": "LEVEL 7 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)

        self.assertEquals(1, OptionGroup.objects.count())
        self.assertEquals(1, Option.objects.count())

        # try posting the same data again
        data = {
            "name": "test 6",
            "options": [
                {
                    "value": "LEVEL 8 test ",
                    "display_text": "LEVEL 8 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(1, OptionGroup.objects.count())
        self.assertEquals(1, Option.objects.count())

    def test_post_invalid_option(self):
        data = {
            "name": "test 4",
            "options": [
                {
                    # value key is deliberately left out
                    "display_text": "LEVEL 4 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(400, response.status_code)

    def test_update_options(self):
        option = mommy.make(Option)
        group = mommy.make(OptionGroup)
        data = {
            "id": str(group.id),
            "name": "test",
            "options": [
                {
                    "value": "LEVEL 8 test ",
                    "display_text": "LEVEL 4 test",
                    "option_type": "TEXT"
                },
                {
                    "id": str(option.id),
                    "value": "value_editted",
                    "display_text": "LEVEL 4 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        option_refteched = Option.objects.get(id=option.id)
        group_refteched = OptionGroup.objects.get(id=group.id)
        self.assertEquals(str(option_refteched.value), "value_editted")
        self.assertEquals(str(group_refteched.name), "test")
        self.assertEquals(2, OptionGroup.objects.count())
        self.assertEquals(2, Option.objects.count())

    def test_update_options_error(self):
        option = mommy.make(Option)
        data = {
            "options": [
                {
                    "value": "LEVEL 8 test ",
                    "display_text": "LEVEL 4 test",
                    "option_type": "TEXT"
                },
                {
                    "id": str(option.id),
                    "value": "value_editted",
                    "display_text": "LEVEL 4 test",
                    "option_type": "TEXT"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(400, response.status_code)

    def test_delete(self):
        group = mommy.make(OptionGroup)
        url = self.url + str(group.id) + "/"
        self.client.delete(url)
        self.assertEquals(0, OptionGroup.objects.count())

    def test_delete_not_found(self):
        group = mommy.make(OptionGroup)
        mommy.make(Option, group=group)

        group.delete()
        url = self.url + str(group.id) + "/"
        response = self.client.delete(url)

        self.assertEquals(404, response.status_code)

    def test_flattened_categories_view(self):
        mama = mommy.make(ServiceCategory)
        c1 = mommy.make(ServiceCategory)
        c2 = mommy.make(ServiceCategory, parent=mama)
        mommy.make(Service, category=c1)
        mommy.make(Service, category=c2)
        url = reverse("api:facilities:flattened_categories")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('count'))
        self.assertNotEquals(
            str(mama.id), response.data.get('results')[0].get('id'))
        self.assertNotEquals(
            str(mama.id), response.data.get('results')[1].get('id'))
