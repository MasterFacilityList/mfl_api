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
        "regulatory_body_type": "d195219b-7b5b-4395-889b-3dbcb7bfccf6" // this is the id of the onwer type of facilities they regulate
    }

Expected Response code
    HTTP 201 CREATED

sample response data

.. code-block:: javascript

    {
        "id": "fbb96308-454f-4d1d-9ca4-597018d460b7",
        "created": "2015-05-08T16:24:09.552222Z",
        "updated": "2015-05-08T16:24:09.552245Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "Kenya Medical Practitioners Pharmacists  and Dentists Board",
        "abbreviation": "KMPPDB",
        "regulation_verb": "license",
        "created_by": 3,
        "updated_by": 3,
        "regulatory_body_type": null,
        "contacts": []
    }

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


Sample response data

.. code-block:: JavaScript

    {
        "id": "fbb96308-454f-4d1d-9ca4-597018d460b7",
        "created": "2015-05-08T16:24:09.552222Z",
        "updated": "2015-05-08T16:24:09.552245Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "Kenya Medical Practitioners Pharmacists  and Dentists Board edited",
        "abbreviation": "KMPPDB",
        "regulation_verb": "license",
        "created_by": 3,
        "updated_by": 3,
        "regulatory_body_type": null,
        "contacts": []
    }

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
                    "id": "bdc6d243-af73-438f-be01-224f621bf538",
                    "created": "2015-05-08T15:58:18.351751Z",
                    "updated": "2015-05-08T15:58:18.351772Z",
                    "deleted": false,
                    "active": true,
                    "search": null,
                    "name": "Pharmacy & Poisons Board",
                    "abbreviation": "Pharmacy & Poisons Board",
                    "regulation_verb": "Licensing",
                    "created_by": 1,
                    "updated_by": 1,
                    "regulatory_body_type": null,
                    "contacts": []
                },
                {
                    "id": "5a797ac9-dbbb-4579-b2c3-dee80c2ae43b",
                    "created": "2015-05-08T15:58:18.346141Z",
                    "updated": "2015-05-08T15:58:18.346164Z",
                    "deleted": false,
                    "active": true,
                    "search": null,
                    "name": "Clinical Officers Council",
                    "abbreviation": "COC",
                    "regulation_verb": "Licensing",
                    "created_by": 1,
                    "updated_by": 1,
                    "regulatory_body_type": null,
                    "contacts": []
                }
        ]

}


Retrieving
----------------
To retrieve a single regulatory body do a ``GET`` to the url ``api/facilities/regulating_bodies/<id>/``
Id being the id of the regulatory body. The response data will be similar to the data shown below:

.. code-block:: javascript

    {
        "id": "bdc6d243-af73-438f-be01-224f621bf538",
        "created": "2015-05-08T15:58:18.351751Z",
        "updated": "2015-05-08T15:58:18.351772Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "Pharmacy & Poisons Board",
        "abbreviation": "Pharmacy & Poisons Board",
        "regulation_verb": "Licensing",
        "created_by": 1,
        "updated_by": 1,
        "regulatory_body_type": null,
        "contacts": []
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

Sample Response data

.. code-block:: javascript

    {
        "id": "698e1e45-0ab7-466f-a449-9091036cfa31",
        "next_state_name": "Pending Licensing",
        "previous_state_name": "Pending Licensing",
        "created": "2015-05-08T16:17:32.016528Z",
        "updated": "2015-05-08T16:17:32.016543Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "PENDING_LICENSING",
        "description": "This is the very first state after a facility has been approved by the CHRIO",
        "is_initial_state": false,
        "is_final_state": true,
        "created_by": 3,
        "updated_by": 3,
        "previous_status": "1938861f-2c34-49c5-808f-caa0ed1c3681",
        "next_status": "1938861f-2c34-49c5-808f-caa0ed1c3681"
    }


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

Sample Response data

.. code-block:: javascript

    {
        "id": "698e1e45-0ab7-466f-a449-9091036cfa31",
        "next_state_name": "Pending Licensing",
        "previous_state_name": "Pending Licensing",
        "created": "2015-05-08T16:17:32.016528Z",
        "updated": "2015-05-08T16:17:32.016543Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "LICENSED",
        "description": "This is the final state after a  facility has been given a license by the regulating body",
        "is_initial_state": false,
        "is_final_state": true,
        "created_by": 3,
        "updated_by": 3,
        "previous_status": "1938861f-2c34-49c5-808f-caa0ed1c3681",
        "next_status": "1938861f-2c34-49c5-808f-caa0ed1c3681"
    }

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

sample Reponse data

.. code-block:: javascript

    {
        "id": "698e1e45-0ab7-466f-a449-9091036cfa31",
        "next_state_name": "Pending Licensing",
        "previous_state_name": "Pending Licensing",
        "created": "2015-05-08T16:17:32.016528Z",
        "updated": "2015-05-08T16:17:32.016543Z",
        "deleted": false,
        "active": true,
        "search": null,
        "name": "INTERMEDIARY_STATE",
        "description": "This is the state in-between state 1 and state 3",
        "is_initial_state": false,
        "is_final_state": false,
        "created_by": 3,
        "updated_by": 3,
        "previous_status": "1938861f-2c34-49c5-808f-caa0ed1c3681",
        "next_status": "1938861f-2c34-49c5-808f-caa0ed1c3681"
    }



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
        
        "name": "Registered Edited"
    }

