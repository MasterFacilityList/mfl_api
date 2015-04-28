from django.core.management import BaseCommand

from mfl_gis.models import CountyBoundary, ConstituencyBoundary, WardBoundary
from common.models import County, Constituency, Ward

from .shared import _load_boundaries


class Command(BaseCommand):
    """Load the boundaries of counties, constituencies and wards"""

    def handle(self, *args, **options):
        _load_boundaries(
            feature_type='counties',
            boundary_cls=CountyBoundary,
            admin_area_cls=County,
            name_field='COUNTY_NAM',
            code_field='COUNTY_COD'
        )
        _load_boundaries(
            feature_type='constituencies',
            boundary_cls=ConstituencyBoundary,
            admin_area_cls=Constituency,
            name_field='CONSTITUEN',
            code_field='CONST_CODE'
        )
        _load_boundaries(
            feature_type='wards',
            boundary_cls=WardBoundary,
            admin_area_cls=Ward,
            name_field='COUNTY_A_1',
            code_field='COUNTY_ASS'
        )
