import os

from django.core.management import BaseCommand
from django.contrib.gis.utils import LayerMapping

from mfl_gis.models import WorldBorder

WORLD_SHAPEFILE = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)  # Folder with this file i.e 'commands'
        )  # Parent of folder where this file is i.e 'management'
    ),  # The application folder itself i.e mfl_gis
    'data/world/TM_WORLD_BORDERS-0.3.shp'
)
WORLD_SHAPEFILE_MODEL_MAPPING = {
    'name': 'NAME',
    'code': 'ISO3',  # We could have used the ISO2 code also
    'mpoly': 'MULTIPOLYGON',
    'longitude': 'LON',
    'latitude': 'LAT'
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        wb_count = WorldBorder.objects.count()
        if wb_count:
            self.stdout.write(
                '{} countries already exist'.format(wb_count))
            return

        lm = LayerMapping(
            WorldBorder,
            WORLD_SHAPEFILE,
            WORLD_SHAPEFILE_MODEL_MAPPING,
            transform=False,
            encoding='iso-8859-1'
        )
        lm.save(strict=True, verbose=False)
        self.stdout.write("Loaded world borders")
