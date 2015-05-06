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
TBD

Administrative units
------------------------
TBD - diagram and brief explanation

Counties
++++++++++
TBD

County Boundaries
~~~~~~~~~~~~~~~~~~~~
TBD


Constituencies
+++++++++++++++++
TBD

Constituency Boundaries
~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Wards
++++++++
TBD

Ward Boundaries
~~~~~~~~~~~~~~~~~~
TBD

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
