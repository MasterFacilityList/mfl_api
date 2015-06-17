Facilities
=============
This chapter assumes that the reader is familiar with the general
principles explained in the :doc:`06_api` chapter.

The MFL is not merely a "list" of facilities; it has rich APIs to manage their
life cycles and to support interaction with other healthcare systems. This
chapter concerns itself with what is arguably the "core" of the MFL system
- the maintenance of facility information. Facilities APIs fall into the
following groups:

============================== ================================================
Function                       Resources / APIs
============================== ================================================
Facility Information storage    * Facility
                                * Facility Physical Addresses
                                * Facility Contacts
                                * Facility Units
                                * Facility Services

Facility Workflow / Life cycle  * Approval
                                * Publishing ( synchronization )
                                * Regulation
                                * Upgrade
                                * Downgrade

Facility ratings                * Facility service ratings
                                * Facility ratings report

Facility downloads              * Facility cover letters
                                * Facility correction templates
                                * Facility excel exports

Facility dashboard APIS         * Analysis by administrative units
                                * Analysis by type
                                * Analysis by owner and owner category
                                * Analysis by regulator and regulation status
============================== ================================================

.. note::

    One of the things associated with facilities that are registered on the
    Master Facilities List is a **Master Facilities List ( MFL ) Code**.

    The MFL code is a unique number ( integral ) that is *sequential* and
    *immutable*. The immutability is taken seriously - the MFL codes that
    were issued under the first generation system will not be re-issued under
    the second generation MFL system.

    Codes that are issued under MFL 2 will start at `100000`.

Facility information storage
-------------------------------

.. note::

    These APIs are the "heart" of the MFL system. A well-behaved front-end
    should take an integrated approach, presenting output from these APIs
    under one set of screens ( instead of five sets, one for each resource
    type ).

Facilities
+++++++++++++
Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The facilities that are currently registered can be listed at
``/api/facilities/facilities/``.

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each facility has a UUID ``id``. A facility's detail record can be listed
at ``/api/facilities/facilities/<id>/``. For example: if a facility
record's ``id`` is ``2927d31f-b1a0-4d17-93b0-ea648af7b9f0``, the detail
URL for the facility record will be ``/api/facilities/facilities/2927d31f-b1a0-4d17-93b0-ea648af7b9f0/``.

Filtering and search
~~~~~~~~~~~~~~~~~~~~~~~
Facilities - as listed at ``/api/facilities/facilities/`` can be filtered using
the following:

==================== ==========================================================
Filter               Explanation
==================== ==========================================================
name                 This does a *case insensitive partial match* but accepts only one name to filter by e.g ``/api/facilities/facilities/?name=molo``.
code                 Filter by **one or more** facility codes e.g ``/api/facilities/facilities/?code=15003,15002``. The ``,`` is used to separate individual parameters. This does exact matches.
description          Similar to ``name`` but operating on descriptions e.g ``/api/facilities/facilities/?name=molo``
facility_type        Filter by the ``id``s of one or more facility types e.g ``/api/facilities/facilities/?facility_type=f25ba517-3b8d-4692-ba7b-3524f6ec58e5,b2225473-08f1-4e86-a47a-0a61cf75e731``. Facility types can be listed at ``/api/facilities/facility_types/``.
operation_status     Filter by the ``id`` of one or more operation statuses from ``/api/facilities/facility_status/``
ward                 Filter by the ``id`` of wards ( from ``/api/common/wards/`` e.g ``/api/facilities/facilities/?ward=353404d7-02e6-422f-b64f-b1c7d0f1bcf0`` )
county                 Filter by the ``id`` of counties ( from ``/api/common/counties/`` e.g ``/api/facilities/facilities/?county=fa47afa2-a78a-421f-ad9f-55e6cbfc280c`` )
constituency                 Filter by the ``id`` of constituencies ( from ``/api/common/constituencies/`` e.g ``/api/facilities/facilities/?constituencies=93280ce0-670f-4b96-a449-57d65f0dcace`` )
owner                Filter by the ``id`` of one or more owners. Owners can be listed at ``/api/facilities/owners/``
owner_type               Filter by the ``id`` of one or more owner types. Owner types can be listed at ``/api/facilities/owner_types/``
officer_in_charge    Filter by the ``id`` of one or more officers-in-charge. The officers can be listed at ``/api/facilities/officers/``
number_of_beds       Filter by the number of beds, supplying one or more filter parameters e.g ``/api/facilities/facilities/?number_of_beds=20,21,22,23,24``
number_of_cots       Filter by the number of cots, supplying one ormore filter parameters e.g ``/api/facilities/facilities/?number_of_cots=10,11,12``
open_whole_day       A boolean filter e.g ``/api/facilities/facilities/?open_whole_day=true``
open_whole_week      A boolean filter e.g ``/api/facilities/facilities/?open_whole_week=true``
is_classified        A boolean filter that determines if a facility's coordinates should be shown or not. The public front-end should omit classified facilities by default. i.e. publish those that can be listed with ``/api/facilities/facilities/?is_classified=false``
is_published         A boolean filter that determines if a facility has been cleared for display on the public site. The public site should only display facilities that can be listed with ``/api/facilities/facilities/?is_published=true``
is_regulated         The facilities that are pending action from the regulators can be listed with ``/api/facilities/facilities/?is_regulated=False``
==================== ==========================================================

