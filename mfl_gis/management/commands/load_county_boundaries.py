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
                    code = feature.get('COUNTY_COD')
                    name = feature.get('COUNTY_NAM')
                    try:
                        CountyBoundary.objects.get(code=code, name=name)
                        self.stdout.write(
                            "Existing boundary for {}:{}".format(code, name))
                    except CountyBoundary.DoesNotExist:
                        try:
                            county = County.objects.get(code=code, name=name)
                            CountyBoundary.objects.create(
                                name=name,
                                code=code,
                                mpoly=str(feature.geom),
                                county=county
                            )
                            self.stdout.write("+ boundary for {}".format(name))
                        except County.DoesNotExist:
                            self.stdout.write(
                                "NO county {}:{}".format(code, name))
