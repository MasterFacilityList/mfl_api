from django.core.management import BaseCommand

from mfl_gis.models import WardBoundary
from common.models import Ward

from .shared import _load_boundaries


class Command(BaseCommand):

    def handle(self, *args, **options):
        _load_boundaries(
            feature_type='wards',
            boundary_cls=WardBoundary,
            admin_area_cls=Ward,
            name_field='COUNTY_ASS',
            code_field='COUNTY_A_1'
        )
