from rest_framework import serializers

from common.serializers import InchargeCountiesSerializer
from .models import MflUser


class UserSerializer(serializers.ModelSerializer):
    counties = InchargeCountiesSerializer(many=True, required=False)

    class Meta:
        model = MflUser
        exclude = ('password',)
