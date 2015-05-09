MFL APIs: Shared Resources and properties
===========================================
.. include:: substitutes.txt

This chapter assumes that the reader is familiar with the general
principles explained in the :doc:`api` chapter.

This chapter concerns itself with the resources that hold "setup" type
information. These resources wil often be used to populate drop-downs
and other types of choosers in the web / mobile front-ends.

Contact Types
---------------
The contact type resource allows us to move the configuration of contact types
that are recognized by the server from code to configuration.

This API will typically be used by web front-ends that need to populate
contact type selection dropdowns during the creation of contacts/

The contact type list endpoint is at ``/api/common/contact_types/`` while the
detail endpoint will be at ``/api/common/contact_types/<pk>/`` ( for example,
the contact whose id is ``3a05b4e7-fb8e-4c23-ac95-4e36ac2b99fa`` can be
retrieved by ``GET``ting
``/api/common/contact_types/3a05b4e7-fb8e-4c23-ac95-4e36ac2b99fa/`` ).

When creating a new contact, the only necessary fields are the ``name`` and
``description``. The following is a valid ``POST`` payload:

.. code-block:: javascript

    {
        "name": "KONTACT TYPE",
        "description": "Documentation Example"
    }

Towns
-------
The town resource allows us to set up the system's list of towns.

This API will typically be used by front-ends that need to populate town
selection dropdowns during the creation of facility records.

The town list endpoint is at ``/api/common/towns/``. As with every other
resource in this API, the detail endpoint will be at ``/api/common/towns/``
e.g ``/api/common/towns/e8f369f1-d115-43a1-a19b-ae40b7b4b19e/`` for a town
whose primary key is ``e8f369f1-d115-43a1-a19b-ae40b7b4b19e``.

When creating a new town, the only mandatory parameter is the ``name``. The
following is a valid ``POST`` payload:

.. code-block:: javascript

    {
        "name": "Documentation Town"
    }

Administrative units
------------------------
The second generation MFL implements the post 2010 ( Kenyan ) constitution
administrative structure. This structure has only three levels, after the
national one: counties, constituencies and wards.

There are 47 counties. Each county contains a number of constituencies - all
adding up to 290. Each constituency in turn contains a number of wards - all
adding up to 1450.

The constituencies will sometimes be referred to as "sub-counties". The wards
often - ut not always - correspond to locations in the previous administrative
structure.

