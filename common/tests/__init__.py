import json

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import default


class ViewTestBase(APITestCase):
    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.client.force_authenticate(user=self.user)
        self.maxDiff = None
        super(ViewTestBase, self).setUp()

    def _assert_response_data_equality(self, data_1, data_2):
        self.assertEquals(
            json.loads(json.dumps(data_1, default=default)),
            json.loads(json.dumps(data_2, default=default)))
