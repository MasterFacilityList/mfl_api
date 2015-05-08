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
        "is_national": true,
        "requires_password_change": false
    }

If the user is not logged in, the return message will be a
``HTTP 403 FORBIDDEN`` with the following message:

.. code-block:: javascript

    {
        "detail": "Authentication credentials were not provided."
    }

.. note::

    If a user needs to change their password e.g because it was created by an
    admin and must be changed on first login, the ``requires_password_change``
    boolean property will be set to ``true``.

    **Every well behaved web client should observe this property** and
    implement the appropriate "roadblock".

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

.. note::

    This API server does not support "true" unauthenticated read-only access
    For the public site, OAuth2 credentials ( that correspond to a role with
    limited access ) will be used.

.. note::

    From the point of view of the MFL API, regulator systems are just one more
    set of API clients.

Users and counties
~~~~~~~~~~~~~~~~~~~~~
In 2010, Kenya got a new constitution. One of the major changes was the
establishment of a devolved system of government.

The second generation MFL API ( this server ) is designed for the era of
devolution. In this system, facility record management should occur at the
county level.

The separation of privileges between data entry staff ( "makers" ) and those
responsible for approval ( "checkers" ) can be modelled easily using the
role based access control setup described above.

The only additional need is the need to link county level users to counties,
and use that information to limit their access. This has been achieved by
adding an ``is_national`` boolean flag to the custom user model and adding a
resource that links users to counties. The example user resource below
represents a non-national ( county ) user ( note the ``is_national`` field ):

.. code-block:: javascript

    {
        "id": 4,
        "short_name": "Serikali",
        "full_name": "Serikali Ndogo ",
        "all_permissions": [
            "common.add_town",
            // many more permissions
        ],
        "user_permissions": [],
        "groups": [],
        "last_login": null,
        "is_superuser": true,
        "email": "serikalindogo@mfltest.slade360.co.ke",
        "first_name": "Serikali",
        "last_name": "Ndogo",
        "other_names": "",
        "username": "serikalindogo",
        "is_staff": true,
        "is_active": true,
        "date_joined": "2015-05-03T02:39:03.443301Z",
        "is_national": false
    }

In order to link a user to a county, you need to have two pieces of
information:

    * the user's ``id``
    * the county's ``id`` - easily obtained from ``/api/common/counties/``

With these two pieces of information in place, ``POST`` to ``/api/common/user_counties/`` a payload similar to this example:

.. code-block:: javascript

    {
        "user": 4,
        "county": "d5f54838-8743-4774-a866-75d7744a9814"
    }

A successful operation will get back a ``HTTP 201 CREATED`` response and
a representation of the newly created resource. For example:

.. code-block:: javascript

    {
        "id": "073d8bfa-2a86-4f9a-9cbe-0b8ac6780c3a",
        "created": "2015-05-04T17:44:56.441006Z",
        "updated": "2015-05-04T17:44:56.441027Z",
        "deleted": false,
        "active": true,
        "created_by": 3,
        "updated_by": 3,
        "user": 4,
        "county": "d5f54838-8743-4774-a866-75d7744a9814"
    }

The filtering of results by county is transparent ( the API client does not
need to do anything ).

.. note::

    A user can only have one active link to a county at any particular time.
    Any attempt to link a user to more than one county at a time will get a
    validation error.

    If you'd like to change the county that a user is linked to, you will need
    to first inactivate the existing record ( ``PATCH`` it and set ``active``
    to ``false`` ).

    In order to determine the role that a user is currently linked to, issue a
    ``GET`` similar to ``/api/common/user_counties/?user=4&active=true``. In
    this example, ``4`` is the user's ``id``.

Setting up users, permissions and groups
-------------------------------------------
Permissions
~~~~~~~~~~~~~

API clients should treat permissions as "fixed" builtins. The server does not
implement any endpoint that can be used to add, edit or remove a permission.

The available permissions can be listed by issuing a ``GET`` to
``/api/users/permissions/``. The results will look like this:

.. code-block:: javascript

    {
        "count": 216,
        "next": "http://localhost:8000/api/users/permissions/?page=2",
        "previous": null,
        "results": [
            {
                "id": 61,
                "name": "Can add email address",
                "codename": "add_emailaddress",
                "content_type": 21
            },
            {
                "id": 62,
                "name": "Can change email address",
                "codename": "change_emailaddress",
                "content_type": 21
            },
            {
                "id": 63,
                "name": "Can delete email address",
                "codename": "delete_emailaddress",
                "content_type": 21
            },
            // truncated for brevity
        ]
    }

