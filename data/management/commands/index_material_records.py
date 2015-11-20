"""
Does the initial indexing of the records in material view
"""
import logging

from django.core.management import BaseCommand

from facilities.models import FacilityExportExcelMaterialView
from search.search_utils import index_instance

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for record in FacilityExportExcelMaterialView.objects.all():
            index_instance(record)
            logger.info("indexed instance {0}".format(record.name))