The following filters are common to **all** list endpoints in this API,
other than ``/api/users/``.

==================== ==========================================================
Filter               Explanation
==================== ==========================================================
updated_before       The most recently updated facilities can be listed with a query similar to ``/api/facilities/facilities/?updated_before=2015-05-09T08:57:48.094112Z``. The datetime is in ISO 8601 format.
created_before       Similar to ``updated_before``, but operating on creation dates. Creation dates are not "touched" after the initial creation of the resource.
updated_after        Similar to ``updated_before``, but returns records newer than the specified datetime
created_after        Similar to ``updated_after``, but works with creation dates.
updated_on           This is similar to the date filters above but performs **exact matches** on the update date.
created_on           This is also performs exact matches.
is_active            For all resources in this server, the preferred way to "retire" records is to mark them as inactive. This allows the API client to request only active or only inactive records.
search               Perform a full text search that looks through all fields. e.g ``/api/facilities/facilities/?search=endebess`` gives back all facilities that have "endebess" anywhere in their name, description or attributes.
==================== ==========================================================

.. note::

    These filters can be combined / chained.

    For example: ``/api/facilities/facilities/?ward=353404d7-02e6-422f-b64f-b1c7d0f1bcf0&open_whole_day=true``

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
The following are the important fields when adding a new facility:

=================== ===========================================================
Field               Explanation
=================== ===========================================================
name                The name of the faciity e.g "Musembe Dispensary (Lugari)"
abbreviation        A shortened name
description         Free text that supplies any additional detail that is required
location_desc       An explanation of the location, in "plain" language e.g "Eldoret - Webuye Highway (at Musembe Mkt junction)"
number_of_beds      The number of beds as per the facility's license
number_of_cots      The number of cots as per the facility's license
open_whole_day      `true` if the facility is a 24 hour operation
open_whole_week     `true` if the facility is a 7 day operation
facility_type       An ``id``, obtained by listing ``/api/facilities/facility_types/``
operation_status    An ``id``, obtained from ``/api/facilities/facility_status/``. This is the overall state of the facility e.g "Operational" or "Not Operational"
ward                An ``id``, obtained from ``/api/common/wards/``. Facilities are attached at the level of the smallest administrative area ( the ward ).
owner               An ``id``, obtained from ``/api/facilities/owners/``.
officer_in_charge   An ``id``, obtained from ``/api/facilities/officers/``
physical_address    An ``id``, obtained from ``/api/common/address/``
parent              Optional. If a facility is a "branch" of a larger facility, the ``id`` of the parent facility should be supplied here.
=================== ===========================================================

The following example illustrates a valid ``POST`` payload:

.. code-block:: javascript

    {
        "name": "Demo Facility",
        "abbreviation": "DEMOFAC",
        "description": "This is an example in the documentation",
        "location_desc": "Planet: Mars",
        "number_of_beds": 20,
        "number_of_cots": 0,
        "open_whole_day": true,
        "open_whole_week": true,
        "facility_type": "db8f93ad-b558-405a-89b5-a0cdb318ee6e",
        "operation_status": "ee194a52-db9d-401c-a2ef-9c8225e501cd",
        "ward": "a64d930d-883e-4b96-ba39-c792a1cd04f2",
        "owner": "f4c7ca47-7ee6-4795-ac1c-a5d219e329ad",
        "officer_in_charge": "972c9c96-fe27-4803-b6f8-c933310e2f44",
        "physical_address": "88dde94b-dc42-4b13-b1cb-05eca047678c",
        "parent": null
    }

A successful ``POST`` will get back a ``HTTP 201 Created`` response. A
representation of the freshly created resource will be returned in the
response.

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to update an existing record, ``PATCH`` the appropriate field from
the record's detail view.

For example, if the facility that we created above got the ``id`` set to
``e88f0c1a-e1e4-44ff-8db1-8c4135abb080`` ( this will be returned to the client
in the resource returned after successful creation ), we can change its
``location_desc`` from "Planet: Mars" to "Planet: Venus" by sending a
``PATCH`` to ``/api/facilities/facilities/e88f0c1a-e1e4-44ff-8db1-8c4135abb080/`` with the
following payload:

