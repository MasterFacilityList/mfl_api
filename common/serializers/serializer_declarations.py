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
    class Meta:
        model = UserContact


class ContactTypeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = ContactType


class ContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Contact


class PhysicalAddressSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = PhysicalAddress


class CountySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = County


class TownSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Town


class WardSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Ward


class ConstituencySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Constituency


class InchargeCountiesSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserCounty
