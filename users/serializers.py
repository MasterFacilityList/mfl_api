from rest_framework import serializers

from common.serializers import InchargeCountiesSerializer
from .models import MflUser, MFLOAuthApplication


class UserSerializer(serializers.ModelSerializer):
    counties = InchargeCountiesSerializer(many=True, required=False)

    short_name = serializers.ReadOnlyField(source='get_short_name')
    full_name = serializers.ReadOnlyField(source='get_full_name')
    permissions = serializers.ReadOnlyField()

    class Meta(object):
        model = MflUser
        exclude = ('password',)


class MFLOAuthApplicationSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = MFLOAuthApplication
