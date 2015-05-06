Using the API - Basic Principles
==================================
.. include:: ../substitutes.txt

All the material here assumes that you already have access to an
MFL test environment.

See :doc:`sandbox` and :doc:`../installing/evaluator_install` or
:doc:`../installing/developer_install` for information on how to get
access to a test environment.

HTTP and HTTPS
---------------
All API actions are based on HTTP and its verbs e.g. ``GET`` and ``POST``.

=========== ====================================================================
 HTTP Verb   Description
=========== ====================================================================
 HEAD        Used to **retrieve header information** about a resource
 GET         Used to **retrieve a resource** and for any **read-only operation**
 POST        Used to **create a resource** and sometimes to change it
 PUT         Used to **mutate an existing resource**. We, however, encourage the use of ``PATCH`` instead of ``PUT`` whenever possible.
 PATCH       Used to **edit** an already existing resource
 DELETE      Used to **delete** an already existing resource
=========== ====================================================================

Production instances should always run over HTTPS.

Data Format
------------
The MFL API server supports JSON and XML for all API endpoints.

*Some* endpoints support CSV and Excel output. This will be indicated in the
relevant sections of the documentation.

The preferred data format is JSON. **We strongly encourage you to use JSON**
- you will find it to be more reliable, since it is the format used by the
official front-ends and is therefore extensively tested.

In order to request a specific format, you will need to learn how to use
`content negotiation`_ .

.. _`content negotiation`: http://www.django-rest-framework.org/api-guide/content-negotiation/

Content Negotiation using headers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Send the correct ``Accept`` header. For example:

**To get json**

     curl -i -H "Accept: application/json" -H "Content-Type: application/json" http://localhost:8000/api/common/contacts/

**To get xml**

    curl -i -H "Accept: application/xml" -H "Content-Type: application/xml" http://localhost:8000/api/common/contacts/

**To get csv**

     curl -i -H "Accept: application/csv" -H "Content-Type: application/csv" http://localhost:8000/api/common/contacts/

**To get a resource in Microsoft Excel format**

    curl -i -H "Accept: application/xlsx" -H "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" http://localhost:8000/api/common/contacts/

Please note that the examples above do not factor in :doc:`authentication`.

Content negotiation using query parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Append a ``?format=<>`` ``GET`` parameter. For example:

 * to get XML append ``?format=xml`` to the URL
 * to get CSV append ``?format=csv`` to the URL
 * to get Excel, append ``?format=xlsx`` to the URL
 * to get JSON ( the default ), append ``?format=json`` to the URL

Common properties
--------------------
**All** |mfl| resources have the following fields:

============= ===============================================================================
 Field          Description
