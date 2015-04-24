import os

from django.test import TestCase
from django.core.management import call_command
from django.conf import settings

from common.models import Ward, Constituency, County


class TestDataLoading(TestCase):
    def test_load_data(self):
        county_files = os.path.join(
            settings.BASE_DIR, 'data/data/0001_counties.json')
        constituencies_files = os.path.join(
            settings.BASE_DIR, 'data/data/0002_constituencies.json')
        owners_files = os.path.join(
            settings.BASE_DIR, 'data/data/0003_facility_owners.json')
        status_files = os.path.join(
            settings.BASE_DIR, 'data/data/0004_facility_status.json')
        geo_code_files = os.path.join(
            settings.BASE_DIR, 'data/data/0005_geo_codes_methods.json')
        service_cat_files = os.path.join(
            settings.BASE_DIR, 'data/data/0007_service_categories.json')
        services = os.path.join(
            settings.BASE_DIR, 'data/data/0008_the_services.json')
        wards_files = os.path.join(
            settings.BASE_DIR, 'data/data/0009_wards.json')
        job_titles = os.path.join(
            settings.BASE_DIR, 'data/data/0006_job_titles.json')

        call_command('bootstrap', county_files)
        call_command('bootstrap', constituencies_files)
        call_command('bootstrap', owners_files)
        call_command('bootstrap', status_files)
        call_command('bootstrap', geo_code_files)
        call_command('bootstrap', service_cat_files)
        call_command('bootstrap', services)
        call_command('bootstrap', wards_files)
        call_command('bootstrap', job_titles)

        self.assertEquals(22, County.objects.all().count())
        self.assertEquals(112, Constituency.objects.all().count())
        self.assertEquals(543, Ward.objects.all().count())
