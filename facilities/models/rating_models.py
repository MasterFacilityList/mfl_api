from django.db import models

from common.models import AbstractBase

from facilities.models import Facility, FacilityService
from users.models import MflUser


class RatingScale(AbstractBase):
    """
    Holds the different types of rating of an entity.

    Some organisations use the likert scale, others use the interval
    scale and yet others use the ration scale.
    """

    name = models.CharField(
        max_length=100, unique=True,
        help_text='The name of the rating scale e.g likert RatingScale')
    description = models.TextField(
        help_text='A summary of the type of rating scale. E.g What it is. ')

    def __unicode__(self):
        return self.name


class Rating(AbstractBase):
    """
    The different levels of a scale.

    The format of a typical five-level Likert item, for example, could be:

        1. Strongly disagree
        2. Disagree
        3. Neither agree nor disagree
        4. Agree
        5. Strongly agree
    """

    scale = models.ForeignKey(RatingScale, on_delete=models.PROTECT)
    rating_code = models.CharField(
        max_length=30,
        help_text='A code representing  a rate e.g 1, Likely etc')
    description = models.TextField(
        null=True, blank=True,
        help_text='An explanation of how the rating code is used')

    def __unicode__(self):
        return self.scale.name + ": " + self.rating_code

    class Meta:
        unique_together = ('scale', 'rating_code', )


class FacilityRatingScale(AbstractBase):
    """
    The rating scale that a facility uses.
    """

    facility = models.ForeignKey(
        Facility, on_delete=models.PROTECT,
        related_name='facility_rating_scales')
    scale = models.ForeignKey(
        RatingScale, on_delete=models.PROTECT,
        related_name='facilities_using_scale')

    def __unicode__(self):
        return self.facility.name + ": " + self.scale.name

    # TODO Fix this code scar before the metadata ticket is closed
    # def validate_only_one_active(self):
    #     facility_scales_no = self.__class__.objects.filter(
    #         facility=self.facility, scale=self.scale, active=True).count()
    #     if facility_scales_no > 0:
    #         raise ValidationError(
    #             "Only one type scale can be active for a facility at a time")

    # def clean(self, *args, **kwargs):
    #     self.validate_only_one_active()
    #     super(FacilityRatingScale, self).clean(*args, **kwargs)

    class Meta:
        unique_together = ('facility', 'scale', )


class FacilityServiceRatingScale(AbstractBase):
    """
    The scale that a facility service uses.
    """

    facility_service = models.ForeignKey(
        FacilityService, on_delete=models.PROTECT,
        related_name='facility_service_scale')
    scale = models.ForeignKey(
        RatingScale, on_delete=models.PROTECT,
        related_name='facility_service_using_scale')

    def __unicode__(self):
        unicode_string = "{}: {}: {}".format(
            self.facility_service.facility.name,
            self.facility_service.service.name,
            self.scale.name)
        return unicode_string

    # TODO Fix this code scar before the metadata ticket is closed
    # def validate_only_one_active(self):
    #     facility_service_scales_no = self.__class__.objects.filter(
    #         facility_service=self.facility_service,
    #         scale=self.scale, active=True).count()
    #     if facility_service_scales_no > 0:
    #         raise ValidationError(
    #             "Only one type of scale can be active for a facility service")  # NOQA

    # def clean(self, *args, **kwargs):
    #     self.validate_only_one_active()
    #     super(FacilityServiceRatingScale, self).clean(*args, **kwargs)

    class Meta:
        unique_together = ('facility_service', 'scale', )


class RatingAbstractBase(AbstractBase):
    """
    Holds the common fields for rating of an entity.
    """

    rating = models.ForeignKey(Rating, on_delete=models.PROTECT)
    comment = models.TextField(
        null=True, blank=True,
        help_text='Reason for picking that rate.')

    class Meta:
        abstract = True


class UserFacilityRating(RatingAbstractBase):
    """
    User rating of a facility.
    """
    user = models.ForeignKey(
        MflUser, on_delete=models.PROTECT, related_name='user_facility_rating')
    facility = models.ForeignKey(
        Facility, on_delete=models.PROTECT, related_name='facility_rating')

    # TODO Fix this code scar before the metadata ticket is closed
    # def validate_user_rating_scale_matches_facility_scale(self):
    #     """
    #     Ensure the scale used by user is that used by the facility.
    #     """
    #     try:
    #         FacilityRatingScale.objects.get(
    #             facility=self.facility, scale=self.rating.scale, active=True)
    #     except FacilityRatingScale.DoesNotExist:
    #         raise ValidationError(
    #             "The rating scale used is not allowed for the facility.")

    def __unicode__(self):
        unicode_string = "{}: {}: {}".format(
            self.user.email, self.facility.name, self.rating)
        return unicode_string

    # TODO Fix this code scar before the metadata ticket is closed
    # def clean(self, *args, **kwargs):
    #     self.validate_user_rating_scale_matches_facility_scale()
    #     super(UserFacilityRating, self).clean(*args, **kwargs)

    class Meta:
        unique_together = ('facility', 'user', )


class UserFacilityServiceRating(RatingAbstractBase):
    """
    User rating of a facility service.
    """
    user = models.ForeignKey(
        MflUser, on_delete=models.PROTECT, related_name='user_service_rating')
    facility_service = models.ForeignKey(
        FacilityService, on_delete=models.PROTECT)

    def __unicode__(self):
        unicode_string = "{}: {}: {}".format(
            self.user, self.facility_service, self.rating)
        return unicode_string

    # TODO Fix this code scar before the metadata ticket is closed
    # def validate_user_rating_scale_matches_service_scale(self):
    #     """
    #     Ensure the scale used by the user is that used by the facility.
    #     """

    #     try:
    #         FacilityServiceRatingScale.objects.get(
    #             facility_service=self.facility_service,
    #             scale=self.rating.scale, active=True)
    #     except FacilityServiceRatingScale.DoesNotExist:
    #         raise ValidationError(
    #             "The rating scale used is not allowed for the facility service"  # NOQA
    #         )

    # def clean(self, *args, **kwargs):
    #     self.validate_user_rating_scale_matches_service_scale()
    #     super(UserFacilityServiceRating, self).clean(*args, **kwargs)

    class Meta:
        unique_together = ('facility_service', 'user', )
