MFL APIs: Shared Resources and properties
===========================================
.. include:: ../substitutes.txt

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
TBD

Facility owners and owner types
-----------------------------------
Facility owners
++++++++++++++++++
TBD

Facility owner types
+++++++++++++++++++++++
TBD

TBD - comment about analytics impact of all this
TBD - comment about a potential move to full detail

Job titles
--------------
TBD

Regulating bodies
--------------------
TBD

Regulating body contacts
++++++++++++++++++++++++++
TBD


.. toctree::
    :maxdepth: 2
