Authentication and Authorization
==================================

`Authentication`_ is the process of associating an API request with a specific
user, while `authorization`_ determines if the user has permission to perform
the requested operation.

.. _`Authentication`: http://www.django-rest-framework.org/api-guide/authentication/
.. _`authorization`: http://www.django-rest-framework.org/api-guide/permissions/

Authentication
-----------------
The MFL API server supports both session ( cookie based ) and OAuth 2 ( token based ) authentication. For both approaches, the production API server **must be run over HTTPS**.

Session Authentication
~~~~~~~~~~~~~~~~~~~~~~~~
Logging in
+++++++++++++
``POST`` the credentials to ``/api/rest-auth/login/``. The payload should be
similar to the example below:

.. code-block:: javascript

    {
        "username": "hakunaruhusa@mfltest.slade360.co.ke",
        "password": "hakunaruhusa"
    }

A successful login will have a ``HTTP 200 OK`` response. The response payload
will have a single ``key`` parameter: a Django Rest Framework `TokenAuthentication`_ key. For example:

.. code-block:: javascript

    {
        "key": "f9a978cd00e9dc0ebfe97d633d98bde4b35f9279"
    }

.. _`TokenAuthentication`: http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication

.. note::

    Please note that the ``username`` is actually an email address.

.. note::

    We discourage the use of token authentication. Kindly see the section on
    OAuth2 below.

Logging out
++++++++++++++
Send an empty ( no payload ) ``POST`` to ``/api/rest-auth/logout/``.

A successful logout will get back a ``HTTP 200 OK`` response, and a success
message similar to the one below:

.. code-block:: javascript

    {
        "success": "Successfully logged out."
    }

.. note:

    Logging out via this method will also delete the token that was assigned
    at login.

Getting user details after login
+++++++++++++++++++++++++++++++++++++
After a user is logged in, a typical client ( such as a web application ) will
need to get additional information about the user. This additional information
includes permissions.

If the user is logged in, a ``GET`` to ``/api/rest-auth/user/`` will get back
a ``HTTP 200 OK`` response and a user details payload similar to this example:

.. code-block:: javascript

    {
        "id": 3,
        "short_name": "Serikali",
        "full_name": "Serikali Kuu ",
        "all_permissions": [
            "common.add_town",
            "oauth2_provider.change_accesstoken",
            "mfl_gis.delete_wardboundary",
            "auth.add_permission",
            "chul.change_approvalstatus",
            "facilities.delete_facilitytype",
            // a long list of permissions; truncated for brevity
        ],
        "user_permissions": [],
        "groups": [],
        "last_login": "2015-05-04T16:33:36.085065Z",
        "is_superuser": true,
        "email": "serikalikuu@mfltest.slade360.co.ke",
        "first_name": "Serikali",
        "last_name": "Kuu",
        "other_names": "",
        "username": "serikalikuu",
        "is_staff": true,
        "is_active": true,
        "date_joined": "2015-05-03T02:39:03.440962Z",
        "is_national": true
    }

If the user is not logged in, the return message will be a
``HTTP 403 FORBIDDEN`` with the following message:

.. code-block:: javascript

    {
        "detail": "Authentication credentials were not provided."
    }

OAuth2 Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~
You can learn all that you need to know about OAuth2 by reading `rfc6749`_.

.. _`rfc6749`: https://tools.ietf.org/html/rfc6749

A simple OAuth2 workflow
+++++++++++++++++++++++++++++
If you are in too much of a hurry to read all that, here is what you
should do:

Registering a new "application"
***********************************
You should know the user ID of the user that you'd like to register an
application for. You can obtain that ID from the user details API described
above or from ``/api/users/``.

You need to know the ``authorization_grant_type`` that you'd like for the new
application. For the example below, we will use ``password``. If you do not
know what to choose, read `rfc6749`_ .

The next decision is the choice of ``client_type``. For the example below,
we will use ``confidential``. As always - consult `rfc6749`_ for more context.

``POST`` to ``/api/users/applications/`` a payload similar to this example:

