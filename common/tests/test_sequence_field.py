from django.contrib.auth import get_user_model
from django.core import exceptions
from django.test import TestCase
from model_mommy import mommy

from common.fields import SequenceField
from common.models import Currency


class SequenceFieldTest(TestCase):
    def setUp(self):
        self.user = mommy.make(get_user_model())
        self.test_model = FakeTestModel(
            created_by=self.user, owner=1, updated_by=self.user,
            currency=mommy.make(Currency))
        self.test_model.save()

    def test_code_generation(self):
        self.assertEquals(self.test_model.document_code, 1)

    def test_invalid_type(self):
        with self.assertRaises(exceptions.ValidationError):
            self.test_model.document_code = 'z'
            self.test_model.save()

    def test_get_prepared_value(self):
        seq = SequenceField()
        self.assertEqual(seq.get_prep_value(value=''), None)
