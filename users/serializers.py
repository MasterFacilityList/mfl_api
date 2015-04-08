from rest_framework import serializers

from common.serializers import AbstractFieldsMixin

from .models import MflUser, UserInchargeCounties


class InchargeCountiesSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserInchargeCounties


class UserSerializer(serializers.ModelSerializer):
    counties = InchargeCountiesSerializer(many=True, required=False)

    class Meta:
        model = MflUser
