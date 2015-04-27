import os
import json

from django.contrib.gis.gdal import DataSource
from django.core.management import BaseCommand, CommandError

from mfl_gis.models import ConstituencyBoundary
from common.models import Constituency

COMBINED_GEOJSON = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)  # Folder with this file i.e 'commands'
        )  # Parent of folder where this file is i.e 'management'
    ),  # The application folder itself i.e mfl_gis
    'data/kenya_gis_formatted.json'
)


def _get_features():
    with open(COMBINED_GEOJSON) as f:
        combined = json.load(f)

        constituency_features = []
        for constituency in combined['constituencies']:
            for layer in DataSource(constituency):
                for feature in layer:
                    constituency_features.append(feature)

        return constituency_features


class Command(BaseCommand):

    def handle(self, *args, **options):
        for feature in _get_features():
            code = feature.get('CONST_CODE')
            name = feature.get('CONSTITUEN')
            try:
                ConstituencyBoundary.objects.get(code=code, name=name)
                self.stdout.write(
                    "Existing boundary for {}:{}".format(code, name))
            except ConstituencyBoundary.DoesNotExist:
                try:
                    constituency = Constituency.objects.get(
                        code=code, name=name)
                    ConstituencyBoundary.objects.create(
                        name=name, code=code, mpoly=str(feature.geom),
                        constituency=constituency
                    )
                    self.stdout.write("ADDED boundary for {}".format(name))
                except Constituency.DoesNotExist:
                    raise CommandError("{}:{} NOT FOUND".format(code, name))
