import os

from django.contrib.gis.geos import Point
from django.contrib.gis.gdal import DataSource
from model_mommy.recipe import Recipe, foreign_key, seq

from common.models import County, Constituency, Ward
from facilities.models import Facility

from mfl_gis.management.commands.shared import _get_mpoly_from_geom

from ..models import (
    FacilityCoordinates,
    CountyBoundary,
    ConstituencyBoundary,
    WardBoundary
)

CUR_DIR = os.path.dirname(__file__)
COUNTY_BORDER = DataSource(
    os.path.join(CUR_DIR, 'nairobi_county_boundary.geojson'))
CONSTITUENCY_BORDER = DataSource(
    os.path.join(CUR_DIR, 'dagoretti_north_constituency_boundary.geojson'))
WARD_BORDER = DataSource(
    os.path.join(CUR_DIR, 'kilimani_ward_boundary.geojson'))


county_recipe = Recipe(
    County
)

county_boundary_recipe = Recipe(
    CountyBoundary,
    area=foreign_key(county_recipe),
    mpoly=_get_mpoly_from_geom(COUNTY_BORDER[0].get_geoms()[0])
)

constituency_recipe = Recipe(
    Constituency,
    county=foreign_key(county_recipe),
)

constituency_boundary_recipe = Recipe(
    ConstituencyBoundary,
    area=foreign_key(constituency_recipe),
    mpoly=_get_mpoly_from_geom(CONSTITUENCY_BORDER[0].get_geoms()[0])
)


ward_recipe = Recipe(
    Ward,
    constituency=foreign_key(constituency_recipe)
)

ward_boundary_recipe = Recipe(
    WardBoundary,
    area=foreign_key(ward_recipe),
    mpoly=_get_mpoly_from_geom(WARD_BORDER[0].get_geoms()[0])
)

MEMOIZED_WARD = None


def _get_ward():
    """We need to use the same ward each time we make a facility"""
    global MEMOIZED_WARD  # Yikes!
    if not MEMOIZED_WARD:
        MEMOIZED_WARD = ward_recipe.make()
        ward_boundary_recipe.make(ward=MEMOIZED_WARD)

    return MEMOIZED_WARD


facility_recipe = Recipe(
    Facility,
    ward=_get_ward
)

facility_coordinates_recipe = Recipe(
    FacilityCoordinates,
    facility=foreign_key(facility_recipe),
    coordinates=Point(-1.295241, 36.805127)
)