.. code-block:: javascript

    {
        "location_desc": "Planet: Venus"
    }

A successful ``PATCH`` will get back a ``HTTP 200 OK`` response and a
representation of the freshly updated resource will be returned.

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
In order to delete the record that we just created, send a ``DELETE`` with an
empty payload to the detail URL i.e. to ``/api/facilities/facilities/e88f0c1a-e1e4-44ff-8db1-8c4135abb080/`` in the example above.

A successful ``DELETE`` will get back a ``HTTP 204 NO CONTENT`` response.

Physical addresses
++++++++++++++++++++++++++++++
Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The physical addresses known to the system can be listed at
``/api/common/address/``.

In addition to the common filters that are already explained above,
physical addresses have the following extra filters:

=================== ===========================================================
Field               Explanation
=================== ===========================================================
town                Filter by the ``id`` of a town. Towns can be listed at ``/api/common/towns/`` e.g ``/api/common/address/?town=b2af0361-c924-4ba2-9bc6-82333fc0a26f``
postal_code         Filter by the ``postal_code`` e.g ``/api/common/address/?postal_code=00100``
address             Filter by the actual text of the address itself e.g ``/api/common/address/?address=P.O.%20Box%201``
nearest_landmark    Filter by the contents of the ``nearest_landmark`` field e.g ``/api/common/address/?nearest_landmark=kicc``
plot_number         Filter by the ``plot_number`` field e.g ``/api/common/address/?plot_number=940``
=================== ===========================================================

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The detail endpoint is ``/api/common/address/<id>/`` e.g
``/api/common/address/20d01a89-f6b5-4a4d-b788-32182d427c18/`` for the address
whose ``id`` is ``20d01a89-f6b5-4a4d-b788-32182d427c18``.

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
Supply the following fields:

=================== ===========================================================
Field               Explanation
=================== ===========================================================
postal_code         A valid postal code e.g "00100"
address             An address e.g "No. 11A, Kabarnet Court, off Kabarnet Road" or "P.O. Box 5980"
nearest_landmark    Free text, left to the discretion of the person creating the record
plot_number         Free text, left to the discretion of the person entering the record
town                The ``id`` of a town, as listed at ``/api/common/towns/``
=================== ===========================================================

.. code-block:: javascript

    {
        "postal_code": "00100",
        "address": "No. 11A, Kabarnet Court, off Kabarnet Road",
        "nearest_landmark": "Kingdom Business Centre",
        "plot_number": "-",
        "town": "b2af0361-c924-4ba2-9bc6-82333fc0a26f"
    }

A successful ``POST`` will get back a ``HTTP 201 Created`` response. A
representation of the freshly created resource will be returned in the
response.

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``PATCH`` the detail endpoint above e.g to set the ``plot_number`` for the
example record above, send the following ``PATCH`` payload to
``/api/common/address/20d01a89-f6b5-4a4d-b788-32182d427c18/``:

.. code-block:: javascript

    {
        "plot_number": "250"
    }

A successful ``PATCH`` will get back a ``HTTP 200 OK`` response. A
representation of the updated resource will be returned in the
response.

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
Send a ``DELETE`` request to the detail endpoint. In the example above,
the ``DELETE`` would be sent to ``/api/common/address/20d01a89-f6b5-4a4d-b788-32182d427c18/``.

A successful ``DELETE`` will get back a ``HTTP 204 NO CONTENT`` response.

Facility contacts
+++++++++++++++++++
Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Facility contacts can be listed at ``/api/facilities/contacts/``.

In addition to the common contacts that are already explained above,
facility contacts have the following extra fields:

=================== ===========================================================
Field               Explanation
=================== ===========================================================
facility            The ``id`` of the relevant facility, as listed at ``/api/facilities/facilities/`` e.g ``/api/facilities/contacts/?facility=faaefb75-dba4-4564-8acb-6b947685de24``
contact             The ``id`` of a contact, as listed at ``/api/common/contacts/`` e.g ``/api/facilities/contacts/?contact=2f5fe4c2-0371-4ba0-ba31-79d997d71c6a``
=================== ===========================================================

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The detail endpoint is ``/api/facilities/contacts/<id>/``. For example, the
detail URL for the facility contact whose ``id`` is
``9641f588-a5c0-4c0d-ad13-cfcf98a2fb7`` is
``/api/facilities/contacts/9641f588-a5c0-4c0d-ad13-cfcf98a2fb7``.

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
The only required fields are the ``facility`` and ``contact`` ( as documented
above ).

The following example is a valid ``POST`` payload:

.. code-block:: javascript

    {
        "facility": "faaefb75-dba4-4564-8acb-6b947685de24",
        "contact": "2f5fe4c2-0371-4ba0-ba31-79d997d71c6a"
    }

