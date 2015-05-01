from rest_framework import serializers

from common.serializers import InchargeCountiesSerializer
from .models import MflUser, MFLOAuthApplication


class UserSerializer(serializers.ModelSerializer):
    counties = InchargeCountiesSerializer(many=True, required=False)

    class Meta(object):
        model = MflUser
        exclude = ('password',)


class MFLOAuthApplicationSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = MFLOAuthApplication
