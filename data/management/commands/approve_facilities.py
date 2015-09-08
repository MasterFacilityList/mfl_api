"""
Bulk creation does not call a model's save method

Thus, some side effects such as approvals, regulation that are supposed
to take place in the save method are not effected.
This command is a work around for ensuring those side effects are
performed on the facilities.
"""
from django.core.management import BaseCommand

from facilities.models import Facility


class Command(BaseCommand):

    def handle(self, *args, **options):
        for facility in Facility.objects.all():
            facility.approved = True
            facility.is_published = True
            facility.regulated = True
            facility.save(allow_save=True)
