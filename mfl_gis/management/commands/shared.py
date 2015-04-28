import os
import json
import logging

from django.contrib.gis.gdal.geometries import Polygon as GDALPolygon
from django.contrib.gis.gdal.geometries import MultiPolygon as GDALMultiPolygon
from django.contrib.gis.geos import MultiPolygon
from django.core.management import CommandError
from django.contrib.gis.gdal import DataSource


COMBINED_GEOJSON = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)  # Folder with this file i.e 'commands'
        )  # Parent of folder where this file is i.e 'management'
    ),  # The application folder itself i.e mfl_gis
    'data/kenya_gis_formatted.json'
)
LOGGER = logging.getLogger(__name__)


def _get_features(feature_type):
    """Get 'counties', 'constituencies' or 'wards' features"""
    with open(COMBINED_GEOJSON) as f:
        combined = json.load(f)

        LOGGER.debug('Feature keys: {}'.format(combined.keys()))

        # Easier to comprehend than a nested list comprehension
        features = []
        for feature in combined[feature_type]:
            try:
                ds = DataSource(feature)
            except:
                # Handle special cases in IEBC data
                LOGGER.error(
                    'Unable to process {} {}'.format(feature_type, feature))
                continue

            for layer in ds:
                for feature in layer:
                    features.append(feature)

        return features


def _get_mpoly_from_geom(geom):
    """Coerce polygons into multipolygons to get past GeoDjango validation"""
    if type(geom) == GDALPolygon:
        return MultiPolygon(geom.geos)
    elif type(geom) == GDALMultiPolygon:
        return geom.geos
    else:
        raise CommandError(
            'Expected a Polygon or MultiPolygon, got {}'.format(
                type(geom)
            )
        )


def _load_boundaries(
        feature_type, boundary_cls, admin_area_cls, name_field, code_field):
    """
    A generic routine to load Kenyan geographic feature boundaries

    It is used for counties, constituencies and wards

    :param: feature_type - one of `ward`, `constituency` or `county`
    :param: boundary_cls - e.g `WardBoundary`
    :param: admin_area_cls e.g `Ward`
    :param: code_field e.g `COUNTY_A_1` contains the names of wards
    :param: name_field e.g `COUNTY_ASS` contains the ward codes
    """
    if feature_type not in ['counties', 'constituencies', 'wards']:
        raise CommandError('Invalid feature type "{{"'.format(feature_type))

    features = _get_features(feature_type)
    LOGGER.debug('{} features found'.format(len(features)))
    for feature in features:
        code = feature.get(name_field)
        name = feature.get(code_field)
        LOGGER.debug('Code: {} Name: {}'.format(code, name))
        try:
            boundary = boundary_cls.objects.get(code=code, name=name)
            LOGGER.debug("Existing boundary {}".format(boundary))
        except boundary_cls.DoesNotExist:
            try:
                admin_area = admin_area_cls.objects.get(code=code)
                boundary_cls.objects.create(
                    name=name,
                    code=code,
                    mpoly=_get_mpoly_from_geom(feature.geom),
                    ward=admin_area
                )
                LOGGER.debug("ADDED boundary for {}".format(admin_area))
            except admin_area_cls.DoesNotExist:
                raise CommandError(
                    "{} {}:{} NOT FOUND".format(admin_area_cls, code, name))
            except Exception as e:  # Broad catch, to print debug info
                raise CommandError(
                    "'{}' '{}'' '{}:{}:{}' and geometry \n    {}\n".format(
                        e, feature, code, name, admin_area_cls, feature.geom
                    )
                )
