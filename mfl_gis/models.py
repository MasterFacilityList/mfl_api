import logging
import json
import reversion

from django.db import models as db_models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db.models import Union
from django.contrib.gis.geos import MultiPolygon
from django.utils import timezone, encoding
from rest_framework.exceptions import ValidationError
from common.models import AbstractBase, County, Constituency, Ward
from facilities.models import Facility


LOGGER = logging.getLogger(__name__)


class CoordinatesValidatorMixin(object):

    def validate_long_and_lat_within_kenya(self):
        try:
            boundary = WorldBorder.objects.get(code='KEN')
            if not boundary.mpoly.contains(self.coordinates):
                # This validation was relaxed ( temporarily? )
                # The Kenyan boundaries that we have loaded have low fidelity
                # at the edges, so that facilities that are, say, 100 meters
                # from the border are reported as not in Kenya
                # If higher fidelity map data is obtained, this validation
                # can be brought back
                LOGGER.error(
                    '{0} is not within the Kenyan boundaries that we have'
                    .format(self.coordinates)
                )
        except WorldBorder.DoesNotExist:
            raise ValidationError('Setup error: Kenyan boundaries not loaded')

    def _validate_within_boundaries(self, boundary_model, area, raise_not_found=True):  # noqa
        try:
            boundary = boundary_model.objects.get(area=area)
            if not boundary.mpoly.contains(self.coordinates):
                raise ValidationError({
                    "coordinates": [
                        '({0}, {1}) not contained in boundary of {2}'.format(
                            self.coordinates.x, self.coordinates.y, area
                        )
                    ]
                })
        except boundary_model.DoesNotExist:
            LOGGER.error('{0} does not have boundary info'.format(area))
            if raise_not_found:
                raise ValidationError({
                    'coordinates': [
                        'No boundary information for {0}'.format(area)
                    ]
                })

    def validate_long_and_lat_within_constituency(self, constituency):
        self._validate_within_boundaries(ConstituencyBoundary, constituency)

    def validate_long_and_lat_within_county(self, county):
        self._validate_within_boundaries(CountyBoundary, county)

    def validate_long_and_lat_within_ward(self, ward):
        self._validate_within_boundaries(WardBoundary, ward, False)


class CustomGeoManager(gis_models.GeoManager):

    """
    Ensure that deleted items are not returned in a gis queryset  by default
    """

    def get_queryset(self):
        return super(
            CustomGeoManager, self).get_queryset().filter(deleted=False)


class GISAbstractBase(AbstractBase, gis_models.Model):

    """
    We've intentionally duplicated the `AbstractBase` in the `common` app
    because we wanted to confine the impact of GIS ( Geographic ) stuff
    to this app.

    The GIS stuff should have only one touch-point with the rest of the
    models: the link to the Facility model.

    We've kept the fields that are in the `common` `AbstractBase` because
    we want to have the same kind of base behavior.
    """
    objects = CustomGeoManager()
    everything = gis_models.GeoManager()

    class Meta(AbstractBase.Meta):
        abstract = True


@reversion.register
@encoding.python_2_unicode_compatible
class GeoCodeSource(GISAbstractBase):

    """
    Where the geo-code came from.

    This is the organization collecting the code.
    For example, DHMT, the Service Availability Mapping survey (SAM),
    Kenya Medical Research Institute (KEMRI), the Regional Center for
    Mapping of Resources for Development (RCMRD), the AIDS, Population
    and Health Integrated Assistance (APHIA) II, or another source.
    It is not the individual who collected the code
    """
    name = gis_models.CharField(
        max_length=100, unique=True,
        help_text="The name of the collecting organization")
    description = gis_models.TextField(
        help_text="A short summary of the collecting organization",
        null=True, blank=True)
    abbreviation = gis_models.CharField(
        max_length=10, null=True, blank=True,
        help_text="An acronym of the collecting or e.g SAM")

    def __str__(self):
        return self.name


