from django.test import TestCase

from ..utilities.sequence_helper import SequenceGenerator
from ..models import County


class SequenceTestCase(TestCase):
    def test_sequence_creation(self):
        seq = SequenceGenerator(model=County)
        self.assertEquals(seq.next(), 1)
