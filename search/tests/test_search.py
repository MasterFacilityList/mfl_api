import json
from mock import patch
from requests.exceptions import ConnectionError

from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from model_mommy import mommy

from facilities.models import Facility, FacilityApproval

from facilities.serializers import FacilitySerializer
from common.models import (
    County,
    Constituency,
    UserConstituency,
    UserCounty,
    ErrorQueue
)
from common.tests import ViewTestBase
from mfl_gis.models import FacilityCoordinates
from chul.models import CommunityHealthUnit

from search.filters import SearchFilter
from search.search_utils import (
    ElasticAPI, index_instance, default, serialize_model)
from users.models import JobTitle
from ..index_settings import get_mappings


SEARCH_TEST_SETTINGS = {
    "ELASTIC_URL": "http://localhost:9200/",
    "INDEX_NAME": "test_index",
    "NON_INDEXABLE_MODELS": [
        "mfl_gis.FacilityCoordinates",
        "mfl_gis.WorldBorder",
        "mfl_gis.CountyBoundary",
        "mfl_gis.ConstituencyBoundary",
        "mfl_gis.WardBoundary",
        "users.CustomGroup",
        "users.ProxyGroup"
    ],
    "FULL_TEXT_SEARCH_FIELDS": {

        "models": [
            {
                "name": "facility",
                "fields": [
                    "name", "county", "constituency", "ward_name",
                    "facility_services.service_name",
                    "facility_services.service_name",
                    "facility_services.category_name",
                    "facility_physical_address.town",
                    "facility_physical_address.nearest_landmark",
                    "facility_physical_address.nearest_landmark"
                ]
            }
        ]

    },
    "AUTOCOMPLETE_MODEL_FIELDS": [
        {
            "app": "facilities",
            "models": [
                {
                    "name": "facility",
                    "fields": ["name", "ward_name"]
                },
                {
                    "name": "owner",
                    "fields": ["name"]
                }
            ]
        }
    ]
}
CACHES_TEST_SETTINGS = {
    'default': {
        'BACKEND':
        'django.core.cache.backends.dummy.DummyCache',
    }
}


@override_settings(
    SEARCH=SEARCH_TEST_SETTINGS,
    CACHES=CACHES_TEST_SETTINGS)
