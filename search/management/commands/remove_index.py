from django.core.management import BaseCommand
from search.search_utils import ElasticAPI


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        api = ElasticAPI()
        api.delete_index()
