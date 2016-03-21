from rest_framework import generics
from rest_framework.views import Response, status

from django.contrib.auth.models import Permission, Group
from django.shortcuts import get_object_or_404

from common.utilities import CustomRetrieveUpdateDestroyView
from common.models import(
    UserCounty, UserSubCounty, UserConstituency, UserContact)

from .models import MflUser, MFLOAuthApplication, CustomGroup, ProxyGroup

from .serializers import (
    MflUserSerializer,
    MFLOAuthApplicationSerializer,
    PermissionSerializer,
    GroupSerializer
)

from .filters import MFLUserFilter, PermissionFilter, GroupFilter


class PermissionsListView(generics.ListAPIView):
    """
    This is a read-only list view; intentionally.

    The system's role based access control is built on the foundations put in
    place in `django.contrib.auth` and `django.contrib.admin`. The official
    web front-ends rely on the "automatic" permissions.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_class = PermissionFilter
    ordering_fields = ('name', )


class GroupListView(generics.ListCreateAPIView):
    queryset = ProxyGroup.objects.all()
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    ordering_fields = ('name', )

    def get_queryset(self, *args, **kwargs):
        user = self.request.user

        if user.county:
            group_ids = [
                grp.id for grp in ProxyGroup.objects.all()
                if not grp.is_national or grp.is_county_level
            ]
            return ProxyGroup.objects.filter(id__in=group_ids)
        elif user.sub_county or user.constituency:
            group_ids = [
                grp.id for grp in ProxyGroup.objects.all()
                if grp.is_sub_county_level
            ]
            return ProxyGroup.objects.filter(id__in=group_ids)
        else:
            return ProxyGroup.objects.all()


class GroupDetailView(CustomRetrieveUpdateDestroyView):
    queryset = ProxyGroup.objects.all()
    serializer_class = GroupSerializer

    def delete(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        group = Group.objects.get(id=pk)

        try:
            CustomGroup.objects.get(group=group).delete()
        except CustomGroup.DoesNotExist:
            pass
        users = MflUser.objects.all()
        for user in users:
            user.groups.remove(group)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListCreateAPIView):
    queryset = MflUser.objects.all()
    serializer_class = MflUserSerializer
    filter_class = MFLUserFilter
    ordering_fields = (
        'first_name', 'email', 'is_active',
        'last_login', 'employee_number'
    )

    def get_queryset(self, *args, **kwargs):
        from common.models import UserCounty, UserConstituency
        user = self.request.user
        custom_queryset = kwargs.pop('custom_queryset', None)
        if hasattr(custom_queryset, 'count'):
            self.queryset = custom_queryset
        if user.county and not user.is_national:
            county_users = [
                const_user.user.id for const_user in
                UserCounty.objects.filter(
                    county=user.county).distinct()
            ]
            sub_county_users = [
                const_user.user.id for const_user in
                UserConstituency.objects.filter(
                    constituency__county=user.county).distinct()
            ]
            area_users = county_users + sub_county_users
            return self.queryset.filter(
                id__in=area_users).exclude(id=self.request.user.id)
        elif user.is_national and not user.is_superuser:
            return MflUser.objects.all()

        elif user.constituency or user.sub_county:
            all_users = MflUser.objects.all()
            users_to_see = []
            sub_county_level_groups = [
                c_group.group for c_group in
                CustomGroup.objects.filter(sub_county_level=True)]
            for user in all_users:
                users_to_see.append(user.id) if set(
                    user.groups.all()).issubset(
                    sub_county_level_groups) else None

                users_to_see.append(user.id) if not user.groups.all() else None

            return self.queryset.filter(
                id__in=users_to_see, created_by_id=self.request.user.id
            ).exclude(id=self.request.user.id)
        elif user.is_superuser:
            return self.queryset.all().exclude(id=self.request.user.id)

        else:
            # The user is not allowed to see the users
            return MflUser.objects.none()

    def filter_queryset(self, queryset):
        """
        Overridden in order to constrain search results to what a user should
        see.
        """
        queryset = super(UserList, self).filter_queryset(queryset)
        return self.get_queryset(custom_queryset=queryset)


class UserDetailView(CustomRetrieveUpdateDestroyView):
    queryset = MflUser.objects.all()
    serializer_class = MflUserSerializer

    def delete(self, request, pk, format=None):
        user = get_object_or_404(MflUser, id=pk)
        user_contacts = UserContact.objects.filter(user=user)
        [uc.contact.delete() for uc in user_contacts]
        user_contacts.delete()
        UserCounty.objects.filter(user=user).delete()
        UserConstituency.objects.filter(user=user).delete()
        UserSubCounty.objects.filter(user=user).delete()
        user.deleted = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MFLOauthApplicationListView(generics.ListCreateAPIView):
    """
    List and register new OAuth2 applications

    This is a controlled access API. It is limited to admin users
    ( users with `is_admin` set to `True` ).

    Also - if you are using OAuth tokens, **the API server MUST be accessed
    over HTTPS**.

    # Registering a new OAuth2 application
    You can learn all that you need to know about oauth2 by reading
    https://tools.ietf.org/html/rfc6749 .

    If you are in too much of a hurry to read all that, here is what you
    should do:

    * obtain the user ID of the user that you'd like to get an access
    token for from [the users API](/api/users/). This naturally means
    that the user should already exist, and have the necessary privileges.
    Set the `user` to the primary key of the user you'd like to create.
    * set the `authorization_grant_type` to `password` ( which
    is referred to in OAuth2 docs as `Resource owner password-based` )
    * set the `client_type` to `confidential`

    It is a good idea to supply a `name` also. The following example
    represents the a minimal `POST` that establishes an application:

        {
            "client_type": "confidential",
            "authorization_grant_type": "password",
            "name": "Demo / Docs Application",
            "user": 3
        }

    A successful `POST` will get back a `HTTP 201 CREATED` response, and
    a representation of the new application. This example request got back
    this representation:

        {
            "id": 1,
            "client_id": "<redacted>",
            "redirect_uris": "",
            "client_type": "confidential",
            "authorization_grant_type": "password",
            "client_secret": "<redacted>",
            "name": "Demo / Docs Application",
            "skip_authorization": false,
            "user": 3
        }

    The `client_id` and `client_secret` fields were automatically assigned.
    The `skip_authorization` and `redirect_urls` fields have default values.

    A single user can be associated with multiple applications.

    # Authenticating using OAuth2 tokens
    Authentication is a two step process:

    ## Step 1: obtain an access token
    In order to obtain an access token, `POST` the user's credentials to
    [/o/token/](/o/token/).

    For example:

        curl -X POST -d "grant_type=password&username=serikalikuu@mfltest.slade360.co.ke&password=serikalikuu" http://sfzgvKKVpLxyHn3EbZrepehJnLn1r0OOFnuqBNy7:7SMXKum5CJVWABxIitwszES3Kls5RTBzYzJDI5jdvgPcw0vSjP5pnlYHfANSkPyn8pzSfyi5ETesPGXbbiKih0D3YRjE49IlsMShJy0p6pxLOLp72UKsNKxnj08H0fXP@localhost:8000/o/token/

    Which breaks down as:

        curl -X POST -d grant_type=<grant_type>&username=<email>&password=<password>" http://<client_id>:<client_secret>@<host>:<por>/o/token/

    ## Step 2: use the access token
    The reply from the server will be a `JSON` payload that has the issued
    access token, the refresh token, the access token type, expiry and scope.

    For example:

        {
            "access_token": "fKDvh2fFLR1iFPuB26RUEalbjYO4rx",
            "token_type": "Bearer",
            "expires_in": 36000,
            "refresh_token": "jLwpCh3WbOXBeb01XMeZR5AQYedkj1",
            "scope": "read write"
        }

    Pick the `access_token` and send it in an `Authorization: Bearer` header
    e.g

        curl -H "Authorization: Bearer ziBLqoXwVEA8lW9yEmE260AZ4lCJHq" http://localhost:8000/api/common/counties/

    For more detail on OAuth2 e.g the role of the refresh tokens, kindly
    consult the RFC.
    """  # NOQA
    queryset = MFLOAuthApplication.objects.all()
    serializer_class = MFLOAuthApplicationSerializer
    ordering_fields = (
        'user', 'client_type', 'authorization_grant_type', 'name')


class MFLOauthApplicationDetailView(CustomRetrieveUpdateDestroyView):
    """View, update and retire specific OAuth2 application authorizations"""
    queryset = MFLOAuthApplication.objects.all()
    serializer_class = MFLOAuthApplicationSerializer