A successful ``POST`` will get back a ``HTTP 201 Created`` response. A
representation of the freshly created resource will be returned in the
response.

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``PATCH`` the detail endpoint with the new values e.g to change the contact in
the record above, a valid ``PATCH`` payload could be:

.. code-block:: javascript

    {
        "contact": "516f64b5-a12c-4323-b918-a5512b4baf6a"
    }

A successful ``PATCH`` will get back a ``HTTP 200 OK`` response. A
representation of the updated resource will be returned in the
response.

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
Send a ``DELETE`` request to the detail endpoint.

A successful ``DELETE`` will get back a ``HTTP 204 NO CONTENT`` response.

Facility units
++++++++++++++++
A facility may contain within it multiple semi-independent units e.g a
pharmacy, a lab and a radiology unit.

.. note::

    These units may fall under the scope of different regulators. This API
    server does not currently handle that.

Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Facility units can be listed via a ``GET`` to ``/api/facilities/facility_units/``.

In addition to the common filters, facility units can be filtered by the
following fields:

=================== ===========================================================
Field               Explanation
=================== ===========================================================
facility            The ``id`` of the facility, as listed at ``/api/facilities/facilities/`` e.g ``/api/facilities/facility_units/?facility=faaefb75-dba4-4564-8acb-6b947685de24``
name                The name of the facility unit e.g ``/api/facilities/facility_units/?facility=faaefb75-dba4-4564-8acb-6b947685de24&name=pharmacy``
description         The description of the facility unit e.g ``/api/facilities/facility_units/?facility=faaefb75-dba4-4564-8acb-6b947685de24&description=hospital%20pharmacy``
=================== ===========================================================

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A single facility unit record can be retrieved at its detail endpoint i.e
 ``/api/facilities/facility_units/<id>/`` e.g
 ``/api/facilities/facility_units/1fcc5c30-9170-4c9d-8d05-9695ba81a08c/``.

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
When adding a new facility unit, the fields of interest are the ``name``,
``description`` and ``facility``.

The following is a valid ``POST`` payload for ``/api/facilities/facility_units/``:

.. code-block:: javascript

    {
        "name": "Pharmacy",
        "description": "Hospital Pharmacy",
        "facility": "faaefb75-dba4-4564-8acb-6b947685de24"
    }

A successful ``POST`` will get back a ``HTTP 201 Created`` response. A
representation of the freshly created resource will be returned in the
response.

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A ``PATCH`` to the detail endpoint will update the relevant field(s):
For example:

.. code-block:: javascript

    {
        "description": "Community Pharmacy"
    }

A successful ``PATCH`` will get back a ``HTTP 200 OK`` response. A
representation of the updated resource will be returned in the
response.

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
Send a ``DELETE`` request to the detail endpoint.

A successful ``DELETE`` will get back a ``HTTP 204 NO CONTENT`` response.

Facility services
++++++++++++++++++++
These APIs link facilities to :doc:`09_services`.

Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The currently registered facility services can be listed via ``GET`` to
``/api/facilities/facility_services/``.

In addition to the standard filters, facility services have the following
additional filters:

=================== ===========================================================
Field               Explanation
=================== ===========================================================
facility            ``id`` of a facility, as obtained from ``/api/facilities/facilities/``
selected_option     ``id`` of a service catalog service option, as obtained from ``/api/facilities/service_options/``
=================== ===========================================================

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A facility service record can be retrieved at
``/api/facilities/facility_services/<id>/`` e.g
``/api/facilities/facility_services/df6bc639-1d9b-49f8-8f95-51e6de9c93e2/``
for the facility service whose ``id`` is ``df6bc639-1d9b-49f8-8f95-51e6de9c93e2``.

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
To  associate a facility with a service, the required fields are ``facility``
and ``selected_option``.

The following is an example ``POST`` payload:

.. code-block:: javascript

    {
        "service": "f465cb89-995c-4004-9f32-1d97fa6d0eb2",
        "option": "f465cb89-995c-4004-9f32-1d97fa6d0eb2"
    }

A successful ``POST`` will get back a ``HTTP 201 Created`` response. A
representation of the freshly created resource will be returned in the
response.

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Issue a ``PATCH`` to the detail endpoint with the new value. For example, to
change the option the example record we created above, the following payload
could be sent via ``PATCH`` to
``/api/facilities/facility_services/df6bc639-1d9b-49f8-8f95-51e6de9c93e2/``:

.. code-block:: javascript

    {
        "option": "7dde4be8-1c1e-43ce-8569-eebb63bcb329"
    }

A successful ``PATCH`` will get back a ``HTTP 200 OK`` response. A
representation of the updated resource will be returned in the
response.

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
Issue a ``DELETE`` to the detail endpoint.

