from django.contrib.auth import authenticate, login, logout

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login
)
from django.utils.http import is_safe_url
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.forms import AuthenticationForm

from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView, Response

from .models import MflUser
from .serializers import UserSerializer
from .filters import MFLUserFilter


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
    ordering_fields = ('first_name', 'last_name', 'email', 'username',)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MflUser.objects.all()
    serializer_class = UserSerializer


@sensitive_post_parameters()
@csrf_protect
@never_cache
def mfl_login(request):
    """
    A simplified rendition of the built in django.contrib.auth login view
    """
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)

        else:
            print 'Invalid auth form!'
            print form.errors
    else:
        form = AuthenticationForm(request)

    current_site = get_current_site(request)
    context = {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    return TemplateResponse(request, 'rest_framework/login.html', context)
