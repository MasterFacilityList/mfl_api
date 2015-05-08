MFL APIs: Regulation
=======================
This chapter assumes that the reader is familiar with the general
principles explained in the :doc:`api` chapter

For regulation of facilities to occur in the system two entities are required:
    1. The regulating body
    2. The regulation status


Regulatory Bodies
------------------
These are the bodies that are in-charge of assessing whether a facility should be licensed, gazetted or registered.
They also determine the KEPH level of operation of a facility.


Creation
----------
`POST` to `/api/facilities/regulating_bodies/` a payload  similar  to the one shown below:

.. code-block:: javascript

    {
        "name": "Kenya Medical Practitioners Pharmacists  and Dentists Board",
        "abbreviation": "KMPPDB",
        "regulation_verb": "license", // e .g gazette license register
        "regulatory_body_type": 'd195219b-7b5b-4395-889b-3dbcb7bfccf6' // this is the id of the onwer type of facilities they regulate
    }

Expected Response code
    HTTP 201 CREATED


Updating
-----------
``PATCH``  ``/api/facilities/regulating_bodies/<id>`` with payload containing only the fields that are to be modified.
For example

.. code-block:: JavaScript

    {
        "name": "Kenya Medical Practitioners Pharmacists  and Dentists Board"
    }

Expected HTTP Response code
    HTTP 200 OK


Listing
---------
Do a ``GET`` the ``/api/facilities/regulating_bodies/``

Below is a sample response data from the endpoint:

    .. code-block:: JavaScript

        {
            "count": 2,
            "next": null,
            "previous": null,
            "results": [
                {
                    "name": "Kenya Medical Practitioners Pharmacists  and Dentists Board",
                    "abbreviation": "KMPPDB",
                    "regulation_verb": "license", // e .g gazette /license /register
                    "regulatory_body_type": '' // this is the id of the owner type of facilities they regulate
                },
                    "name": "Nursing Council of Kenya",
                    "abbreviation": "NCK",
                    "regulation_verb": "license", // e .g gazette /license /register
                    "regulatory_body_type": '' // this is the id of the owner type of facilities they regulate
                }
            ]
        } 

Retrieving
----------------
To retrieve a single regulatory body do a ``GET`` to the url ``api/facilities/regulating_bodies/<id>/``
Id being the id of the regulatory body. The response data will be similar to the data shown below:

.. code-block:: javascript

    {
        
    }

Regulatory Statuses
---------------------
A regulation state is a state in which the facility will be after the regulator has assessed a facility's suitability for that state.

The default states are as provided in the implementation guide. 
    1. PENDING_LICENSING
    2. LICENSED
    3. LICENSE_SUSPENDED 
    4. LICENSE_CANCELLED
    5. PENDING_REGISTRATION
    6. REGISTERED
    7. PENDING_GAZETTEMENT
    8. GAZETTED


Listing
--------
Do a ``GET`` to the url ``api/facilities/regulation_status/``
Example response

.. code-block:: javascript

    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "d195219b-7b5b-4395-889b-3dbcb7bfccf6",
                "next_state_name": "",
                "previous_state_name": "Pending Registration",
                "created": "2015-05-08T10:00:48.608555Z",
                "updated": "2015-05-08T10:00:48.608572Z",
                "deleted": false,
                "active": true,
                "search": null,
                "name": "Registered",
                "description": null,
                "is_initial_state": false,
                "is_final_state": false,
                "created_by": 1,
                "updated_by": 1,
                "previous_status": "1390d5c3-9226-44a0-b464-13d17fed2b41",
                "next_status": null
            },
            {
                "id": "5287dbfc-e2c0-410f-80e3-7ec20ac4dc79",
                "next_state_name": "",
                "previous_state_name": "Pending Gazettment",
                "created": "2015-05-08T10:00:48.601773Z",
                "updated": "2015-05-08T10:00:48.601808Z",
                "deleted": false,
                "active": true,
                "search": null,
                "name": "Gazettment",
                "description": null,
                "is_initial_state": false,
                "is_final_state": true,
                "created_by": 1,
                "updated_by": 1,
                "previous_status": "06d215ec-4a8c-469f-88df-028e597a348d",
                "next_status": null
            }
        ]
    }

