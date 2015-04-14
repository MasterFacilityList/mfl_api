from django.contrib.auth import authenticate, login, logout

from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView, Response

from common.models import UserCounties
from .models import MflUser
from .serializers import InchargeCountiesSerializer, UserSerializer
from .filters import MFLUserFilter, UserCountiesFilter


class APILogin(APIView):
    """Logs in a user request."""
    permission_classes = (permissions.AllowAny, )

    @staticmethod
    def post(request, *args, **kwargs):

        email = request.DATA['email']
        password = request.DATA['password']

        user = authenticate(email=email, password=password)
        if user:
            if not user.is_active:
                data = "The user is not active"
                return Response(data=data, status=401)
            login(request, user)
            data = UserSerializer(user).data
            return Response(data=data, status=200)
        else:
            return Response(
                "Invalid username/password Combination",
                status=401)


class APILogout(APIView):
    """Logs out a user."""
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)
        return Response(status=401, data='User logged out')


class UserList(generics.ListCreateAPIView):
    queryset = MflUser.objects.all()
    serializer_class = UserSerializer
    filter_class = MFLUserFilter
    ordering_fields = ('first_name', )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MflUser.objects.all()
    serializer_class = UserSerializer


class UserCountiesView(generics.ListCreateAPIView):
    queryset = UserCounties.objects.all()
    serializer_class = InchargeCountiesSerializer
    filter_class = UserCountiesFilter
    ordering_fields = ('user', )


class UserCountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserCounties.objects.all()
    serializer_class = InchargeCountiesSerializer
