import reversion
import logging

from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError
from common.models import AbstractBase, County, Constituency, Ward
from facilities.models import Facility


LOGGER = logging.getLogger(__name__)


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
    objects = gis_models.GeoManager()
    everything = gis_models.GeoManager()

    class Meta(AbstractBase.Meta):
        abstract = True


@reversion.register
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

    def __unicode__(self):
        return self.name


@reversion.register
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

    def __unicode__(self):
        return self.name


@reversion.register
class FacilityCoordinates(GISAbstractBase):
    """
    Location derived by the use of GPS satellites and GPS device or receivers.

    It it three dimensional.
    The three-dimensional readings from a GPS device are latitude, longitude,
    and attitude. The date/time the reading is done is also important, as
    is the source and method of the reading.
    """
    facility = gis_models.OneToOneField(Facility)
    coordinates = gis_models.PointField()
    source = gis_models.ForeignKey(
        GeoCodeSource,
        help_text="where the geo code came from", on_delete=gis_models.PROTECT)
    method = gis_models.ForeignKey(
        GeoCodeMethod,
        help_text="Method used to obtain the geo codes. e.g"
        " taken with GPS device")
    collection_date = gis_models.DateTimeField()

    def validate_longitude_and_latitude_within_kenya(self):
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
                    '{} is not within the Kenyan boundaries that we have'
                    .format(self.coordinates)
                )
        except WorldBorder.DoesNotExist:
            raise ValidationError('Setup error: Kenyan boundaries not loaded')

    def validate_longitude_and_latitude_within_constituency(self):
        try:
            boundary = ConstituencyBoundary.objects.get(
                area=self.facility.ward.constituency)
            if not boundary.mpoly.contains(self.coordinates):
                raise ValidationError(
                    '{} not contained in boundary of {}'.format(
                        self.coordinates,
                        self.facility.ward.constituency
                    )
                )
        except ConstituencyBoundary.DoesNotExist:
            raise ValidationError(
                'No boundary for {}'.format(
                    self.facility.ward.constituency
                )
            )

    def validate_longitude_and_latitude_within_county(self):
        try:
            boundary = CountyBoundary.objects.get(
                area=self.facility.ward.constituency.county)
            if not boundary.mpoly.contains(self.coordinates):
                raise ValidationError(
                    '{} not contained in boundary of {}'.format(
                        self.coordinates,
                        self.facility.ward.constituency.county
                    )
                )
        except CountyBoundary.DoesNotExist:
            raise ValidationError(
                'No boundary for {}'.format(
                    self.facility.ward.constituency.county
                )
            )

    def validate_longitude_and_latitude_within_ward(self):
        try:
            boundary = WardBoundary.objects.get(area=self.facility.ward)
            if not boundary.mpoly.contains(self.coordinates):
                raise ValidationError(
                    '{} not contained in boundary of {}'.format(
                        self.coordinates, self.facility.ward
                    )
                )
        except WardBoundary.DoesNotExist:
            LOGGER.error(
                'Ward {} does not have boundary info'.format(
                    self.facility.ward)
            )

    def clean(self):
        self.validate_longitude_and_latitude_within_kenya()
        self.validate_longitude_and_latitude_within_county()
        self.validate_longitude_and_latitude_within_constituency()
        self.validate_longitude_and_latitude_within_ward()
        super(FacilityCoordinates, self).clean()

    def __unicode__(self):
        return self.facility.name

    class Meta(GISAbstractBase.Meta):
        verbose_name_plural = 'facility coordinates'
        verbose_name = 'facility coordinates'


class AdministrativeUnitBoundary(GISAbstractBase):
    """Base class for the models that implement administrative boundaries

    All common operations and fields are here.
    We retain the default SRID ( 4326 - WGS84 ).
    """
    name = gis_models.CharField(max_length=100)
    code = gis_models.CharField(max_length=10, unique=True)

    # Making this field nullable is a temporary band-aid for a deficiency
    # in model_mommy ( a testing tool )
    # The impact of this is minimal; these models hold setup data that is
    # loaded and tested during each build
    mpoly = gis_models.MultiPolygonField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta(GISAbstractBase.Meta):
        abstract = True


@reversion.register
class WorldBorder(AdministrativeUnitBoundary):
    """World boundaries

    Source: http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip
    """
    longitude = gis_models.FloatField()
    latitude = gis_models.FloatField()


@reversion.register
class CountyBoundary(AdministrativeUnitBoundary):
    area = gis_models.OneToOneField(County)

    class Meta(GISAbstractBase.Meta):
        verbose_name_plural = 'county boundaries'


@reversion.register
class ConstituencyBoundary(AdministrativeUnitBoundary):
    area = gis_models.OneToOneField(Constituency)

    class Meta(GISAbstractBase.Meta):
        verbose_name_plural = 'constituency boundaries'


@reversion.register
class WardBoundary(AdministrativeUnitBoundary):
    area = gis_models.OneToOneField(Ward)

    class Meta(GISAbstractBase.Meta):
        verbose_name_plural = 'ward boundaries'