@reversion.register
@encoding.python_2_unicode_compatible
class GeoCodeMethod(GISAbstractBase):

    """
    Method used to capture the geo-code.

    Examples:
        1= Taken with GPS device,
        2= Calculated from proximity to school, village, markets
        3= Calculated from 1:50,000 scale topographic maps,
        4= Scanned from hand-drawn maps,
        5= Centroid calculation from sub-location
        8= No geo-code
        9= Other
    """
    name = gis_models.CharField(
        max_length=100, unique=True, help_text="The name of the method.")
    description = gis_models.TextField(
        help_text="A short description of the method",
        null=True, blank=True)

    def __str__(self):
        return self.name


@reversion.register(follow=['facility', 'source', 'method', ])
@encoding.python_2_unicode_compatible
class FacilityCoordinates(CoordinatesValidatorMixin, GISAbstractBase):

    """
    Location derived by the use of GPS satellites and GPS device or receivers.

    It is three dimensional.
    The three-dimensional readings from a GPS device are latitude, longitude,
    and attitude. The date/time the reading is done is also important, as
    is the source and method of the reading.
    """
    facility = gis_models.OneToOneField(
        Facility, related_name='facility_coordinates_through', unique=True)
    coordinates = gis_models.PointField()
    source = gis_models.ForeignKey(
        GeoCodeSource, null=True, blank=True,
        help_text="where the geo code came from", on_delete=gis_models.PROTECT)
    method = gis_models.ForeignKey(
        GeoCodeMethod, null=True, blank=True,
        help_text="Method used to obtain the geo codes. e.g"
        " taken with GPS device")
    collection_date = gis_models.DateTimeField(default=timezone.now)

    @property
    def simplify_coordinates(self):
        return {
            "coordinates": [
                float('%.2f' % round(self.coordinates[0], 2)),
                float('%.2f' % round(self.coordinates[1], 2))
            ]
        }

    @property
    def json_features(self):
        return {
            "geometry": self.simplify_coordinates,
        }

    def clean(self):
        self.validate_long_and_lat_within_kenya()
        self.validate_long_and_lat_within_county(
            self.facility.ward.constituency.county)
        self.validate_long_and_lat_within_constituency(
            self.facility.ward.constituency)
        self.validate_long_and_lat_within_ward(
            self.facility.ward)
        super(FacilityCoordinates, self).clean()

    def __str__(self):
        return "{}:{}:{}".format(self.facility, self.source, self.method)

    class Meta(GISAbstractBase.Meta):
        verbose_name_plural = 'facility coordinates'
        verbose_name = 'facility coordinates'


class AdministrativeUnitBoundary(GISAbstractBase):

    """Base class for the models that implement administrative boundaries

    All common operations and fields are here.
    We retain the default SRID ( 4326 - WGS84 ).
    """

    # 3 decimal places for the web map ( about 10 meter accuracy )
    PRECISION = 3
    TOLERANCE = (1.0 / 10 ** PRECISION)

    # These two fields should mirror the contents of the relevant admin
    # area model
    # TODO : remove the two fields in CountyBoundary, ConstituencyBoundary and
    # WardBoundary models, retain them in WorldBorder model.
    name = gis_models.CharField(max_length=100)
    code = gis_models.CharField(max_length=10, unique=True)

    # Making this field nullable is a temporary band-aid for a deficiency
    # in model_mommy ( a testing tool )
    # The impact of this is minimal; these models hold setup data that is
    # loaded and tested during each build
    mpoly = gis_models.MultiPolygonField(null=True, blank=True)

    @property
    def bound(self):
        return json.loads(self.mpoly.envelope.geojson) if self.mpoly else None

    @property
    def center(self):
        return json.loads(self.mpoly.centroid.geojson) if self.mpoly else None

    @property
    def surface_area(self):
        return self.mpoly.area if self.mpoly else 0

    @property
    def facility_count(self):
        return FacilityCoordinates.objects.filter(
            coordinates__contained=self.mpoly
        ).count() if self and self.mpoly else 0

    @property
    def density(self):
        """This is a synthetic value

        The units matter less than the relative density compared to other
        administrative units
        """
        return self.facility_count / (self.surface_area * 10000) \
            if self.surface_area else 0

    @property
    def facility_coordinates(self):
        from common.models.model_declarations import \
            _lookup_facility_coordinates
        return _lookup_facility_coordinates(self)

    @property
    def geometry(self):
        """Reduce the precision of the geometries sent in list views

        This produces a MASSIVE saving in rendering time
        """
        if not self.mpoly:
            return self.mpoly

        def _simplify(tolerance, geometry):
            if isinstance(geometry, MultiPolygon):
                polygon = None
                for child_polygon in geometry:
                    if polygon:
                        polygon.extend(child_polygon)
                    else:
                        polygon = child_polygon
            else:
                polygon = geometry

            return json.loads(
                polygon.simplify(tolerance=tolerance).geojson
            )

        geojson_dict = _simplify(
            tolerance=self.TOLERANCE, geometry=self.mpoly.cascaded_union
        )
        original_coordinates = geojson_dict['coordinates']
        assert original_coordinates
        new_coordinates = [
            [
                [
                    round(coordinate_pair[0], self.PRECISION),
                    round(coordinate_pair[1], self.PRECISION)
                ]
                for coordinate_pair in original_coordinates[0]
                if coordinate_pair and
                isinstance(coordinate_pair[0], float) and
                isinstance(coordinate_pair[1], float)
            ]
        ]
        geojson_dict['coordinates'] = new_coordinates
        return geojson_dict

    class Meta(GISAbstractBase.Meta):
        abstract = True


