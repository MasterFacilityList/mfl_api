from django.core.management import BaseCommand
from facilities.models import Service


class Command(BaseCommand):

    def handle(self, *args, **options):
        for service in Service.objects.all():
            service.assign_options()
