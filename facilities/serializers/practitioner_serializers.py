from rest_framework import serializers
from common.serializers import AbstractFieldsMixin

from ..models import (
    PracticeType,
    Speciality,
    Qualification,
    Practitioner,
    PractitionerQualification,
    PractitionerContact,
    PractitionerFacility
)


class PracticeTypeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = PracticeType


class SpecialitySerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Speciality


class QualificationSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Qualification


class PractitionerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Practitioner


class PractitionerQualificationSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = PractitionerQualification


class PractitionerContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = PractitionerContact


class PractitionerFacilitySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = PractitionerFacility
