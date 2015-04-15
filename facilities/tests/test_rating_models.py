from django.test import TestCase
from django.core.exceptions import ValidationError

from model_mommy import mommy

from common.tests.test_models import BaseTestCase
from facilities.models import Facility, FacilityService

from ..models import(
    RatingScale, Rating, FacilityRatingScale, FacilityServiceRatingScale,
    UserFacilityRating, UserFacilityServiceRating)


class TestRatingScale(TestCase):
    def test_save(self):
        rating_scale = mommy.make(RatingScale)
        self.assertEquals(1, RatingScale.objects.count())

        # test unicode
        self.assertEquals(rating_scale.name, rating_scale.__unicode__())


class TestRating(TestCase):
    def test_save(self):
        rating = mommy.make(Rating)
        self.assertEquals(1, Rating.objects.count())

        # test unicode
        expected_unicode = "{}: {}". format(
            rating.scale.name, rating.rating_code)
        self.assertEquals(expected_unicode, rating.__unicode__())


class TestsFacilityRatingScale(BaseTestCase):
    def test_save(self):
        facility_rating_scale = mommy.make(FacilityRatingScale)
        self.assertEquals(1, FacilityRatingScale.objects.count())

        # test unicode
        expected_unicode = "{}: {}".format(
            facility_rating_scale.facility.name,
            facility_rating_scale.scale.name)
        self.assertEquals(
            expected_unicode,
            facility_rating_scale.__unicode__())

    def test_only_one_facility_rating_active(self):
        facility = mommy.make(Facility)
        rating_scale = mommy.make(RatingScale)
        mommy.make(
            FacilityRatingScale, facility=facility,
            scale=rating_scale, active=True)
        data = {
            "facility": facility,
            "scale": rating_scale
        }
        data = self.inject_audit_fields(data)
        with self.assertRaises(ValidationError):
            FacilityRatingScale.objects.create(**data)


class TestFacilityServiceRating(BaseTestCase):
    def test_save(self):
        facility_service_rating_scale = mommy.make(FacilityServiceRatingScale)
        self.assertEquals(1, FacilityServiceRatingScale.objects.count())

        # test unicode
        expected_unicode = "{}: {}: {}".format(
            facility_service_rating_scale.facility_service.facility.name,
            facility_service_rating_scale.facility_service.service.name,
            facility_service_rating_scale.scale.name)
        self.assertEquals(
            expected_unicode, facility_service_rating_scale.__unicode__())

    def test_only_one_active(self):
        facility_service = mommy.make(FacilityService)
        scale = mommy.make(RatingScale)

        mommy.make(
            FacilityServiceRatingScale, facility_service=facility_service,
            scale=scale)
        data = {
            "facility_service": facility_service,
            "scale": scale
        }
        data = self.inject_audit_fields(data)
        with self.assertRaises(ValidationError):
            FacilityServiceRatingScale.objects.create(**data)


class TestUserFacilityRating(BaseTestCase):
    def test_save(self):
        facility = mommy.make(Facility)
        scale = mommy.make(RatingScale)
        rating = mommy.make(Rating, scale=scale)
        mommy.make(FacilityRatingScale, scale=scale, facility=facility)
        user_rating = mommy.make(
            UserFacilityRating, facility=facility, rating=rating)
        self.assertEquals(1, UserFacilityRating.objects.count())

        # test unicode
        expected_unicode = "{}: {}: {}: {}".format(
            user_rating.user.email, user_rating.facility.name,
            user_rating.rating.scale.name,
            user_rating.rating.rating_code)
        self.assertEquals(expected_unicode, user_rating.__unicode__())

    def test_user_scale_matches_facility_scale(self):
        facility = mommy.make(Facility)
        scale = mommy.make(RatingScale)
        scale_2 = mommy.make(RatingScale)
        mommy.make(
            FacilityRatingScale, facility=facility, scale=scale)
        rating = mommy.make(Rating, scale=scale_2)

        data = {
            "rating": rating,
            "facility": facility,
            "user": self.user
        }
        data = self.inject_audit_fields(data)
        with self.assertRaises(ValidationError):
            UserFacilityRating.objects.create(**data)


class TestUserFacilityServiceRating(BaseTestCase):
    def test_save(self):
        facility_service = mommy.make(FacilityService)
        scale = mommy.make(RatingScale)
        rating = mommy.make(Rating, scale=scale)
        mommy.make(
            FacilityServiceRatingScale, scale=scale,
            facility_service=facility_service)
        user_facility_service_rating = mommy.make(
            UserFacilityServiceRating,
            facility_service=facility_service, rating=rating)
        self.assertEquals(1, UserFacilityServiceRating.objects.count())

        #  test unicode
        expected_unicode = "{}: {}: {}".format(
            user_facility_service_rating.user,
            user_facility_service_rating.facility_service,
            user_facility_service_rating.rating)
        self.assertEquals(
            expected_unicode, user_facility_service_rating.__unicode__())

    def test_user_scale_matches_facility_scale(self):
        scale = mommy.make(RatingScale)
        scale_2 = mommy.make(RatingScale)
        rating = mommy.make(Rating, scale=scale_2)
        facility_service = mommy.make(FacilityService)
        mommy.make(
            FacilityServiceRatingScale, facility_service=facility_service,
            scale=scale)

        data = {
            "user": self.user,
            "rating": rating,
            "facility_service": facility_service
        }
        data = self.inject_audit_fields(data)
        with self.assertRaises(ValidationError):
            UserFacilityServiceRating.objects.create(**data)
