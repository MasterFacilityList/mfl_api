import os
import json
from django.contrib.gis.db import models as gis_models
from django.utils import timezone

from django.core.management import BaseCommand
from mfl_gis.models import WardBoundary, FacilityCoordinates, GeoCodeSource, GeoCodeMethod
from facilities.models import Facility


class Command(BaseCommand):

    def handle(self, *args, **options):
        geo_code_file = "/home/titan/savannah/mfl_api/data/new_data/geocodes/facility_codes.json"
        with open(geo_code_file) as geo_code_file:
            data = json.loads(geo_code_file.read())
            geo_codes = data[0].get("records")
            for geo_code in geo_codes:
                try:
                    facility = Facility.objects.get(
                        code=geo_code.get("facility").get("code"))
                except:
                    print "Unable to locate the facility with code ".format(
                        geo_code.get("facility").get("code"))
                    continue
                latitude = geo_code.get("latitude")
                if latitude:
                    latitude = geo_code.get("latitude").replace("+", "")
                else:
                    print "No latitude"
                    continue
                longitude = geo_code.get("longitude")
                if longitude:
                    longitude = geo_code.get("longitude").replace("+", "")
                else:
                    print "No longitude"
                    continue
                coordinates = 'POINT({} {})'.format(longitude, latitude)
                try:
                    source = GeoCodeSource.objects.get(
                        name=geo_code.get("source"))
                except:
                    print "Unable to locate geo code source named {}".format(geo_code.get("source"))
                    continue
                try:
                    method = GeoCodeMethod.objects.get(
                        name=geo_code.get("method"))
                except:
                    print "Unable to locate geo code method named {}".format(geo_code.get("source"))
                    continue

                collection_date = geo_code.get("collection_date", timezone.now().isoformat())
                try:
                    fc = FacilityCoordinates.objects.get_or_create(
                        source=source, method=method, coordinates=coordinates,
                        collection_date=collection_date, facility=facility)
                # try:
                    ward_boundary = WardBoundary.objects.filter(mpoly__contains=coordinates)
                except ValueError:
                    print "Badly formed coordinate {}".format(coordinates)
                    continue
                if len(ward_boundary) != 1:
                        print "The coordinates is not in Kenya".format(coordinates)
                        continue
                else:
                    facility.ward = ward_boundary[0].area
                    facility.save(allow_save=True)
                    print "Created successfully"