============= ===============================================================================
 ``id``         A UUID. This is the database record's primary key.
 ``created``    An ISO 8601 timestamp ( UTC time zone ) that indicates when the resource was created
 ``updated``    An ISO 8601 timestamp ( UTC time zone ) that shows when the last update occured
 ``active```    A boolean; will be set to ``false`` when the record is retired
 ``deleted``    A boolean; will be set to ``true`` when the record is removed. The API will in-fact not return deleted items by default.
 ``created``    The ID of the user that created the record. The user model is the only one with non UUID primary keys.
 ``updated``    The ID of the user that last updated the record.
============= ===============================================================================

The example listing below clearly shows the shared fields:

.. code-block:: javascript

    {
        "count": 5,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "16f7593f-0a21-41b6-87f1-ef2c4ec7e029",
                "created": "2015-05-03T02:30:26.345994Z",
                "updated": "2015-05-03T02:30:26.346007Z",
                "deleted": false,
                "active": true,
                "name": "POSTAL",
                "description": null,
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "f4eaf905-be91-4050-b154-600e31510306",
                "created": "2015-05-03T02:30:26.342216Z",
                "updated": "2015-05-03T02:30:26.342229Z",
                "deleted": false,
                "active": true,
                "name": "FAX",
                "description": null,
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "f4e835d3-e6a4-4d2d-9d37-344a3da1bb0a",
                "created": "2015-05-03T02:30:26.338468Z",
                "updated": "2015-05-03T02:30:26.338481Z",
                "deleted": false,
                "active": true,
                "name": "LANDLINE",
                "description": null,
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "68281bd2-d616-418d-ab01-616a225b643b",
                "created": "2015-05-03T02:30:26.334496Z",
                "updated": "2015-05-03T02:30:26.334510Z",
                "deleted": false,
                "active": true,
                "name": "MOBILE",
                "description": null,
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "b2ce5bc9-0c73-4586-b5d2-e96c69b90b85",
                "created": "2015-05-03T02:30:26.328938Z",
                "updated": "2015-05-03T02:30:26.328956Z",
                "deleted": false,
                "active": true,
                "name": "EMAIL",
                "description": null,
                "created_by": 1,
                "updated_by": 1
            }
        ]
    }

Documentation examples
~~~~~~~~~~~~~~~~~~~~~~~~~
All the examples in this documentation will use the recommended JSON format.

Data notations
^^^^^^^^^^^^^^^
The example below demonstrates the manner in which example JSON payloads
in the documentation should be interpreted:

.. code-block:: javascript

    {
        "name": "John Doe",
        "gender": "M",
        "age": 33,
        "houses": [
            {
                "city": "Nairobi",
                "type": "Flat"
            },
            {
                "city": "Mombasa",
                "type": "Bungalow"
            }
        ],
        "phone": {
            "work": "8781923",
            "home": "213789123"
        }
    }

This table describes the data above

================  =================  ===============================
 Property          Type               Description
================  =================  ===============================
 name              string             Name of the person
 age               integer            Age of the person
 gender            string             Gender of the person
 houses            list of objects    A list of houses the person owns
 houses[ ].city    string             The city in which the house is in
 houses[ ].type    string             The type of the house
 phone             object             The person's phone numbers
 phone.work        string             Work phone number
 phone.home        string             Home phone number
================  =================  ===============================

The *[ ]* notation is used to indicate a property of every object in a list.
For example, ``houses[ ].city`` means every object in the list ``houses``
has a property called ``city``.

Data types
^^^^^^^^^^
The data types are standard `JSON`_. The MFL API uses `UUIDs`_ for its
primary keys.

===========  =====================  =====================
 Data type    JSON Representation    Description
===========  =====================  =====================
 string       string                 A sequence of zero or more characters wrapped in double quotes.
 object       object                 A collection of name-value pairs wrapped in curly braces : **{** and **}**
 list         array                  A collection of values
 boolean      boolean                Represents truthy values and falsy values.Valid values are ``true`` and ``false``
 null         null                   Represents null values
 integer      integer                Integer values
 decimal      string                 Precision decimal values represented as strings
 uuid         string                 A string of 32 characters used as a unique identifier (`UUIDs`_)
 datetime     string                 A string representing date and time values (`Dates and times`_)
 url          string                 A string representing the location of a network resource
===========  =====================  =====================

.. _`JSON`: http://www.json.org/
.. _`UUIDs`: http://en.wikipedia.org/wiki/Universally_unique_identifier

URLs
----
URLs in this document shall be written in shortform, excluding the scheme and
domain (or IP) from which |mfl| can be accessed.

For a production system, the scheme shall always be ``https``, unless
otherwise specified.

For example, if |mfl| is running from the IP *192.168.1.56*, a full URL could be ``https://192.168.1.56/api/common/contacts/``. In the documentation, the
URL shall be written as ``/api/common/contacts/``, exluding the scheme and
domain (or IP).

.. note::

    **All URLs have a trailing slash** unless specified otherwise.
    For example, the url ``https://192.168.1.56/v1/claims/`` is not equivalent
    to the url ``https://192.168.1.56/v1/claims``.
    The latter will result in a ``HTTP 404`` (Not Found) response

URL Parameters
-----------------
Any API endpoints that support url parameters shall be specified in the following format:

.. code-block:: text

    /api/common/counties/<value>/

For example to retrieve a county by its ID ( UUID ),  the URL shall be
specified as:

.. code-block:: text

    /api/common/counties/<id>/

e.g. ``/api/common/counties/89d8f3dd698b46e6a052f355a231858d/``


URL Query Parameters
----------------------
Any API endpoints that support query parameters shall be specified in the following format:

.. code-block:: text

    /api/common/counties/?name=<value>

For example to query the county endpoint by ``name``, the URL shall be
specified as:

.. code-block:: text

    /api/common/counties/?name=<name>

e.g. ``/api/common/counties/?name=Nairobi``

Dates and times
-----------------
All dates and times shall be represented as datetime strings in
`ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ format i.e.

.. code-block:: text

    YYYY-MM-DDTHH:MM:SSZ

e.g. ``2015-03-30T15:23:89Z``

If timezone is to be included, the timezone shall be ``UTC``, thus the format becomes

.. code-block:: text

    YYYY-MM-DDTHH:MM:SS+0000

e.g. ``2015-03-30T15:23:89+0000``

Any date that does not have a timezone shall be assumed to be ``UTC``.

UUIDs
-----
UUIDs are used as unique record identifiers for each record in |mfl|.
All UUIDs used in |mfl| are `version 4 UUIDs <http://tools.ietf.org/html/rfc4122.html>`_.

HTTP Errors
-----------
400 (Bad Request)
    This error occurs if the request given to the server is malformed or does not meet certain criteria e.g. invalid data.

401 (Unauthorized)
    The request to access a resource was unauthorized. (:doc:`authentication`)

403 (Forbidden)
    The authorized user does not have permission to access a resource (:doc:`authentication`)

404 (Not found)
    The requested resource was not found

410 (Gone)
    The requested resource has been removed

500 (Server Error)
    A server error has occurred

Pagination
----------
Endpoints that return multiple items will be paginated with a page size of 25
by default. All endpoints returning a list of items shall have the following
format:

.. code-block:: text

    GET /api/common/constituencies/?page=2


.. code-block:: javascript

    {
    "count": 290,
    "next": "http://localhost:8000/api/common/constituencies/?page=3",
    "previous": "http://localhost:8000/api/common/constituencies/",
    "results": [
        {
            ... // list of items requested, in this case constituencies
        ]
    }

Audit trail
-------------
The API server provides an audit trail for all non third-party resources.
This audit trail can be accessed on **detail endpoints** by appending an
`include_audit=true` query parameter.

For example, if there was a contact with `id`
`28d2a0c8-40f4-4686-97d0-d7c6f453fcb3`, a `GET` request to
`/api/common/contacts/28d2a0c8-40f4-4686-97d0-d7c6f453fcb3/?include_audit=true`
would return a payload that has a `revisions` key that contains a
representation of every past revision of that specific contact.

.. toctree::
    :maxdepth: 2
