from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from model_mommy import mommy


from common.models import County
from common.renderers.excel_renderer import (
    _write_excel_file, sanitize_field_names, _build_name_from_list
)
from .test_views import LoginMixin


class TestExcelRenderer(LoginMixin, APITestCase):

    def test_not_list(self):
        c = mommy.make(County)
        url = reverse('api:common:county_detail', kwargs={"pk": c.id})
        url += "?format=excel"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 406)

    def test_get_excel_from_end_point(self):
        url = reverse('api:common:counties_list')
        excel_url = url + "?format=excel"
        mommy.make(County)
        mommy.make(County)
        response = self.client.get(excel_url)
        self.assertEquals(200, response.status_code)

    def test_get_non_list_endpoint(self):
        county = mommy.make(County)
        url = reverse('api:common:counties_list')
        url = url + "{}/".format(county.id)
        excel_url = url + "?format=excel"
        mommy.make(County)
        response = self.client.get(excel_url)
        self.assertEquals(406, response.status_code)

    def test_write_excel_file(self):
        mommy.make(County)
        mommy.make(County)
        url = reverse('api:common:counties_list')
        response = self.client.get(url)
        _write_excel_file(response.data['results'])

    def test_nested_list_in_excel_renderer(self):
        data = [
            {
                "key_a": "data",
                "key_b": "data",
                "key_b": "39f97a13-4f3f-45a3-a411-970e496526cd",
                'boolean_key': False
            },
            {
                "key_a": "data",
                "key_b": "data",
                "key_b": "39f97a13-4f3f-45a3-a411-970e496526cd",
                'boolean_key': True
            },
            {
                "key_a": "data",
                "key_b": [
                    {
                        "key_a": "data",
                        "key_b": "data"
                    }
                ],
                "key_b": "39f97a13-4f3f-45a3-a411-970e496526cd"
            }
        ]
        _write_excel_file(data)

    def test_nested_empty_list_in_excel_renderer(self):
        data = [
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
        _write_excel_file(data)

    def test_empty_list(self):
        data = []
        _write_excel_file(data)

    def test_sanitize_field_names(self):
        sample_list = ['regulatory_status_name']
        key_map = sanitize_field_names(sample_list)
        self.assertEquals([
            {
                "actual": sample_list[0],
                "preferred": "regulatory status"
            }
        ], key_map)

        sample_list = ['is_approved']
        key_map = sanitize_field_names(sample_list)
        self.assertEquals([
            {
                "actual": sample_list[0],
                "preferred": "approved"
            }
        ], key_map)
        sample_list = ['name']
        key_map = sanitize_field_names(sample_list)
        self.assertEquals([
            {
                "actual": sample_list[0],
                "preferred": "name"
            }
        ], key_map)

    def test__build_name_from_list(self):
        name_list = ["regulatory", "status"]
        result = _build_name_from_list(name_list)
        self.assertEquals("regulatory status", result)
        name_list = ["approved"]
        result = _build_name_from_list(name_list)
        self.assertEquals("approved", result)


class TestCsvRenderer(LoginMixin, APITestCase):

    def test_not_list(self):
        c = mommy.make(County)
        url = reverse('api:common:county_detail', kwargs={"pk": str(c.pk)})
        url += "?format=csv"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 406)

    def test_get_csv_from_end_point(self):
        url = reverse('api:common:counties_list')
        excel_url = url + "?format=csv"
        mommy.make(County)
        mommy.make(County)
        response = self.client.get(excel_url)
        self.assertEquals(200, response.status_code)


class TestPDFRender(LoginMixin, APITestCase):

    def test_get_pdf_from_end_point(self):
        url = reverse('api:common:counties_list')
        pdf_url = url + "?format=pdf"
        mommy.make(County)
        mommy.make(County)
        response = self.client.get(pdf_url)
        self.assertEquals(200, response.status_code)