The above payload will update the details of the state whose id is the url.

Expected Response code:
    HTTP 200 OK


Sample Response data

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
        "name": "Registered Edited",
        "description": null,
        "is_initial_state": false,
        "is_final_state": false,
        "created_by": 1,
        "updated_by": 1,
        "previous_status": "1390d5c3-9226-44a0-b464-13d17fed2b41",
        "next_status": null
    }


Listing Facilities pending regulation
--------------------------------------

Do a ``GET`` to the url ``/api/facilities/facility_regulation_status/?regulated=False``
This will respond with a list of the facilities that have been modified and need to be regulated or the facilities that have been not yet been regulated.
The response data will be similar to the sample response data below:

.. code-block:: javascript

    {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
            {
                "id": "8c0964a1-b733-40e4-b0be-1874749e469b",
                "regulary_status_name": null,
                "facility_type_name": "District Hospital",
                "owner_name": "Ministry of Health",
                "owner_type_name": "Ministry of Health",
                "county": "TRANS NZOIA",
                "constituency": "ENDEBESS",
                "created": "2015-05-08T09:58:36.862227Z",
                "updated": "2015-05-08T09:58:36.862242Z",
                "deleted": false,
                "active": true,
                "search": null,
                "name": "Endebess District Hospital",
                "code": 14455,
                "abbreviation": "",
                "description": "",
                "location_desc": "Kitale Swam Road",
                "number_of_beds": 20,
                "number_of_cots": 8,
                "open_whole_day": true,
                "open_whole_week": true,
                "is_classified": false,
                "is_published": true,
                "is_synchronized": false,
                "created_by": 1,
                "updated_by": 1,
                "facility_type": "1d2e7d02-97e0-470b-9889-549df3ff49f8",
                "operation_status": "e865f01b-8937-40fc-a095-fbbb83c59461",
                "ward": "a4223139-30e4-4253-88fe-405a622aa2f7",
                "owner": "7506421d-7838-4eee-9a44-7c92fd76d0b9",
                "officer_in_charge": null,
                "physical_address": "3c75fb20-619d-4591-8f93-56f7493ee764",
                "parent": null,
                "contacts": []
            },
            {
                "id": "854bb94d-7a87-45c7-9243-4b9d9751a690",
                "regulary_status_name": null,
                "facility_type_name": "Health Centre",
                "owner_name": "Ministry of Health",
                "owner_type_name": "Ministry of Health",
                "county": "TRANS NZOIA",
                "constituency": "ENDEBESS",
                "created": "2015-05-08T09:58:36.849294Z",
                "updated": "2015-05-08T09:58:36.849311Z",
                "deleted": false,
                "active": true,
                "search": null,
                "name": "Kwanza Health Centre",
                "code": 15003,
                "abbreviation": "",
                "description": "",
                "location_desc": "",
                "number_of_beds": 18,
                "number_of_cots": 0,
                "open_whole_day": false,
                "open_whole_week": true,
                "is_classified": false,
                "is_published": true,
                "is_synchronized": false,
                "created_by": 1,
                "updated_by": 1,
                "facility_type": "3c8a65ec-8489-4483-b32b-057098a9fe08",
                "operation_status": "e865f01b-8937-40fc-a095-fbbb83c59461",
                "ward": "4e203a27-8c37-468e-8b39-407193a6d862",
                "owner": "7506421d-7838-4eee-9a44-7c92fd76d0b9",
                "officer_in_charge": null,
                "physical_address": "3c75fb20-619d-4591-8f93-56f7493ee764",
                "parent": null,
                "contacts": []
            }
        ]
    }
 

Regulate a facility
---------------------
``POST``  to ``/api/facilities/facility_regulation_status/`` a payload similar to the one shown below:

.. code-block:: javascript

    {
    
        "reason": "The facility has met all the requirements",
        "license_number": "F135/2015",
        "facility": "d0cf7632-2854-464f-8638-03d1c021f519",
        "regulating_body": "ed3ac8af-c1a7-42f4-9f0d-a9c5e4cf3c13",
        "regulation_status": "5287dbfc-e2c0-410f-80e3-7ec20ac4dc79"
    }

Expected Reponse Code
    HTTP 201 Created

Sample Reponse data

.. code-block:: javascript

    {
        "id": "594f7bd1-ce6b-4a6d-82c2-523b1710ec31",
        "created": "2015-05-08T16:10:22.604609Z",
        "updated": "2015-05-08T16:10:22.604631Z",
        "deleted": false,
        "active": true,
        "search": null,
        "reason": "The facility has met all the requirements",
        "license_number": "F135/2015",
        "is_confirmed": false,
        "is_cancelled": false,
        "created_by": 3,
        "updated_by": 3,
        "facility": "d0cf7632-2854-464f-8638-03d1c021f519",
        "regulating_body": "ed3ac8af-c1a7-42f4-9f0d-a9c5e4cf3c13",
        "regulation_status": "5287dbfc-e2c0-410f-80e3-7ec20ac4dc79"
    }   


.. toctree::
    :maxdepth: 2
