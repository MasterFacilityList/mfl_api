from rest_framework import generics
from django.contrib.auth.models import Group, Permission
from .models import MflUser, MFLOAuthApplication
from .serializers import (
    UserSerializer,
    MFLOAuthApplicationSerializer,
    PermissionSerializer,
    GroupSerializer
)
from .filters import MFLUserFilter


class PermissionsListView(generics.ListAPIView):
    """
    This is a read-only list view; intentionally.

    The system's role based access control is built on the foundations put in
    place in `django.contrib.auth` and `django.contrib.admin`. The official
    web front-ends rely on the "automatic" permissions.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class GroupListView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserList(generics.ListCreateAPIView):
    queryset = MflUser.objects.all()
    serializer_class = UserSerializer
    filter_class = MFLUserFilter
    ordering_fields = ('first_name', 'last_name', 'email', 'username',)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MflUser.objects.all()
    serializer_class = UserSerializer


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


class MFLOauthApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MFLOAuthApplication.objects.all()
    serializer_class = MFLOAuthApplicationSerializer

# TODO Add and document APIs for role setup
# Read only API for permissions
# Read-write API for groups
# Document adding permissions to users
# Document adding groups to users / creating users
# TODO Implement and document custom permission for accessing GIS
# TODO Document is_national and county linkage
# TODO Create in demo data default roles for each county and national
# TODO Define general public role ( read only, no GIS )
# TODO Define public role with GIS access ( read only perms, has GIS )
# TODO Map current facilities to GIS and make report of unmapped ones
# TODO Add notes on the need to run over HTTPS ( compulsory ) and OAuth
# TODO Document API login vis session; email vs username
# TODO Document API login via OAuth2
# TODO Document API logout
# TODO Document password reset
# TODO Document password reset confirmation
# TODO Document password change
# TODO Document GET of user details ( if it overlaps with ours, remove one )
# TODO Document updating user details vis PUT and PATCH
# TODO Document user registration
# TODO Document retrieval of user permisions and how to use them
# TODO Document email verification in registration
# TODO Document future possibility of social media auth
# TODO Document national vs county stuff
# TODO Document GIS ( map plotting APIs ); enhance if needed
# TODO Borrow @ngash's introductory API docs
# TODO Write out an overview of the goals and architecture of MFL v2
# TODO Write out a section of the docs that talks about how to use
# e.g what client, what browser extension ( httpie, curl )
# TODO Add Swagger compatible docstrings to every view
# ( first line summary, detailed description, params from filters
# including base filter )
# TODO Fix sandbox is_logged_in check
