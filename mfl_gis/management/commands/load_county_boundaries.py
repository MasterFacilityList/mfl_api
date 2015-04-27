import os
import json

from django.contrib.gis.gdal import DataSource
from django.core.management import BaseCommand

from mfl_gis.models import CountyBoundary
from common.models import County

COMBINED_GEOJSON = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)  # Folder with this file i.e 'commands'
        )  # Parent of folder where this file is i.e 'management'
    ),  # The application folder itself i.e mfl_gis
    'data/kenya_gis_formatted.json'
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(COMBINED_GEOJSON) as f:
            combined = json.load(f)

        for county in combined['counties']:
            for layer in DataSource(county):
                for feature in layer:
                    try:
                        CountyBoundary.objects.get(
                            code=feature.get('COUNTY_COD'),
                            name=feature.get('COUNTY_NAM')
                        )
                        self.stdout.write(
                            "County with id {} and name {} EXISTS".format(
                                feature.get('COUNTY_COD'),
                                feature.get('COUNTY_NAM')
                            )
                        )
                    except CountyBoundary.DoesNotExist:
                        try:
                            county = County.objects.get(
                                code=feature.get('COUNTY_COD'),
                                name=feature.get('COUNTY_NAM')
                            )
                            CountyBoundary.objects.create(
                                name=feature.get('COUNTY_NAM'),
                                code=feature.get('COUNTY_COD'),
                                mpoly=str(feature.geom),
                                county=county
                            )
                            self.stdout.write(
                                "ADDED boundary for {}".format(
                                    feature.get('COUNTY_NAM')
                                )
                            )
                        except County.DoesNotExist:
                            self.stdout.write(
                                "NO county with id {} and name {}".format(
                                    feature.get('COUNTY_COD'),
                                    feature.get('COUNTY_NAM')
                                )
                            )
