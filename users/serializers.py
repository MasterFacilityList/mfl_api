from rest_framework import serializers

from common.serializers import AbstractFieldsMixin
from roles.serializers import UserRolesSerializer

from .models import MflUser, UserInchargeCounties


class InchargeCountiesSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserInchargeCounties


class UserSerializer(serializers.ModelSerializer):
    counties = InchargeCountiesSerializer(many=True, required=False)
    user_roles = UserRolesSerializer(many=True, required=False)

    class Meta:
        model = MflUser
