MFL APIs: Shared Resources and properties
===========================================
.. include:: ../substitutes.txt

TBD - support resources
TBD - audit support

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


Common Filters
-------------------
TBD - Document filters found in every resource
TBD - examples for GET, POST, PUT, PATCH, DELETE ( could be elsewhere )

.. toctree::
    :maxdepth: 3
