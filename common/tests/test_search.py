from django.test import TestCase

from model_mommy import mommy

from facilities.models import Facility
from facilities.serializers import FacilitySerializer

from ..utilities import search_utils


class TestElasticSearchAPI(TestCase):
    def setUp(self):
        self.elastic_search_api = search_utils.ElasticAPI()
        super(TestElasticSearchAPI, self).setUp()

    def test_setup_index(self):
        result = self.elastic_search_api.setup_index()
        self.assertEquals(200, result.json().get('status'))


class TestSearchFunctions(TestCase):
    def test_serialize_model(self):
        facility = mommy.make(Facility)
        serialized_data = FacilitySerializer(facility).data
        expected_data = FacilitySerializer(facility).data
        self.assertEquals(expected_data, serialized_data)
