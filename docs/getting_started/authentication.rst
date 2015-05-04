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
TBD - example login / *loguut*, including notes about the use of email instead of username
TBD - getting user details after login
TBD - getting and interpreting user permissions

OAuth2 Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~
TBD


Authorization
----------------
TBD - overview, how roles and permissions work
TBD - access control for GIS ( standard public role cannot get coordinates )
TBD - default data; GIS enabled public role
TBD - facility life cycle: approvals and interaction with access control
TBD - facility life cycle: regulation and interaction with access control

Permissions
~~~~~~~~~~~~~
TBD - document custom permissions, if any, plus read only API

Groups
~~~~~~~~
TBD - document role setup ( read, write )
TBD - comment about default roles

Registering users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

National and county users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD - national users, including documenting sandbox
TBD - county users, including documenting sandbox
TBD - updating user details

.. toctree::
    :maxdepth: 3