Creation
----------
Creating a regulation status requires one to know the entire regulation workflow of a facility from the first state to the last state.
This is so since as one configures a state they have to know whether it is the initial state, the final state or an intermediary state.

This section will be divided into 3 parts.


1. Creating an initial state
---------------------------------

To create the very first regulation state. To create it do a ``POST`` to the ``api/facilities/regulation_status/`` with the similar to the one shown below.

.. code-block:: javascript

    {
        "name": "PENDING_LICENSING",
        "description": "This is the very first state after a facility has been approved by the CHRIO",
        "is_initial_state": true,
     
    }

Expected response code.
    HTTP 201 CREATED


2. Creating a final State
---------------------------

Creating a  final state is very similar to creating an initial state.

``POST`` to  ``/api/facilities/regulation_status/``
The only change will be to substitute the is_initial_state with is_final_state and add a previous_state to the sample payload.

.. code-block:: javascript

    {
        "name": "LICENSED",
        "description": "This is the final state after a  facility has been given a license by the regulating body",
        "is_final_state": true,
        'previous_state': "1938861f-2c34-49c5-808f-caa0ed1c3681" // id of the preceding state     
    }

Expected response code:
    HTTP 201 CREATED


3. Creating an intermediary State.
------------------------------------

An intermediary should have a preceding and succeeding state. 
Here is an example:

``POST`` to  ``/api/facilities/regulation_status/``

.. code-block:: javascript

    {
        "name": "INTERMEDIARY_STATE",
        "description": "This is the state in-between state 1 and state 3",
        "previous_status": "1938861f-2c34-49c5-808f-caa0ed1c3681" // id of the preceding state ,
        "next_status": "1938861f-2c34-49c5-808f-caa0ed1c3681" // id of the suceeding state
    }

Expected response
    HTTP 201 CREATED


Retrieving a single regulatory state
------------------------------------
Do a ``GET`` to the url ``/api/facilities/regulation_status/<id>`` where id is the id of the regulatory state.

.. code-block:: javascript

    {
        "id": "d195219b-7b5b-4395-889b-3dbcb7bfccf6",
        "next_state_name": "",
        "previous_state_name": "Pending Registration",
        "created": "2015-05-08T10:00:48.608555Z",
        "updated": "2015-05-08T10:00:48.608572Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "Registered",
        "description": null,
        "is_initial_state": false,
        "is_final_state": false,
        "created_by": 1,
        "updated_by": 1,
        "previous_status": "1390d5c3-9226-44a0-b464-13d17fed2b41",
        "next_status": null
    }


Expected Response 
    HTTP 200 OK


Updating a regulatory state
----------------------------------
Do a ``PATCH`` to ``/api/facilities/regulation_status/<id>/`` with the payload being the fields to update.
Here is a sample payload

.. code-block:: javascript

    {
        
        "name": "Registered Edited",
        "description": "The first state of the regulation",
    }

The above payload will update the details of the state whose id is the url.

Expected Response code:
    HTTP 200 OK


Listing Facilities pending regulation
--------------------------------------

Do a ``GET`` to the url ``/api/facilities/facility_regulation_status/?regulated=false``
This will respond with a list of the facilities that have been modified and need to be regulated or the facilities that have been not yet been regulated.
The response data will be similar to the sample response data below:

.. code-block:: javascript

    {
        "count": 0,
        "next": null,
        "previous": null,
        "results": [
        ]
    }
 

Regulate a facility
---------------------
``POST``  to ``/api/facilities/facility_regulation_status/`` a payload similar to the one shown below:

.. code-block:: javascript

    {
        "reason": "The facility has been closed due to being dirty",
        "license_number": "352/28K", // license number as give by the regulatory body
        "facility": 8c0964a1-b733-40e4-b0be-1874749e469b, // id of the facility
        "regulating_body": 8c0964a1-b733-40e4-b0be-1874749e469b, //id of the regulating body
        "regulation_status": 8c0964a1-b733-40e4-b0be-1874749e469b //id of the regulation state
    }



.. toctree::
    :maxdepth: 2
