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
    if feature_type not in ['counties', 'constituencies', 'wards']:
        raise CommandError('Invalid feature type "{{"'.format(feature_type))

    with open(COMBINED_GEOJSON) as f:
        combined = json.load(f)

        # Easier to comprehend than a nested list comprehension
        features = []
        for feature in combined[feature_type]:
            try:
                ds = DataSource(feature)
            except:
                # Handle special cases in IEBC data
                LOGGER.error(
                    'Unable to process {} {}'.format(feature_type, feature))
                break

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