.. note::

    The `content_type` keys in the example above originate from
    `Django's contenttypes framework`_. For an API consumer, they are an
    implementation detail / curiosity; API clients will nto need to know more
    about them.

.. _`Django's contenttypes framework`: https://docs.djangoproject.com/en/1.8/ref/contrib/contenttypes/

Groups
~~~~~~~~
The API server provides APIs that can be used to create roles, alter existing
roles and retire roles.

Existing roles ( groups ) can be listed by issuing a ``GET`` to
``/api/users/groups/``.

Creating a new role
+++++++++++++++++++++++
``POST`` to ``/api/users/groups/`` a payload that similar to the one below:

.. code-block:: javascript

    {
        "name": "Documentation Example Group",
        "permissions": [
            {
                "id": 61,
                "name": "Can add email address",
                "codename": "add_emailaddress"
            },
            {
                "id": 62,
                "name": "Can change email address",
                "codename": "change_emailaddress"
            }
        ]
    }

A successful operation will get back a ``HTTP 201 CREATED`` status.

.. note::

    You must supply both a ``name`` and ``permissions``.

Updating an existing role
++++++++++++++++++++++++++++

``PUT`` or ``PATCH`` to a group **detail URL** e.g ``/api/users/groups/1/``.

For example, to take away from the example role the "Can change email address"
permission, the following ``PATCH`` request should be sent:

.. code-block:: javascript

    {
        "permissions": [
            {
                "id": 61,
                "name": "Can add email address",
                "codename": "add_emailaddress"
            }
        ]
    }

A similar approach will be followed to add permissions.

A successful operation will get back a ``HTTP 200 OK`` status.

.. note::

    **Permissions will always be overwritten** when you perform an update.

User management
-------------------
User registration ( sign up )
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``POST`` to ``/api/rest-auth/registration/`` a payload similar to this example:

.. code-block:: javascript

    {
        "username": "likeforreal",
        "email": "likeforreal@yodawg.dawg",
        "password1": "most_secure_password_in_the_world_like_for_real",
        "password2": "most_secure_password_in_the_world_like_for_real"
    }

A successful operation will get back a ``HTTP 201 CREATED`` response and
a representation of the new user. For example:

.. code-block:: text

    HTTP 201 CREATED
    Content-Type: application/json
    Vary: Accept
    Allow: POST, OPTIONS, HEAD

    {
        "id": 9,
        "short_name": "",
        "full_name": "  ",
        "all_permissions": [],
        "user_permissions": [],
        "groups": [],
        "last_login": "2015-05-05T09:12:01.888514Z",
        "is_superuser": false,
        "email": "likeforreal1@yodawg.dawg",
        "first_name": "",
        "last_name": "",
        "other_names": "",
        "username": "likeforreal1",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2015-05-05T09:12:01.790167Z",
        "is_national": false
    }

.. note::

    This API server does not implement email address confirmation.
    A future release might implement that.

.. note::

    The registration operation described above suffices, for public users.

The manner in which users should be linked to counties has already been
discussed in the Authorization section.

Linking users to groups
~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to assign a user to a group, you will need to know the group
ID ( which you can obtain from ```/api/groups/``.

``PATCH`` an already existing user with a payload similar to this example:

.. code-block:: javascript

    {
        "groups": [
            {"id": 1, "name": "Documentation Example Group"}
        ]
    }

In order to remove them from their assigned roles, ``PATCH`` with an empty
``groups`` list.

.. note::

    This server does not support the direct assignment of permissions to users.
    That is deliberate.

Updating user details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Every writable attribute of a user record can be ``PATCH``ed. For example,
to inactivate or retire a user, ``PATCH`` the user's ( detail ) record and set
``is_active`` to ``false``.

For example: if the detail record for the user we registered above
( ``likeforreal`` ) is to be found at ``/api/users/9/``, the user can be
inactivated by ``PATCH``ing ``/api/users/9/`` with:

.. code-block:: javascript

    {
        "active": false
    }

.. note::

    The same general approach can be used for any other flag e.g
    ``is_superuser``.

Password changes
~~~~~~~~~~~~~~~~~~~
The password of the **logged in user** can be changed by ``POST``ing to
``/api/rest-auth/password/change/`` a payload similar to this example:

.. code-block:: javascript

    {
        "old_password": "oldanddonewith",
        "new_password1": "newhotness",
        "new_password2": "newhotness"
    }

.. note::

    A future version of this server may add support for social authentication
    e.g login via Facebook, Twitter or Google accounts.

.. note::

    A future version of this server may add support for API based password
    reset.

.. toctree::
    :maxdepth: 2