It is unlikely that an API client will need to alter the administrative unit
setup data ( it is part of the server's default data ). API support for
editing has still been supplied - as a failsafe mechanism.

Counties
++++++++++
Counties can be listed by visiting ``/api/common/counties/``. Individual county
details can be listed by visiting ``/api/common/counties/<pk>/`` e.g
``/api/common/counties/dd999449-d36b-47f2-a958-1f5bb52951d4/`` for a county
whose ``id`` is ``dd999449-d36b-47f2-a958-1f5bb52951d4``.

.. note::

    The county detail endpoint is atypical.

    It embeds a geographic feature ( GeoJSON ) under the ``county_boundary``
    key and the coordinates of all facilities ( as a map of GeoJSON points )
    in the county under the key ``facility_coordinates``.

    This API provides all the raw information that is needed to render a map
    of the county and plot the facilities on that map.

Constituencies
+++++++++++++++++
Constituencies can be listed by visiting ``/api/common/constituencies/``.
Individual constituency details can be viewed by visiting
``/api/common/constituencies/<pk>/`` e.g
``/api/common/constituencies/16da4d8a-4bff-448b-8fbb-0f64ee82c05a/`` for the
constituency with an ``id`` ``16da4d8a-4bff-448b-8fbb-0f64ee82c05a``.

.. note::

    Like the county detail endpoint, the constituency detail endpoint is
    atypical. It embeds the same coordinates and boundary information.

Wards
++++++++
Wards can be listed by visiting ``/api/common/wards/``. Individual ward details
can be retrieved at ``/api/common/wards/<pk>/`` e.g ``/api/common/wards/41ae635c-5dba-40af-bb74-37d8d0a4c175/`` for the ward with an ``id``
``41ae635c-5dba-40af-bb74-37d8d0a4c175``.

.. note::

    Like the county and constituency detail endpoints, the ward detail
    endpoint is atypical because it embeds coordinates and boundary
    information.

Facility Types
-----------------
The purpose of this resource is to populate dropdowns used in facility creation
and edit screens. The API also supports the creation of an administrative
interface that can be used to add new facility types and retire old ones.

Facility types can be listed at ``/api/facilities/facility_types/``. Individual
facility details can be listed at ``/api/facilities/facility_types/<pk>/`` e.g
``/api/facilities/facility_types/ccf14e50-2606-40b9-96fd-0dc5b3ed4a15/`` for
the facility whose ``id`` is ``ccf14e50-2606-40b9-96fd-0dc5b3ed4a15``.

The only required fields when creating a new facility type are ``name``
( which should be set to something meaningful ) and ``sub_division`` ( which
can be null ). The following is a minimal but valid ``POST`` payload:

.. code-block:: javascript

    {
        "name": "Test facility type for docs",
        "sub_division": null
    }

Facility owners and owner types
-----------------------------------
Facility owner types provide a mechanism by which the owners of facilities
can be classified, arbitrarily. Examples are "Non Governmental Organizations",
"Faith Based Organizations" and the "Ministry of Health". These owner types
can be changed at will.

In the MFL 1 era, facility owners were set up in a very general manner e.g
"Private Enterprise (Institution)" and "Private Practice - Unspecified". There
is no technical reason why these facility owners cannot be more specific e.g
names of specific private sector organizations.

Facility owner types
+++++++++++++++++++++++
Facility owner types can be listed at ``/api/facilities/owner_types/``.
Predictably, the detailed representations will be found at
``7ce5a7b1-9a5e-476c-a01c-8f52c4233926``.

When creating a new facility owner type, the only mandatory field is the
``name``. For example: the following is a perfectly valid ``POST`` payload:

.. code-block:: javascript

    {
        "name": "Owner type for docs"
    }

Facility owners
++++++++++++++++++
Facility owners can be listed at ``/api/facilities/owners/``. Detail
representations can be obtained from ``/api/facilities/owners/<pk>/``
e.g ``/api/facilities/owners/f770a132-f62a-418a-96b4-062c3cc7860c/``.

When registering a new facility owner, the ``POST`` payload should contain
at least the ``name``, ``description`` and ``abbreviation``. For example:

.. code-block:: javascript

    {
        "name": "Imaginary BigCorp.",
        "description": "BigCorp owns everything",
        "abbreviation": "BIG",
    }

.. note::

    The setup of owners and owner types should be performed with care, because
    of the importance of this metadata in analysis / reporting.

Job titles
--------------
The job titles that are available to be assigned to facility officers can be
listed at ``/api/facilities/job_titles/``. Individual job title detail
resources will be at ``/api/facilities/job_titles/<pk>`` e.g
``/api/facilities/job_titles/7ec51365-75b7-45e5-873b-8bb3c97bbe21``.

When creating a new job title, the ``name`` and ``description`` should be sent
as a ``POST`` payload to the list endpoint. The example below is a valid
payload:

.. code-block:: javascript

    {
        "name": "Boss",
        "description": "Big Cahunna"
    }

Regulating bodies
--------------------
The regulators that are known to the server can be listed by ``GET``ting
``/api/facilities/regulating_bodies/``. Predictaby, the detail of each can
be retrieved at ``/api/facilities/regulating_bodies/<pk>/`` e.g
``/api/facilities/regulating_bodies/07f8302f-042a-4a9c-906b-10d69092b43e/``.

When registering a new regulating body, you should set the ``name``,
``abbreviation`` and ``regulation_verb`` fields. For example:

.. code-block:: javascript

    {
        "name": "A newly legislated regulator",
        "abbreviation": "ANLR",
        "regulation_verb": "Gazettment"
    }

Regulating body contacts
++++++++++++++++++++++++++
After creating a regulating body, one or more contacts can be associated with
it by ``POST``ing to ``/api/facilities/regulating_body_contacts/`` the ``id``
of the ``regulating_body`` ( returned by the API after creating the body or
retrieved from the relevant list / detail endpoint ) and the ``id`` of the
``contact`` ( obtained in a similar manner ).

Suppose that the ``id`` for the newly created regulating body is
``5763a053-668e-4ca7-bab4-cda3da396453``. Suppose also that we have just
created a contact with ``id`` ``7dd62ab9-94c2-48d6-a10f-d903bd57acd5``.

We can associate that contact and the regulating body by ``POST``ing to
``/api/facilities/regulating_body_contacts/`` the following payload:

.. code-block:: javascript

    {
        "regulating_body": "5763a053-668e-4ca7-bab4-cda3da396453",
        "contact": "7dd62ab9-94c2-48d6-a10f-d903bd57acd5"
    }

The regulating body contacts that already exist can be listed by issuing a
``GET`` to ``/api/facilities/regulating_body_contacts/``. If you would like to
filter those that belong to a known regulating body, use a ``regulating_body``
query parameter, with the ``id`` of the regulating body as the filter value
e.g ``/api/facilities/regulating_body_contacts/?regulating_body=5763a053-668e-4ca7-bab4-cda3da396453``. You could also filter the regulating body contacts using the ``id`` of a
known contact, although the use cases for that are more limited.

.. note::

    This section introduces some patterns that will recur in this API:

    *   The use of filters: the list APIs are filterably by most of the
        fields that they list. You can explore this further in the sandbox.
    *   The use of **explicit join tables** for many to many relationships.

    The ``regulating_body_contact`` resource that is the subject of this
    section is an example. That is a deliberate choice - we find that, even
    though it makes the API clients do a little more work, it leads to more
    **reliable** APIs. In RESTful APIs, nested serialization / deserialization
    is a massive pain. We'd rather not deal with it.

.. toctree::
    :maxdepth: 2
