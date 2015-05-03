from django.test import TestCase

from model_mommy import mommy

from facilities.models import Facility
from facilities.serializers import FacilitySerializer

from ..utilities import search_utils


class TestElasticSearchAPI(TestCase):
    def setUp(self):
        self.elastic_search_api = search_utils.ElasticAPI()
        super(TestElasticSearchAPI, self).setUp()

    def tearDown(self):
        self.elastic_search_api.delete_index()
        super(TestElasticSearchAPI, self).tearDown()

    def test_setup_index(self):
        result = self.elastic_search_api.setup_index(index_name='test_index')
        self.assertEquals(200, result.json().get('status'))
        self.elastic_search_api.delete_index(index_name='test_index')


class TestSearchFunctions(TestCase):
    def test_serialize_model(self):
        facility = mommy.make(Facility)
        serialized_data = FacilitySerializer(facility).data
        expected_data = FacilitySerializer(facility).data
        self.assertEquals(expected_data, serialized_data)
