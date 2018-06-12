import json
import six

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import default


class ViewTestBase(APITestCase):

    def setUp(self):
        self.admin_group = mommy.make(Group, name="mfl admins")
        view_fields_perm = Permission.objects.get(
            codename='view_all_facility_fields')
        self.admin_group.permissions.add(view_fields_perm.id)
        self.user = mommy.make(get_user_model())
        self.user.groups.add(self.admin_group)
        self.client.force_authenticate(user=self.user)
        self.maxDiff = None
        super(ViewTestBase, self).setUp()

    def _assert_response_data_equality(self, data_1, data_2):
        self.assertEquals(
            json.loads(json.dumps(data_1, default=default)),
            json.loads(json.dumps(data_2, default=default)))


class ModelReprMixin(object):

    def check_repr(self, instance, expected):
        self.assertEqual(str(instance), expected)
        self.assertEqual(instance.__str__(), expected)
        if six.PY2:  # pragma: no cover
            self.assertEqual(instance.__unicode__(), expected)
