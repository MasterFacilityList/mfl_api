from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from .test_views import LoginMixin

from common.models import County
from model_mommy import mommy
from common.renderers import _write_excel_file


class TestExcelRenderer(LoginMixin, APITestCase):
    def test_get_excel_from_end_point(self):
        url = reverse('api:common:counties_list')
        excel_url = url + "?format=excel"
        mommy.make(County)
        mommy.make(County)
        response = self.client.get(excel_url)
        self.assertEquals(200, response.status_code)

    def test_write_excel_file(self):
        mommy.make(County)
        mommy.make(County)
        url = reverse('api:common:counties_list')
        response = self.client.get(url)
        _write_excel_file(response.data)

    def test_nested_list_in_excel_renderer(self):
        data = {
            "results": [
                {
                    "key_a": "data",
                    "key_b": "data"
                },
                {
                    "key_a": "data",
                    "key_b": "data"
                },
                {
                    "key_a": "data",
                    "key_b": [
                        {
                            "key_a": "data",
                            "key_b": "data"
                        }
                    ]
                }
            ]
        }

        _write_excel_file(data)

    def test_nested_empty_list_in_excel_renderer(self):
            data = {
                "results": [
                    {
                        "key_a": "data",
                        "key_b": "data"
                    },
                    {
                        "key_a": "data",
                        "key_b": "data"
                    },
                    {
                        "key_a": "data",
                        "key_b": []
                    }
                ]
            }

            _write_excel_file(data)

    def test_empty_list(self):
        data = {
            "results": []
        }

        _write_excel_file(data)
