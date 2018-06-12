from django.contrib.auth import get_user_model
from django.test import TestCase
from model_mommy import mommy

from common.fields import SequenceField
from common.models import County


class SequenceFieldTest(TestCase):
    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.test_model = County(name='test county')
        self.test_model.save()

    def test_get_prepared_value(self):
        seq = SequenceField()
        self.assertEqual(seq.get_prep_value(value=''), None)
