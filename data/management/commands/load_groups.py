from django.core.management import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):

    def handle(self, *args, **options):
        Group.objects.get_or_create(
            name="County Health Records Information Officer")
        Group.objects.get_or_create(
            name="Sub County Health Records Information Officer")
        Group.objects.get_or_create(
            name="National Users")
