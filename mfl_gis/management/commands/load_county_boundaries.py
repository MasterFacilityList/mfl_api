from django.core.management import BaseCommand

from mfl_gis.models import CountyBoundary
from common.models import County

from .shared import _load_boundaries


class Command(BaseCommand):

    def handle(self, *args, **options):
        _load_boundaries(
            feature_type='counties',
            boundary_cls=CountyBoundary,
            admin_area_cls=County,
            name_field='COUNTY_NAM',
            code_field='COUNTY_COD'
        )
