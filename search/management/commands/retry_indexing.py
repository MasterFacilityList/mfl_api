from django.core.management import BaseCommand
from ...tasks import retry_indexing


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        retry_indexing()
