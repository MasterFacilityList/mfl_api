"""
Bulk creation does not call a model's save method

Thus, some side effects such as approvals, regulation that are supposed
to take place in the save method are not effected.
This command is a work around for ensuring those side effects are
performed on the facilities.
"""
import logging
from multiprocessing import Pool
from django.core.management import BaseCommand
from django.core.exceptions import ValidationError

from facilities.models import Facility
from chul.models import CommunityHealthUnit

logger = logging.getLogger(__name__)


def update_facility(facility):
    facility.approved = True
    facility.is_published = True
    facility.regulated = True
    try:
        facility.save(allow_save=True)
    except ValidationError:
        error = "Unable to update facility {}".format(facility.code)
        logger.debug(error, exc_info=True)


def approve_chus(chu):
    chu.is_approved = True
    chu.save()


class Command(BaseCommand):

    def handle(self, *args, **options):
        def do_approve_facilities():
            for facility in Facility.objects.all():
                update_facility(facility)

        def approve_community_units():
            q = Pool(5)
            q.map(approve_chus, CommunityHealthUnit.objects.all())

        do_approve_facilities()
        approve_community_units()
