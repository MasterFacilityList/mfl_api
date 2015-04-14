from rest_framework import serializers

from common.serializers import AbstractFieldsMixin

from common.models import UserCounties
from .models import MflUser


class InchargeCountiesSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserCounties


class UserSerializer(serializers.ModelSerializer):
    counties = InchargeCountiesSerializer(many=True, required=False)

    class Meta:
        model = MflUser