A successful ``DELETE`` will get back a ``HTTP 204 NO CONTENT`` response.

Facility workflows
---------------------

.. note::

    These five workflows are the day-to-day operations performed on the MFL
    system. A well behaved front-end should integrate them into the facility
    information screens that handle the facility information services mentioned
    above, rather than give each of these its own set of screens.

.. note::

    These workflows have multiple interactions with the role based access
    control setup.

The facility "publishing" workflow
++++++++++++++++++++++++++++++++++++
The first generation MFL system had a notion of "synchronizing" facility
records to the "public site". This notion arose beceause the "public" MFL
system was a separate system.

This API does away with that notion. All applications - admin or public, web
or mobile - share the same API. Facilities that should be seen in the public
API have ``is_published`` set to ``true`` and ``is_classified`` set to
``false``.

.. note::

    When ``is_classified`` is ``true``, a user accessing the public site will
    need to be logged in with an account that has a the
    ``view_classified_facilities`` permission.

To "publish" a facility, simply ``PATCH`` the facility's detail URL and set
``is_published`` to ``true``. Newly created facilities are not published by
default.

To "classify" a facility, ``PATCH`` its detail endpoint with ``is_classified``
set to ``true``. A facility is not classified by default.

.. note::

    The public user interface should add an ``is_published=true`` filter to
    every request made to the facilities endpoints. For an unauthenticated
    user, it should also append ``is_classified=false`` to every call to the
    facilities list endpoint.

    The administration user interface should implement role based access
    control, limiting publishing to users with the ``publish_facilities``
    permission.


Facility ratings
-------------------
Ratings are scores given to a facility's services. One facility service can be rated by multiple users.
One user, can rate multiple facility services.

The scores given to a service range from 1 to 5, with 1 being the lowest score
and 5 being the highest score.

.. note::

    The facility ratings APIs will be used by both the public and
    administration user interfaces. The public interface's concern is to
    facilitate ratings by the general public. The admninistration interface
    will present read-only summary information.

Facility service ratings
+++++++++++++++++++++++++++
To rate a facility service, simply make a ``POST`` to ``api/facilities/facility_service_ratings/`` with the
facility_service's ``id`` and the score given. For example,

.. code-block:: javascript

    {
        "facility_service": "80613650-f765-4032-a9d3-bb0fc9cc37cc",
        "rating": 3
    }

Facility rating reports
++++++++++++++++++++++++++
The rating reports available include:

1) number of users with specific rating/score
2) sorting of facilities by average score
3) sorting of facility services by average score
4) sorting of facility services in a facility by average score


Facility downloads
-----------------------

