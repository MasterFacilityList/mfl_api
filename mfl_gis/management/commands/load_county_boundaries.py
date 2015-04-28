from django.core.management import BaseCommand, CommandError

from mfl_gis.models import CountyBoundary
from common.models import County

from .shared import _get_mpoly_from_geom, _get_features


class Command(BaseCommand):

    def handle(self, *args, **options):
        for feature in _get_features('counties'):
            code = feature.get('COUNTY_COD')
            name = feature.get('COUNTY_NAM')
            try:
                CountyBoundary.objects.get(code=code, name=name)
                self.stdout.write(
                    "Existing boundary for {}:{}".format(code, name))
            except CountyBoundary.DoesNotExist:
                try:
                    county = County.objects.get(code=code)
                    CountyBoundary.objects.create(
                        name=name, code=code,
                        mpoly=_get_mpoly_from_geom(feature.geom),
                        county=county
                    )
                    self.stdout.write(
                        "ADDED boundary for county {}".format(name))
                except County.DoesNotExist:
                    raise CommandError("{}:{} NOT FOUND".format(code, name))
                except Exception as e:  # Broad catch, to print debug info
                    raise CommandError(
                        "'{}' '{}'' '{}:{}:{}' and geometry \n    {}\n".format(
                            e, feature, code, name, county, feature.geom
                        )
                    )
