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
    class Meta:
        model = PracticeType


class SpecialitySerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Speciality


class QualificationSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Qualification


class PractitionerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Practitioner


class PractitionerQualificationSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = PractitionerQualification


class PractitionerContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = PractitionerContact


class PractitionerFacilitySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = PractitionerFacility
