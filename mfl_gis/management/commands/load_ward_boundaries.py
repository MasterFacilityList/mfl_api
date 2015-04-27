import os
import json

from django.contrib.gis.gdal import DataSource
from django.core.management import BaseCommand, CommandError

from mfl_gis.models import WardBoundary
from common.models import Ward

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

        # Easier to comprehend than a nested list comprehension
        ward_features = []
        for ward in combined['wards']:
            try:
                ds = DataSource(ward)
            except:
                # Handle special case in IEBC data
                print('Unable to process ward "{}"'.format(ward))
                break

            for layer in ds:
                for feature in layer:
                    ward_features.append(feature)

        return ward_features


class Command(BaseCommand):

    def handle(self, *args, **options):
        for feature in _get_features():
            code = feature.get('COUNTY_ASS')
            name = feature.get('COUNTY_A_1')
            try:
                WardBoundary.objects.get(code=code, name=name)
                self.stdout.write(
                    "Existing boundary for {}:{}".format(code, name))
            except WardBoundary.DoesNotExist:
                try:
                    ward = Ward.objects.get(
                        code=code, name=name)
                    WardBoundary.objects.create(
                        name=name, code=code, mpoly=str(feature.geom),
                        ward=ward
                    )
                    self.stdout.write("ADDED boundary for {}".format(name))
                except Ward.DoesNotExist:
                    raise CommandError("{}:{} NOT FOUND".format(code, name))
