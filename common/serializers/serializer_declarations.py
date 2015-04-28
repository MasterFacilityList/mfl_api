from rest_framework import serializers

from ..models import (
    Contact,
    PhysicalAddress,
    County,
    Ward,
    Constituency,
    ContactType,
    UserCounty,
    UserContact,
    Town
)
from .serializer_base import AbstractFieldsMixin


class UserContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = UserContact


class ContactTypeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = ContactType


class ContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Contact


class PhysicalAddressSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = PhysicalAddress


class CountySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = County


class TownSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Town


class WardSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    county = serializers.CharField(source='county', read_only=True)

    class Meta(object):
        model = Ward


class ConstituencySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Constituency


class InchargeCountiesSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = UserCounty
