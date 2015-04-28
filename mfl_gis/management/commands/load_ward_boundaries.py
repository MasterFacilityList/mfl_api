from django.core.management import BaseCommand, CommandError

from mfl_gis.models import WardBoundary
from common.models import Ward

from .shared import _get_mpoly_from_geom, _get_features


class Command(BaseCommand):

    def handle(self, *args, **options):
        for feature in _get_features('wards'):
            code = feature.get('COUNTY_ASS')
            name = feature.get('COUNTY_A_1')
            try:
                WardBoundary.objects.get(code=code, name=name)
                self.stdout.write(
                    "Existing boundary for {}:{}".format(code, name))
            except WardBoundary.DoesNotExist:
                try:
                    ward = Ward.objects.get(code=code)
                    WardBoundary.objects.create(
                        name=name, code=code,
                        poly=_get_mpoly_from_geom(feature.geom),
                        ward=ward
                    )
                    self.stdout.write("ADDED boundary for {}".format(name))
                except Ward.DoesNotExist:
                    raise CommandError("{}:{} NOT FOUND".format(code, name))
                except Exception as e:  # Broad catch, to print debug info
                    raise CommandError(
                        "'{}' '{}'' '{}:{}:{}' and geometry \n    {}\n".format(
                            e, feature, code, name, ward, feature.geom
                        )
                    )
