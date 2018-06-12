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

    # Easier to comprehend than a nested list comprehension
    features = []
    for feature in combined[feature_type]:
        try:
            features.extend(
                [feature for layer in DataSource(feature) for feature in layer]
            )
        except:
            # Handle special cases in IEBC data
            LOGGER.error(
                'Unable to process {} {}'.format(feature_type, feature))
            continue

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


def _feature_has_ward_name(feature):
    """Because I am too lazy to monkey-patch feature [ GeoDjango ]"""
    try:
        return True if feature.get('Ward_Name') else False
    except:
        return False


def _get_code_and_name(feature, name_field, code_field):
    """This exists solely for the purpose of handling 'special cases'

    i.e. compensating for inconsistencies in IEBC sourced GeoJSON
    """
    # Special cases
    malformed_geojson_wards = [
        {
            'OBJECTID': 5763,
            'Ward_Name': 'GITOTHUA',
            'CODE': 569
        },
        {
            'OBJECTID': 5763,
            'Ward_Name': 'BIASHARA',
            'CODE': 570
        },
        {
            'OBJECTID': 3219,
            'Ward_Name': 'GATONGORA',
            'CODE': 571
        },
        {
            'OBJECTID': 3219,
            'Ward_Name': 'KAHAWA/SUKARI',
            'CODE': 572
        },
        {
            'OBJECTID': 3219,
            'Ward_Name': 'KAHAWA WENDANI',
            'CODE': 573
        },
        {
            'OBJECTID': 3219,
            'Ward_Name': 'KIUU',
            'CODE': 574
        },
        {
            'OBJECTID': 3219,
            'Ward_Name': 'MWIKI',
            'CODE': 575
        },
        {
            'OBJECTID': 3219,
            'Ward_Name': 'MWIHOKO',
            'CODE': 576
        }
    ]

    # Inefficient, but this is used in a one off operation
    for ward in malformed_geojson_wards:
        if (
            _feature_has_ward_name(feature) and
            feature.get('OBJECTID') == ward['OBJECTID'] and
            feature.get('Ward_Name') == ward['Ward_Name']
        ):
            return ward['CODE'], ward['Ward_Name']

    return feature.get(code_field), feature.get(name_field)


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
    errors = []
    unsaved_instances = {}

    for feature in _get_features(feature_type):
        try:
            code, name = _get_code_and_name(feature, name_field, code_field)
            boundary = boundary_cls.objects.get(code=code, name=name)
            LOGGER.debug("Existing boundary for '{}'".format(boundary))
        except boundary_cls.DoesNotExist:
            try:
                admin_area = admin_area_cls.objects.get(code=code)
                unsaved_instances[code] = boundary_cls(
                    name=name,
                    code=code,
                    mpoly=_get_mpoly_from_geom(feature.geom),
                    area=admin_area
                )
                LOGGER.debug("ADDED boundary for '{}'".format(admin_area))
            except admin_area_cls.DoesNotExist:
                errors.append(
                    "{} {}:{} NOT FOUND".format(admin_area_cls, code, name))

    if unsaved_instances:
        boundary_cls.objects.bulk_create(unsaved_instances.values())
    if errors:
        raise CommandError('\n'.join(errors))
