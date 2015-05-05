from django.core.management import BaseCommand
from common.utilities.search_utils import ElasticAPI
from facilities.models impo


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        api = ElasticAPI()
        api.setup_index()