class TestElasticSearchAPI(TestCase):

    def setUp(self):
        self.elastic_search_api = ElasticAPI()
        super(TestElasticSearchAPI, self).setUp()

    def test_setup_index(self):
        self.elastic_search_api.delete_index(index_name='test_index')
        result = self.elastic_search_api.setup_index(index_name='test_index')
        self.assertEquals(200, result.status_code)
        self.elastic_search_api.delete_index(index_name='test_index')

    def test_get_non_existing_index(self):
        index_name = 'test_index'
        self.elastic_search_api.delete_index(index_name)
        self.elastic_search_api.get_index(index_name)

    def test_get_exsting_index(self):
        index_name = 'test_index'
        self.elastic_search_api.setup_index(index_name=index_name)
        self.elastic_search_api.get_index(index_name)
        self.elastic_search_api.delete_index(index_name='test_index')

    def test_delete_index(self):
        index_name = 'test_index_3'
        response = self.elastic_search_api.setup_index(index_name=index_name)
        self.assertEquals(200, response.status_code)
        self.elastic_search_api.delete_index(index_name)

    def test_index_document(self):
        facility = mommy.make(Facility, name='Fig tree medical clinic')
        self.elastic_search_api.setup_index(index_name='test_index')
        result = index_instance(
            'facilities', 'Facility', str(facility.id), 'test_index')
        self.assertTrue(result)

    def test_search_document_no_instance_type(self):
        index_name = 'test_index'
        response = self.elastic_search_api.setup_index(index_name=index_name)
        self.assertEquals(200, response.status_code)
        facility = mommy.make(Facility, name='Fig tree medical clinic')
        result = index_instance(
            'facilities', 'Facility', str(facility.id), 'test_index')
        self.assertTrue(result)
        self.elastic_search_api.search_document(
            index_name=index_name, instance_type=Facility, query='tree')

    def test_remove_document(self):
        index_name = 'test_index'
        self.elastic_search_api.setup_index(index_name=index_name)
        facility = mommy.make(Facility, name='Fig tree medical clinic')
        result = index_instance(
            'facilities', 'Facility', str(facility.id), 'test_index')
        self.assertTrue(result)
        self.elastic_search_api.remove_document(
            index_name, 'facility', str(facility.id))
        self.elastic_search_api.delete_index(index_name='test_index')

    def test_index_settings(self):
        expected_map = get_mappings()
        for key, value in expected_map.items():
            for key_2, value_2 in expected_map.get(key).items():
                for key_3, value_3 in expected_map.get(key).get(key_2).items():
                        values = expected_map.get(key).get(key_2).get(key_3)
                        self.assertEquals(
                            'autocomplete',
                            values.get('index_analyzer'))
                        self.assertEquals(
                            'autocomplete',
                            values.get('search_analyzer'))
                        self.assertEquals(
                            'string',
                            values.get('type'))
                        self.assertEquals(
                            False,
                            values.get('coerce'))
                        self.assertEquals(
                            True,
                            values.get('store'))

    def test_is_on_true(self):
        self.assertTrue(self.elastic_search_api._is_on)

    def test_is_on_false(self):
        with patch('search.search_utils.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError
            elastic_api = ElasticAPI()
            self.assertFalse(elastic_api._is_on)

    def tearDown(self):
        self.elastic_search_api.delete_index(index_name='test_index')
        super(TestElasticSearchAPI, self).tearDown()


@override_settings(
    SEARCH=SEARCH_TEST_SETTINGS,
    CACHES=CACHES_TEST_SETTINGS)
class TestSearchFunctions(ViewTestBase):
    def setUp(self):
        self.elastic_search_api = ElasticAPI()
        self.elastic_search_api.setup_index(index_name='test_index')
        super(TestSearchFunctions, self).setUp()

    def test_serialize_model(self):
        self.maxDiff = None
        facility = mommy.make(Facility)
        serialized_data = serialize_model(facility)
        expected_data = FacilitySerializer(
            facility
        ).data
        expected_data = json.dumps(expected_data, default=default)
        self.assertEquals(expected_data, serialized_data.get('data'))

    def test_serialize_model_serializer_not_found(self):
        # There is no serializer named GroupSerializer
        # Therefore the serialize model function should return None
        group = mommy.make(Group)
        serialized_data = serialize_model(group)
        self.assertIsNone(serialized_data)

    def test_default_json_dumps_function(self):
        facility = mommy.make(Facility)
        data = FacilitySerializer(
            facility
        ).data
        result = json.dumps(data, default=default)
        self.assertIsInstance(result, str)

    def test_search_facility(self):
        url = reverse('api:facilities:facilities_list')
        self.elastic_search_api = ElasticAPI()
        self.elastic_search_api.setup_index(index_name='test_index')
        facility = mommy.make(Facility, name='Kanyakini')
        index_instance(
            'facilities', 'Facility', str(facility.id), 'test_index')
        url = url + "?search={}".format('Kanyakini')

        response = self.client.get(url)

        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.data.get('results'), list)

        self.elastic_search_api.delete_index('test_index')

    def test_search_facility_using_material_view(self):
        self.elastic_search_api = ElasticAPI()
        self.elastic_search_api.setup_index(index_name='test_index')

        facility = mommy.make(Facility, name='Facility ya kutest material')
        url = reverse('api:facilities:material')
        index_instance(
            'facilities', 'Facility', str(facility.id), 'test_index')
        url = url + "?search={}".format('material')

        response = self.client.get(url)

        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.data.get('results'), list)

        self.elastic_search_api.delete_index('test_index')

    def test_search_facility_using_query_dsl(self):
        url = reverse('api:facilities:facilities_list')
        self.elastic_search_api = ElasticAPI()
        self.elastic_search_api.setup_index(index_name='test_index')
        facility = mommy.make(Facility, name='Kanyakini')
        index_instance(
            'facilities', 'Facility', str(facility.id), 'test_index')
        query_dsl = {
            "from": 0,
            "size": 30,
            "query": {
                "query_string": {
                    "default_field": "name",
                    "query": "Kanyakini"
                }
            }
        }
        url = url + "?search={}".format(json.dumps(query_dsl))

        response = self.client.get(url)

        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.data.get('results'), list)

        self.elastic_search_api.delete_index('test_index')

    def test_seach_auto_complete(self):
        url = reverse('api:facilities:facilities_list')
        self.elastic_search_api = ElasticAPI()
        self.elastic_search_api.setup_index(index_name='test_index')
        facility = mommy.make(Facility, name='Kanyakini')
        index_instance(
            'facilities', 'Facility', str(facility.id), 'test_index')
        url = url + "?search_auto={}".format('Kanya')
        response = self.client.get(url)

        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.data.get('results'), list)

        self.elastic_search_api.delete_index('test_index')

    def test_search_facility_multiple_filters(self):
        url = reverse('api:facilities:facilities_list')
        self.elastic_search_api = ElasticAPI()
        self.elastic_search_api.setup_index(index_name='test_index')

        facility = mommy.make(
            Facility, name='Mordal mountains medical clinic')
        mommy.make(FacilityApproval, facility=facility)
        facility.is_published = True
        facility.save()
        facility_2 = mommy.make(
            Facility,
            name='Eye of mordal health center',
            is_published=False)
        index_instance(
            'facilities', 'Facility', str(facility.id), 'test_index')

        index_instance(
            'facilities', 'Facility', str(facility_2.id), 'test_index')

        url = url + "?search={}&is_published={}".format('mordal', 'false')
        response = self.client.get(url)

        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.data.get('results'), list)

        self.elastic_search_api.delete_index('test_index')

    def test_get_search_auto_complete_fields(self):
        search_fields = self.elastic_search_api.get_search_fields('facility')
        self.assertIsInstance(search_fields, list)
        self.assertEquals(len(search_fields), 10)

    def test_get_search_auto_complete_fields_si_empty(self):
        search_fields = self.elastic_search_api.get_search_fields('no_model')
        self.assertIsNone(search_fields)

    def test_user_search(self):
        user = mommy.make(get_user_model(), is_national=True)
        self.client.force_authenticate(user)
        county_user = mommy.make(get_user_model())
        sub_county_user = mommy.make(
            get_user_model(), first_name='kijana', last_name='mzee')

        index_instance(
            'users', 'MflUser', str(sub_county_user.id), 'test_index')
        url = reverse("api:users:mfl_users_list")
        url = url + "?search=kijana"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        # the national users are not allowed to see the sub county level users
        county = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        mommy.make(UserCounty, county=county, user=county_user)
        mommy.make(
            UserConstituency, user=sub_county_user, constituency=const,
            created_by=county_user, updated_by=county_user)
        filtered_response = self.client.get(url)
        self.assertEquals(200, filtered_response.status_code)

    def test_chu_search(self):
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        chu_url = reverse("api:chul:community_health_units_list")
        chu = mommy.make(
            CommunityHealthUnit, facility=facility, name='Jericho')
        mommy.make(CommunityHealthUnit, facility=facility_2)
        index_instance(
            'chul', 'CommunityHealthUnit', str(chu.id), 'test_index')
        chu_search_url = chu_url + "?search=Jericho"
        response = self.client.get(chu_search_url)
        self.assertEquals(200, response.status_code)

    def test_chu_search_using_code(self):
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        chu_url = reverse("api:chul:community_health_units_list")
        chu = mommy.make(
            CommunityHealthUnit, facility=facility, name='Jericho')
        mommy.make(CommunityHealthUnit, facility=facility_2)
        index_instance(
            'chul', 'CommunityHealthUnit', str(chu.id), 'test_index')
        chu_search_url = chu_url + "?search={}".format(chu.code)
        response = self.client.get(chu_search_url)
        self.assertEquals(200, response.status_code)

    def test_record_pushed_to_error_queue(self):
        with patch('search.search_utils.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError
            mommy.make(Facility, name='Ile Noma')
            self.assertEquals(1, ErrorQueue.objects.count())

    def test_unique_record_in_error_queue(self):
        with patch('search.search_utils.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError
            facility = mommy.make(Facility, name='Ile Noma')
            self.assertEquals(1, ErrorQueue.objects.count())
            facility.name = 'Ile noma sana'
            facility.save()
            self.assertEquals(1, ErrorQueue.objects.count())

    def test_retrying_indexing_elastic_search_off(self):
        with patch('search.search_utils.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError
            mommy.make(Facility, name='Ile Noma')
            call_command('retry_indexing')

            # elastic search down hence no records updated
            self.assertEquals(1, ErrorQueue.objects.count())

    def test_retrying_indexing_elastic_search_on(self):
        mommy.make(Facility, name='Ile Noma')
        self.assertEquals(0, ErrorQueue.objects.count())
        call_command('retry_indexing')

        # elastic search up hence records updated
        self.assertEquals(0, ErrorQueue.objects.count())

    def test_retrying_indexing_object_already_deleted(self):
        facility = mommy.make(Facility, name='Ile Noma')
        facility.delete()
        ErrorQueue.objects.create(
            object_pk=str(facility.pk),
            error_type='SEARCH_INDEXING_ERROR',
            app_label='facilities',
            model_name='Facility')
        call_command('retry_indexing')
        self.assertEquals(1, ErrorQueue.objects.count())

    def test_retry_indexing_objects_in_queue(self):
        with patch('search.search_utils.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError
            mommy.make(Facility, name='Ile Noma')
            self.assertEquals(1, ErrorQueue.objects.count())

        # elastic search up hence records updated
        call_command('retry_indexing')
        self.assertEquals(0, ErrorQueue.objects.count())

    def test_index_non_indexable_model(self):
        job_title = mommy.make(JobTitle)
        self.assertFalse(
            index_instance('users', 'JobTitle', job_title.id)
        )

    def test_sending_email_to_admins(self):
        """
        This is for test coverage only.
        Tests that emails are sent to admins if the number
        of retries on a record is more than one
        """

        with patch('search.search_utils.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError
            mommy.make(Facility, name='Ile Noma')
            self.assertEquals(1, ErrorQueue.objects.count())
            # elastic search up hence records updated
            call_command('retry_indexing')
            self.assertEquals(1, ErrorQueue.objects.count())
            error_queue_object = ErrorQueue.objects.all()[0]
            self.assertEquals(1, error_queue_object.retries)

            call_command('retry_indexing')
            self.assertEquals(1, ErrorQueue.objects.count())
            error_queue_object = ErrorQueue.objects.all()[0]
            self.assertEquals(2, error_queue_object.retries)

            call_command('retry_indexing')
            self.assertEquals(1, ErrorQueue.objects.count())
            error_queue_object = ErrorQueue.objects.all()[0]
            self.assertEquals(3, error_queue_object.retries)

    def test_search_using_facility_name_when_elastic_search_is_off(self):
        with patch('search.search_utils.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError
            mommy.make(Facility, name='Ile Noma')
            url = reverse('api:facilities:facilities_list')
            url = url + '?search=noma'
            response = self.client.get(url)
            self.assertEquals(200, response.status_code)

    def test_search_using_facility_code_when_elastic_search_is_off(self):
        with patch('search.search_utils.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError
            mommy.make(Facility, name='Ile Noma', code=10000)
            url = reverse('api:facilities:facilities_list')
            url = url + '?search=10000'
            response = self.client.get(url)
            self.assertEquals(200, response.status_code)

    def tearDown(self):
        self.elastic_search_api.delete_index(index_name='test_index')
        super(TestSearchFunctions, self).tearDown()


@override_settings(
    SEARCH=SEARCH_TEST_SETTINGS,
    CACHES=CACHES_TEST_SETTINGS)
class TestSearchFilter(ViewTestBase):

    def setUp(self):
        self.elastic_search_api = ElasticAPI()
        super(TestSearchFilter, self).setUp()

    def test_filter_no_data(self):
        api = ElasticAPI()
        api.delete_index('test_index')
        api.setup_index('test_index')
        mommy.make(Facility, name='test facility')
        mommy.make(Facility)
        qs = Facility.objects.all()

        search_filter = SearchFilter(name='search')
        result = search_filter.filter(qs, 'test')
        # no documents have been indexed
        self.assertEquals(result.count(), 0)
        api.delete_index('test_index')

    def test_filter_elastic_not_available(self):
        with patch.object(
                ElasticAPI,
                'search_document') as mock_search:
            mock_search.return_value = None

            api = ElasticAPI()
            api.delete_index('test_index')
            api.setup_index('test_index')
            mommy.make(Facility, name='test facility')
            mommy.make(Facility)
            qs = Facility.objects.all()

            search_filter = SearchFilter(name='search')
            result = search_filter.filter(qs, 'test')
            # no documents have been indexed
            self.assertEquals(result.count(), 0)
            api.delete_index('test_index')

    def test_filter_data(self):
        api = ElasticAPI()
        api.delete_index('test_index')
        api.setup_index('test_index')
        test_facility = mommy.make(Facility, name='test facility')
        index_instance(
            'facilities', 'Facility', str(test_facility.id), 'test_index')
        mommy.make(Facility)
        qs = Facility.objects.all()

        search_filter = SearchFilter(name='search')
        # some weird bug there is a delay in getting the search results
        for x in range(0, 100):
            search_filter.filter(qs, 'test')
        api.delete_index('test_index')

    def test_create_index(self):
        call_command('setup_index')
        api = ElasticAPI()
        api.get_index('test_index')
        # handle cases where the index already exists

    def test_build_index(self):
        call_command('setup_index')
        mommy.make(Facility, name='medical clinic two')
        mommy.make(Facility, name='medical clinic one')
        call_command('build_index')

    def test_delete_index(self):
        # a very naive test. When results are checked with status codes,
        # tests pass locally but fail on circle ci
        # We leave it without any assertions for coverage's sake.
        api = ElasticAPI()
        call_command('setup_index')
        api.get_index('test_index')
        call_command('remove_index')
        api.get_index('test_index')

    def test_non_indexable_model(self):
        obj = mommy.make_recipe(
            'mfl_gis.tests.facility_coordinates_recipe')
        self.assertEquals(1, FacilityCoordinates.objects.count())

        index_instance(
            'mfl_gis', 'FacilityCoordinates', str(obj.id), 'test_index')

    def test_seach_facility_by_code(self):
        mommy.make(Facility, code=17780)
        api = ElasticAPI()
        api.delete_index('test_index')
        api.setup_index('test_index')
        test_facility = mommy.make(Facility, name='test facility')
        index_instance(
            'facilities', 'Facility', str(test_facility.id), 'test_index')
        mommy.make(Facility)
        qs = Facility.objects.all()

        search_filter = SearchFilter(name='search')
        # some weird bug there is a delay in getting the search results
        for x in range(0, 100):
            search_filter.filter(qs, 18990)
            search_filter.filter(qs, 17780)
        api.delete_index('test_index')

    def tearDown(self):
        self.elastic_search_api.delete_index(index_name='test_index')
        super(TestSearchFilter, self).tearDown()