@reversion.register
@encoding.python_2_unicode_compatible
class WorldBorder(AdministrativeUnitBoundary):

    """World boundaries

    Source: http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip
    """
    longitude = gis_models.FloatField()
    latitude = gis_models.FloatField()

    @property
    def geometry(self):
        """The world border data is unreliable, hence this; works for Kenya"""
        return json.loads(
            CountyBoundary.objects.aggregate(
                Union('mpoly')
            )['mpoly__union'].geojson
        ) if self.mpoly else {}

    def __str__(self):
        return self.name


@reversion.register(follow=['area'])
@encoding.python_2_unicode_compatible
class CountyBoundary(AdministrativeUnitBoundary):
    area = gis_models.OneToOneField(County)

    @property
    def constituency_ids(self):
        return Constituency.objects.filter(
            county=self.area).values_list('id', flat=True)

    @property
    def constituency_boundary_ids(self):
        constituency_boundary_ids = ConstituencyBoundary.objects.filter(
            area__id__in=self.constituency_ids
        ).values_list('id', flat=True)
        return constituency_boundary_ids

    def __str__(self):
        return self.name

    class Meta(GISAbstractBase.Meta):
        verbose_name_plural = 'county boundaries'


@reversion.register(follow=['area'])
@encoding.python_2_unicode_compatible
class ConstituencyBoundary(AdministrativeUnitBoundary):
    area = gis_models.OneToOneField(Constituency)

    def __str__(self):
        return self.name

    @property
    def ward_ids(self):
        return Ward.objects.filter(
            constituency=self.area).values_list('id', flat=True)

    @property
    def ward_boundary_ids(self):
        ward_boundary_ids = WardBoundary.objects.filter(
            area__id__in=self.ward_ids
        ).values_list('id', flat=True)
        return ward_boundary_ids

    class Meta(GISAbstractBase.Meta):
        verbose_name_plural = 'constituency boundaries'


@reversion.register(follow=['area'])
@encoding.python_2_unicode_compatible
class WardBoundary(AdministrativeUnitBoundary):
    area = gis_models.OneToOneField(Ward)

    def __str__(self):
        return self.name

    class Meta(GISAbstractBase.Meta):
        verbose_name_plural = 'ward boundaries'


class DrilldownView(db_models.Model):
    id = db_models.UUIDField(primary_key=True)
    county = db_models.PositiveIntegerField()
    constituency = db_models.PositiveIntegerField()
    ward = db_models.PositiveIntegerField()
    name = db_models.CharField(max_length=255)
    lat = db_models.FloatField()
    lng = db_models.FloatField()

    class Meta(object):
        managed = False
        db_table = 'mfl_gis_drilldown'