.. note::

    Some of these downloads e.g the facility correction template are there for
    historical reasons. A better approach would involve the use of mobile
    interfaces ( supported by this server's APIs ) to facilitate data
    collection and data updates in the field.

Facility cover letters
+++++++++++++++++++++++++

To **view** a facilities cover letter:

``GET`` the URL ``api/facilities/facility_cover_report/<facility_id>/``

To get the cover letter in PDF:
``GET the URL ``api/common/dowload_pdf/?file_url=api/facilities/facility_cover_report/<facility_id>/&file_name=<file_name>``



Facility correction templates
++++++++++++++++++++++++++++++++
To view a facility's correction template:

``GET`` the URL ``api/facilities/facility_correction_template/<id>/``

To get a PDF of the correction template:
``GET`` the URL ``api/common/dowload_pdf/?file_url=api/facilities/facility_correction_template/<facility_id>/&file_name=<file_name>``


Facilty Inspection Report
++++++++++++++++++++++++++

To view a facility's inspection report:
``GET`` the URL ``api/facilities/facility_inspection_report/<facility_id>/``

To get a PDF of the inspection report:
``GET`` ``api/common/dowload_pdf/?file_url=api/facilities/facility_inspection_report/<facility_id>/&file_name=<file_name>``

Facility Excel reports
+++++++++++++++++++++++++

.. note::

    The authors of this API treated Excel and CSV output as simply **one more
    format that data can be exported into**. Excel and CSV data comes from the
    same serializers that produce the standard API JSON and XML output. This
    has two positive effects:

        * it can use all the available filters
        * every list API endpoint ( not just the facilities list API endpoint ) can produce CSV and Excel

    e.g. to get an excel file of facilities:
    ``GET`` the URL ``api/facilities/facilities/?format=excel``


Facility dashboard APIs
++++++++++++++++++++++++++
This API is accesbile by administrators at both the county and the National level.
The dashboard API does a high level analysis of different aspects of the facilities.
Currently, it supports analysis of facilities by owners, administrative units,
facility types, facility owner types and analysis by time created.


To get the analyzed data:
``GET`` the URL ``api/facilities/dashboard/``.
The data that the endpoint responds with is dependent upon the priviledges of the user logged in.

For a **National user**, the following response is expected

.. code-block:: javascript

    {
        "owners_summary": [
            {
                "count": 5,
                "name": "State Coorporation"
            },
            {
                "count": 1203,
                "name": "Private Enterprise (Institution)"
            },
            {
                "count": 0,
                "name": "NOT IN LIST"
            },
            {
                "count": 3,
                "name": "Humanitarian Agencies"
            },
            {
                "count": 179,
                "name": "Private Practice - Unspecified"
            },

        ],
        "recently_created": 8361,
        "county_summary": [
            {
                "count": 784,
                "name": "NAIROBI"
            },
            {
                "count": 392,
                "name": "MERU"
            },
            {
                "count": 379,
                "name": "NAKURU"
            },
            {
                "count": 363,
                "name": "KITUI"
            },
            {
                "count": 358,
                "name": "NYERI"
            },
            {
                "count": 333,
                "name": "KIAMBU"
            },
            {
                "count": 267,
                "name": "KAJIADO"
            },
            {
                "count": 256,
                "name": "MOMBASA"
            },
            {
                "count": 243,
                "name": "MACHAKOS"
            },
            {
                "count": 233,
                "name": "KILIFI"
            }
        ],
        "total_facilities": 8361,
        "status_summary": [
            {
                "count": 0,
                "name": "Facility_Gazette_By_ID"
            },
            {
                "count": 0,
                "name": "PENDING"
            },
            {
                "count": 0,
                "name": "Not-Operational"
            },
            {
                "count": 8361,
                "name": "OPERATIONAL"
            },
            {
                "count": 0,
                "name": "Licensing"
            },
            {
                "count": 0,
                "name": "Registration"
            },
            {
                "count": 0,
                "name": "Gazettment"
            }
        ],
        "owner_types": [
            {
                "count": 0,
                "name": "Other"
            },
            {
                "count": 268,
                "name": "Non-Governmental Organizations"
            },
            {
                "count": 3226,
                "name": "Private Institutions and Private Practice"
            },
            {
                "count": 853,
                "name": "Faith Based Organization"
            },
            {
                "count": 356,
                "name": "Other Public Institution"
            },
            {
                "count": 3658,
                "name": "Ministry of Health"
            }
        ],
        "constituencies_summary": [],
        "types_summary": [
            {
                "count": 119,
                "name": "District Hospital"
            },
            {
                "count": 901,
                "name": "Health Centre"
            },
            {
                "count": 3808,
                "name": "Dispensary"
            }
        ]
    }

For a **County user** (Mombasa County in this case), the following response is expected

.. code-block:: javascript

    {
        "owners_summary": [

            {
                "count": 5,
                "name": "Local Authority T Fund"
            },
            {
                "count": 33,
                "name": "Community Development Fund"
            },
            {
                "count": 78,
                "name": "Company Medical Service"
            },
            {
                "count": 265,
                "name": "Non-Governmental Organizations"
            },
            {
                "count": 225,
                "name": "Other Faith Based"
            },
            {
                "count": 10,
                "name": "Supreme Council for Kenya Muslims"
            },

        ],
        "owner_types": [
            {
                "count": 189,
                "name": "Private Institutions and Private Practice"
            },
            {
                "count": 10,
                "name": "Faith Based Organization"
            },
            {
                "count": 27,
                "name": "Other Public Institution"
            },
            {
                "count": 23,
                "name": "Ministry of Health"
            }
        ],
        "constituencies_summary": [
            {
                "count": 71,
                "name": "MVITA"
            },
            {
                "count": 49,
                "name": "LIKONI"
            },
            {
                "count": 46,
                "name": "NYALI"
            },
            {
                "count": 44,
                "name": "CHANGAMWE"
            },
            {
                "count": 25,
                "name": "KISAUNI"
            },
            {
                "count": 21,
                "name": "JOMVU"
            }
        ],
        "types_summary": [
            {
                "count": 2735,
                "name": "Medical Clinic"
            },
            {
                "count": 196,
                "name": "Other Hospital"
            },
            {
                "count": 119,
                "name": "Sub-District Hospital"
            },
            {
                "count": 172,
                "name": "Nursing Home"
            }

        ]
    }


Facility types
==============
There are many types of facilities ranging from health centers,
hospitals, dispensaries, national hospitals etc.

Facility types form the basis of upgrading and downgrading of facilities.

A facility type has five distinct fields:

================ ==============================================================
    Field          Explanation
================ ==============================================================
    id            The primary key of the facility type

    name           The name of the facility type e.g HEALTH_CENTER

    sub-division   A sub-division of the facility type e.g A hospitla has got
                   several sub divisions e.g District Hospital of Provincial
                   Hospital

    preceeding    A facility type that comes before the type e.g a Provincial
                  Hospital comes before a National Hospital
================ ==============================================================


Creating A facility type
------------------------
``POST`` to ``api/facilities/facility_types/`` a payload similar to the one below

.. code-block:: javascript

    {
        "name": "Hospital",
        "sub_division": "Provincial Hospital",
        "preceding": "950047f7-dae4-4803-9818-9886004daaf1"
    }


Expected Response Code:
    ``HTTP 201 CREATED``

Expected sample data:

.. code-block:: javascript

    {
        "id": "11494347-f40c-4fbb-8632-cc1f35fe1fc9",
        "created": "2015-05-21T14:38:03.298142Z",
        "updated": "2015-05-21T14:38:03.298162Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "Hospital",
        "sub_division": "Provincial Hospital",
        "created_by": 1,
        "updated_by": 1,
        "preceding": "950047f7-dae4-4803-9818-9886004daaf1"
    }




Listing Facillity types
-----------------------
``GET`` the URL ``api/facilities/facility_types/``

Sample Response data:

.. code-block:: javascript

        {
            "count": 27,
            "next": "http://localhost:8000/api/facilities/facility_types/?page=2",
            "previous": null,
            "results": [
                {
                    "id": "11494347-f40c-4fbb-8632-cc1f35fe1fc9",
                    "created": "2015-05-21T14:38:03.298142Z",
                    "updated": "2015-05-21T14:38:03.298162Z",
                    "deleted": false,
                    "active": true,
                    "search": null,
                    "name": "Hospital",
                    "sub_division": "Provincial Hospital",
                    "created_by": 1,
                    "updated_by": 1,
                    "preceding": "950047f7-dae4-4803-9818-9886004daaf1"
                },
                {
                    "id": "950047f7-dae4-4803-9818-9886004daaf1",
                    "created": "2015-05-15T13:45:13.592372Z",
                    "updated": "2015-05-15T13:45:13.592404Z",
                    "deleted": false,
                    "active": true,
                    "search": null,
                    "name": "District Hospital",
                    "sub_division": null,
                    "created_by": 1,
                    "updated_by": 1,
                    "preceding": null
                }
            ]
    }

Expected Response code:
    ``HTTP 200 OK``


Retrieving a facility type
---------------------------
``GET`` the URL ``api/facilities/facility_types/<id>/``

For example to get the details of a facility type whose is
``950047f7-dae4-4803-9818-9886004daaf1``  do a ``GET`` to the URL
``api/facilities/facility_types/950047f7-dae4-4803-9818-9886004daaf1/``

Sample Response data:

.. code-block:: javascript

    {
        "id": "950047f7-dae4-4803-9818-9886004daaf1",
        "created": "2015-05-15T13:45:13.592372Z",
        "updated": "2015-05-15T13:45:13.592404Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "District Hospital",
        "sub_division": null,
        "created_by": 1,
        "updated_by": 1,
        "preceding": null
    }


Expected Response code
    ``HTTP 200 OK``


Updating Facility types
-----------------------
``PATCH`` the URL ``api/facilities/facility_types/<id>/`` with a payload
containing the fields to be edited. For example to update a facility type's
name whose id is 950047f7-dae4-4803-9818-9886004daaf1 do a ``PATCH`` to the URL
``api/facilities/facility_types/950047f7-dae4-4803-9818-9886004daaf1/``
with a  payload similar to the one below

.. code-block:: javascript

    {
        "name": "District Hospital Edited"
    }

Sample Expected Response data:

.. code-block:: javascript

    {
        "id": "950047f7-dae4-4803-9818-9886004daaf1",
        "created": "2015-05-15T13:45:13.592372Z",
        "updated": "2015-05-15T13:45:13.592404Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "District Hospital Edited",
        "sub_division": null,
        "created_by": 1,
        "updated_by": 1,
        "preceding": null,
    }

Expected Response Code:
    ``HTTP 200 OK``


Facility Upgrades and Downgrades
================================

Upgrading or downgrading a facility is as easy as changing the
facility type of a facility to another type. The person doing this should
have the sufficient permssions to do so.
This is however a two step process. The First step involves making the upgrade
or the downgrade and the second involves confirming the upgrade or the
downgrade.

Upgrading/Downgrading a Facility (First Step)
---------------------------------------------
``POST`` to ``api/facilities/facility_upgrade/`` a payload similar to the one
shown below

.. code-block:: javascript

    {
        "reason": "A good reason for the upgrade",
        "facility": "cc585b49-dc42-47a3-a08a-7f2c39633393", // id of the facility
        "facility_type": "57a0351b-accd-4ccf-b19f-38920ea78e75" // id of the facility type
    }

Sample Response Data:

.. code-block:: javascript

    {
        "id": "70610b2b-ddd8-49b4-8594-52c236a834d2",
        "created": "2015-05-21T15:37:56.240505Z",
        "updated": "2015-05-21T15:37:56.240522Z",
        "deleted": false,
        "active": true,
        "search": null,
        "reason": "A good reason for the upgrade",
        "is_confirmed": false,
        "is_cancelled": false,
        "created_by": 3,
        "updated_by": 3,
        "facility": "cc585b49-dc42-47a3-a08a-7f2c39633393",
        "facility_type": "57a0351b-accd-4ccf-b19f-38920ea78e75"
    }

Expected Response Code:
    ``HTTP 201 CREATED``


Confirming Upgrade or Downgrade (Second Step)
---------------------------------------------
The CHRIO may choose to either to confirm or cancel a facility upgrade
or downgrade.

To confirm a facility upgrade/downgrade ``PATCH``
``api/facilities/facility_upgrade/<id>/`` where the ``id`` identifies a particular
facility upgrade/downgrade.

For example to confirm the facility upgrade done above do a ``PATCH`` to
``api/facilities/facility_upgrade/70610b2b-ddd8-49b4-8594-52c236a834d2``
with the payload below:

.. code-block:: javascript

    {
        "is_confirmed": true
    }


Expected Response data:

.. code-block:: javascript

    {
        "id": "70610b2b-ddd8-49b4-8594-52c236a834d2",
        "created": "2015-05-21T15:37:56.240505Z",
        "updated": "2015-05-21T15:37:56.240522Z",
        "deleted": false,
        "active": true,
        "search": null,
        "reason": "A good reason for the upgrade",
        "is_confirmed": true,
        "is_cancelled": false,
        "created_by": 3,
        "updated_by": 3,
        "facility": "cc585b49-dc42-47a3-a08a-7f2c39633393",
        "facility_type": "57a0351b-accd-4ccf-b19f-38920ea78e75"
    }

Expected HTTP Response code
    ``HTTP 200 OK``


Cancelling a facility upgrade/downgrade(Second Step)
----------------------------------------------------
Cancelling a facility upgrade or downgrade is very similar to confirming a
facility upgrade with a minor change
in the payload sent.

Do a ``PATCH``  to the url ``api/facilities/facility_upgrade/<id>/``
with a payload similar to the one shown below:

.. code-block:: javascript

    {
        "is_cancelled": true
    }


.. note::

    It is after the confirmation of a facility upgrade or downgrade that a facility
    is deemed to have been upgraded or downgraded and the changes reflected in
    the facility.

Listing Facilities that are due for upgrade/downgrade Confirmation
------------------------------------------------------------------
``GET`` the URL ``/api/facilities/facility_upgrade/?is_confirmed=false``


Sample Response data:

.. code-block:: javascript

        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": "70610b2b-ddd8-49b4-8594-52c236a834d2",
                    "created": "2015-05-21T15:37:56.240505Z",
                    "updated": "2015-05-21T15:37:56.240522Z",
                    "deleted": false,
                    "active": true,
                    "search": null,
                    "reason": "A good reason for the upgrade",
                    "is_confirmed": false,
                    "is_cancelled": false,
                    "created_by": 3,
                    "updated_by": 3,
                    "facility": "cc585b49-dc42-47a3-a08a-7f2c39633393",
                    "facility_type": "57a0351b-accd-4ccf-b19f-38920ea78e75"
                }
        ]
    }


