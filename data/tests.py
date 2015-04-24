from django.test import TestCase
from django.core.manament import call_command
from common.models import Ward, Constituency, County


class TestDataLoading(TestCase):
    def test_load_data(self):
        call_command('bootstrap', '../data/*')
        self.assertEquals(22, County.objects.all())
        self.assertEquals(112, Constituency.objects.all())
        self.assertEquals(543, Ward.objects.all())
