from django.core.management import BaseCommand, CommandError

from mfl_gis.models import ConstituencyBoundary
from common.models import Constituency

from .shared import _get_mpoly_from_geom, _get_features


class Command(BaseCommand):

    def handle(self, *args, **options):
        for feature in _get_features('constituencies'):
            code = feature.get('CONST_CODE')
            name = feature.get('CONSTITUEN')
            try:
                ConstituencyBoundary.objects.get(code=code, name=name)
                self.stdout.write(
                    "Existing boundary for {}:{}".format(code, name))
            except ConstituencyBoundary.DoesNotExist:
                try:
                    constituency = Constituency.objects.get(code=code)
                    ConstituencyBoundary.objects.create(
                        name=name, code=code,
                        mpoly=_get_mpoly_from_geom(feature.geom),
                        constituency=constituency
                    )
                    self.stdout.write(
                        "ADDED boundary for constituency {}".format(name))
                except Constituency.DoesNotExist:
                    raise CommandError("{}:{} NOT FOUND".format(code, name))
                except Exception as e:  # Broad catch, to print debug info
                    raise CommandError(
                        "'{}' '{}'' '{}:{}:{}' and geometry \n    {}\n".format(
                            e, feature, code, name, constituency, feature.geom
                        )
                    )