Expected Response code:
    ``HTTP 200 OK``

Listing all the facilties whose upgrades and downgrades have been declined:
``GET`` the URL ``/api/facilities/facility_upgrade/?is_cacelled=true``

The resulting payload and expected response code are similar the ones above


Listing all the the Upgrades/Downgrades of a facility
-----------------------------------------------------
``GET`` the URL ``/api/facilities/facility_upgrade/?facility=<id>``

For example a get to the URL
``api/facilities/facility_upgrade/?facility=cc585b49-dc42-47a3-a08a-7f2c3963339311``
results in the data shown below and the a response code of ``HTTTP 200 OK``

.. code-block:: javascript

    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "70610b2b-ddd8-49b4-8594-52c236a834d2",
                "created": "2015-05-21T15:37:56.240505Z",
                "updated": "2015-05-21T15:37:56.240522Z",
                "deleted": false,
                "active": true,
                "search": null,
                "reason": "A good reason for the upgrade",
                "is_confirmed": true,
                "is_cancelled": true,
                "created_by": 3,
                "updated_by": 3,
                "facility": "cc585b49-dc42-47a3-a08a-7f2c39633393",
                "facility_type": "57a0351b-accd-4ccf-b19f-38920ea78e75"
            }
        ]
    }


.. toctree::
    :maxdepth: 2