.. code-block:: javascript

    {
        "client_type": "confidential",
        "authorization_grant_type": "password",
        "name": "Demo / Docs Application",
        "user": 3
    }

A successful ``POST`` will get back a ``HTTP 201 CREATED`` response, and
a representation of the new application. This example request got back
this representation:

.. code-block:: javascript

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

.. note::
    * The `client_id` and `client_secret` fields were automatically assigned.
    * The `skip_authorization` and `redirect_urls` fields have default values.
    * A single user can be associated with multiple applications.

Authenticating using OAuth2 tokens
*************************************
First,  obtain an access token by ``POST``ing the user's credentials to
``/o/token/``. For example:

.. code-block:: text

    curl -X POST -d "grant_type=password&username=serikalikuu@mfltest.slade360.co.ke&password=serikalikuu" http://sfzgvKKVpLxyHn3EbZrepehJnLn1r0OOFnuqBNy7:7SMXKum5CJVWABxIitwszES3Kls5RTBzYzJDI5jdvgPcw0vSjP5pnlYHfANSkPyn8pzSfyi5ETesPGXbbiKih0D3YRjE49IlsMShJy0p6pxLOLp72UKsNKxnj08H0fXP@localhost:8000/o/token/

Which breaks down as:

.. code-block:: text

    curl -X POST -d grant_type=<grant_type>&username=<email>&password=<password>" http://<client_id>:<client_secret>@<host>:<por>/o/token/

If you authenticate successfully, the reply from the server will be a `JSON`
payload that has the issued access token, the refresh token, the access token
type, expiry and scope. For example:

.. code-block:: javascript

    {
        "access_token": "fKDvh2fFLR1iFPuB26RUEalbjYO4rx",
        "token_type": "Bearer",
        "expires_in": 36000,
        "refresh_token": "jLwpCh3WbOXBeb01XMeZR5AQYedkj1",
        "scope": "read write"
    }

Pick the ``access_token`` and send it in an ``Authorization: Bearer`` header
e.g

.. code-block:: text

    curl -H "Authorization: Bearer ziBLqoXwVEA8lW9yEmE260AZ4lCJHq" http://localhost:8000/api/common/counties/

Authorization
----------------
This server's `Role Based Access Control`_ setup is based on the
`Django framework permissions and authorization`_ system.

.. _`Role Based Access Control`: http://en.wikipedia.org/wiki/Role-based_access_control
.. _`Django framework permissions and authorization`: https://docs.djangoproject.com/en/1.8/topics/auth/default/#topic-authorization

Understanding the role based access control setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The user details API endpoint ( explained above ) returns the logged in user's
permissions.

A user's permissions come from three "sources":

    * the permissions assigned to the group ( role ) that the user belongs to
    * the permissions assigned directly to the user
    * the ``is_superuser`` boolean flag; a user who is a "superuser" automatically gets all permissions

The MFL API server has an additional "layer" of authorization: whether a user
is a "national user" or a "county user". In certain list endpoints ( chiefly
those that deal directly with facilities ), a "county" user will have their
results limited to facilities that are located in their county.

TBD - setting up a link between a user and a county
TBD - getting and interpreting user permissions
TBD - overview, how roles and permissions work
TBD - note about there being no true unauthenticated access
TBD - notes about facility approvers and data entry people
TBD - the regulators systems are just one more set of API clients

RBAC setup
--------------
Permissions
~~~~~~~~~~~~~
TBD - document custom permissions, if any, plus read only API

Groups
~~~~~~~~
TBD - document role setup ( read, write )
TBD - comment about default roles

User registration
-------------------
TBD - user creation / registration
TBD - email verification
TBD - assigning permissions to users via groups
TBD - assigning permisssions to users directly
TBD - altering permissions via altering groups
TBD - altering permissions assigned directly
TBD - retiring a user
TBD - moving a user between counties
TBD - password reset
TBD - password reset confirmation
TBD - password change
TBD - comment about future possibilities of social media auth
TBD - updating user details

.. toctree::
    :maxdepth: 3
