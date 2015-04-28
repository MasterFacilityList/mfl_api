import os
import json

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
    County,
    name=seq('NAIROBI'),
    code=seq(470)
)

county_boundary_recipe = Recipe(
    CountyBoundary,
    county=foreign_key(county_recipe),
    name=seq('NAIROBI'),
    code=seq(470),
    mpoly=_get_mpoly_from_geom(COUNTY_BORDER[0].get_geoms()[0])
)

constituency_recipe = Recipe(
    Constituency,
    area=foreign_key(county_recipe),
    name=seq('DAGORETTI NORTH'),
    code=seq(2750)
)

constituency_boundary_recipe = Recipe(
    ConstituencyBoundary,
    constituency=foreign_key(constituency_recipe),
    name=seq('DAGORETTI NORTH'),
    code=seq(2750),
    mpoly=_get_mpoly_from_geom(CONSTITUENCY_BORDER[0].get_geoms()[0])
)


ward_recipe = Recipe(
    Ward,
    area=foreign_key(constituency_recipe),
    name=seq('KILIMANI'),
    code=seq(13710)
)

ward_boundary_recipe = Recipe(
    WardBoundary,
    ward=foreign_key(ward_recipe),
    name=seq('KILIMANI'),
    code=seq(13710),
    mpoly=_get_mpoly_from_geom(WARD_BORDER[0].get_geoms()[0])
)


facility_recipe = Recipe(
    Facility,
    ward=foreign_key(ward_recipe)
)

facility_coordinates_recipe = Recipe(
    FacilityCoordinates,
    facility=foreign_key(facility_recipe),
    coordinates=Point(-1.295241, 36.805127)
)
