from django.test import TestCase
from model_mommy import mommy

from common.tests import ModelReprMixin
from mfl_gis import models


class TestModelRepr(ModelReprMixin, TestCase):

    def test_geocode_source(self):
        x = "gcs"
        self.check_repr(models.GeoCodeSource.objects.create(name=x), x)

    def test_geocode_method(self):
        x = "gcm"
        self.check_repr(models.GeoCodeMethod.objects.create(name=x), x)

    def test_facility_coordinates(self):
        f = mommy.make(models.Facility, name="fac")
        s = models.GeoCodeSource.objects.create(name="gcs")
        m = models.GeoCodeMethod.objects.create(name="gcm")
        self.check_repr(
            models.FacilityCoordinates(facility=f, source=s, method=m),
            "fac:gcs:gcm"
        )

    def test_world_border(self):
        self.check_repr(models.WorldBorder(name="world"), "world")

    def test_county_boundary(self):
        self.check_repr(models.CountyBoundary(name="county"), "county")

    def test_constituency_boundary(self):
        self.check_repr(models.ConstituencyBoundary(name="cons"), "cons")

    def test_ward_border(self):
        self.check_repr(models.WardBoundary(name="ward"), "ward")
