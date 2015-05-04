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
TBD - port documentation from docstring

Authorization
----------------
TBD - define RBAC, provide link

Understanding the role based access control setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD - getting and interpreting user permissions
TBD - overview, how roles and permissions work

National and county users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD - access control for GIS ( standard public role cannot get coordinates )
TBD - national users, including documenting sandbox
TBD - county users, including documenting sandbox

Public API clients and GIS data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD - default data; GIS enabled public role
TBD - access control for GIS ( standard public role cannot get coordinates

RBAC and the facility life cycle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD - facility life cycle: approvals and interaction with access control

RBAC and regulation
~~~~~~~~~~~~~~~~~~~~~~
TBD - facility life cycle: regulation and interaction with access control

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
