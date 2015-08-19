from multiprocessing import Pool

import json

from django.utils import timezone

from django.core.management import BaseCommand
from mfl_gis.models import (
    WardBoundary, FacilityCoordinates, GeoCodeSource, GeoCodeMethod)
from facilities.models import Facility


def load_geo_code(geo_code):
    try:
        facility = Facility.objects.get(
            code=geo_code.get("facility").get("code"))
    except:
        print "Unable to locate the facility with code ".format(
            geo_code.get("facility").get("code"))
        return
    latitude = geo_code.get("latitude")
    if latitude:
        latitude = geo_code.get("latitude").replace("+", "")
    else:
        print "No latitude"

    longitude = geo_code.get("longitude")
    if longitude:
        longitude = geo_code.get("longitude").replace("+", "")
    else:
        print "No longitude"
        return
    coordinates = 'POINT({} {})'.format(longitude, latitude)
    try:
        source = GeoCodeSource.objects.get(
            name=geo_code.get("source"))
    except:
        print "Unable to locate geo code source named {}".format(
            geo_code.get("source"))
        return
    try:
        method = GeoCodeMethod.objects.get(
            name=geo_code.get("method"))
    except:
        print "Unable to locate geo code method named {}".format(
            geo_code.get("source"))
        return

    collection_date = geo_code.get(
        "collection_date", timezone.now().isoformat())
    try:
        FacilityCoordinates.objects.get_or_create(
            source=source, method=method, coordinates=coordinates,
            collection_date=collection_date, facility=facility)
    # try:
        ward_boundary = WardBoundary.objects.filter(
            mpoly__contains=coordinates)
    except ValueError:
        print "Badly formed coordinate {}".format(coordinates)
        return
    if len(ward_boundary) != 1:
            print "The coordinates are not in Kenya".format(coordinates)
            return
    else:
        facility.ward = ward_boundary[0].area
        facility.save(allow_save=True)
        print "Created successfully"


class Command(BaseCommand):

    def handle(self, *args, **options):
        geo_code_file = "/home/titan/savannah/mfl_api/data/new_data/geocodes/facility_codes.json"  # NOQA
        with open(geo_code_file) as geo_code_file:
            data = json.loads(geo_code_file.read())
            geo_codes = data[0].get("records")

            p = Pool(20)
            p.map(load_geo_code, geo_codes)
            # for geo_code in geo_codes:
            #     load_geo_code(geo_code)
