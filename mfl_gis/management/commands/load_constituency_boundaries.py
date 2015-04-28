from django.core.management import BaseCommand

from mfl_gis.models import ConstituencyBoundary
from common.models import Constituency

from .shared import _load_boundaries


class Command(BaseCommand):

    def handle(self, *args, **options):
        _load_boundaries(
            feature_type='constituencies',
            boundary_cls=ConstituencyBoundary,
            admin_area_cls=Constituency,
            name_field='CONSTITUEN',
            code_field='CONST_CODE'
        )
