from django.core.management import BaseCommand
from common.models import Town, Ward, Constituency
from facilities.models import Facility, RegulatingBody


class Command(BaseCommand):

    def handle(self, *args, **options):
        mathare = Constituency.objects.get(code=290)
        kamukunji = Constituency.objects.get(code=288)
        starehe = Constituency.objects.get(code=289)

        for ward in Ward.objects.filter(constituency=mathare):
            for town in Town.objects.all()[0:10]:
                town.ward = ward
                town.save()

        for ward in Ward.objects.filter(constituency=kamukunji):
            for town in Town.objects.all()[10:20]:
                town.ward = ward
                town.save()

        for ward in Ward.objects.filter(constituency=starehe):
            for town in Town.objects.all()[20:30]:
                town.ward = ward
                town.save()

        regulatory_body = RegulatingBody.objects.get(
            name="Kenya MPDB - Institution")
        for facility in Facility.objects.filter(ward__constituency=mathare):
            facility.regulatory_body = regulatory_body
            facility.save(allow_save=True)
        for facility in Facility.objects.filter(ward__constituency=kamukunji):
            facility.regulatory_body = regulatory_body
            facility.save(allow_save=True)
        for facility in Facility.objects.filter(ward__constituency=starehe):
            facility.regulatory_body = regulatory_body
            facility.save(allow_save=True)
        print "Finished"
