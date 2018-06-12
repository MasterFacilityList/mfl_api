import os

from django.contrib.gis.geos import Point
from django.contrib.gis.gdal import DataSource
from model_mommy.recipe import Recipe, foreign_key

from common.models import County, Constituency, Ward
from facilities.models import Facility

from mfl_gis.management.commands.shared import _get_mpoly_from_geom

from ..models import (
    FacilityCoordinates,
    WorldBorder,
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
KENYA_BORDER = DataSource(
    os.path.join(CUR_DIR, 'kenya_boundary.geojson'))


country_boundary_recipe = Recipe(
    WorldBorder,
    mpoly=_get_mpoly_from_geom(KENYA_BORDER[0].get_geoms()[0])
)


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


def _get_ward():
    """We need to use the same ward each time we make a facility"""
    ward = ward_recipe.make()

    ward_boundary_recipe.make(area=ward)
    constituency_boundary_recipe.make(area=ward.constituency)
    county_boundary_recipe.make(area=ward.constituency.county)

    try:
        WorldBorder.objects.get(code='KEN')
    except WorldBorder.DoesNotExist:
        country_boundary_recipe.make(code='KEN')

    return ward


facility_recipe = Recipe(
    Facility,
    ward=_get_ward
)

facility_coordinates_recipe = Recipe(
    FacilityCoordinates,
    facility=foreign_key(facility_recipe),
    coordinates=Point(36.78378206656476, -1.2840274151085824)  # x, y
)
