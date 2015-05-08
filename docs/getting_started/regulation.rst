MFL APIs: Regulation
=======================
This chapter assumes that the reader is familiar with the general
principles explained in the :doc:`api` chapter

TBD - Adding regulatory bodies
What is a regulaory body?

Creating a regulatory body do a 'POST' to the url. '/api/facilities/regulating_bodies/'
An example payload is as given below
    {
        "name": "Kenya Medical Practitioners Pharmists  and Denstists Board",
        "abbreviation": "KMPPDB",
        "regulation_verb": "license", // e .g gazette /license /register
        "regulatory_body_type": '' // this is the id of the onwer type of facilities they regulate
    }
expected Reponse code
 HTTP 201 CREATED

Updating A Record
To modify a regulatory body record. 
PATCH to the url 
url '/api/facilities/regulating_bodies/<id>'
    {
        "name": "Kenya Medical Practitioners Pharmists  and Denstists Board",
    }
Expected Http Reponse code
HTTP 200 OK
Note in data you put only the field that you want to modify.
 
 Listing Regulatory bodies.
 To get a list of all the regulatory bodies in the system
 Do a GET to the url '/api/facilities/regulating_bodies/'
Here is a sample reponse data from the endpoint
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Kenya Medical Practitioners Pharmacists  and Denstists Board",
            "abbreviation": "KMPPDB",
            "regulation_verb": "license", // e .g gazette /license /register
            "regulatory_body_type": '' // this is the id of the onwer type of facilities they regulate
        },
            "name": "Nursing Council of Kenya",
            "abbreviation": "NCK",
            "regulation_verb": "license", // e .g gazette /license /register
            "regulatory_body_type": '' // this is the id of the onwer type of facilities they regulate
        }
    ]
} 

Like any other list endpoint one can access the same resource in xml, get an excel file or even get a csv file.


Once the regulatory bodies have been added, the next step is to configure regulation states.
The endppoint where this is done is 'api/facilities/regulation_status/'
A regulation states is a state in which the facility will be after the regulator has assess its suitability for that state.
The default states are as provided in the implemetation guide. PENDING_LICENSING, LINCESED, LICENSE_SUSPENDED, LINCENSE_CANCELLED, PENDING_REGISTRATION, REGISTERED, PENDING_GAZETTEMENT, GAZETTED
to list all the available regulation statuses do a GET to the url 'api/facilities/regulation_status/' this give sample payload as shown below:
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

Creating a regulation status
Creating a regulation status requires one to know the entire workflow from the first state to the last state.
This is so since as one creates a state one has to know whether it is an initial state or a final state and if the state 
is an intermediary state, then which are the preceeding and succeeding states.
This section will be devided into 3 parts.
    1. Creating an initial state
To create the very first regulation state do a post to the url with the payload as shown below:
    {
        "name": "PENDING_LICENSING",
        "description": "This is the very first state after a facility has been approved by the CHRIO",
        "is_initial_state": true,
     
    }
Expected reponse code.
    HTTP 201 CREATED

To create a final state is very similar to creating an initial state.
The url to POST to is still '/api/facilities/regulation_status/'
The only change will be to subtitute the is_initial_state with is_final_state and add a pBelow is a sample payload.
    {
        "name": "LICENSED",
        "description": "This is the final state after a  facility has been given a license by the regulating body",
        "is_final_state": true,
        'previous_state': "1938861f-2c34-49c5-808f-caa0ed1c3681" // id of the preceding state
     
    }
expected reponse code:
    HTTP 201 CREATED

To create an intermediate state.
AN intermediate should have a preceeding and succeeding state. 
Here is an example
POST to the url 
    {
        "name": "INTERMEDIARY_STATE",
        "description": "This is the state inbetween state 1 and state 3",
        "previous_status": "1938861f-2c34-49c5-808f-caa0ed1c3681" // id of the preceding state ,
        "next_status": "1938861f-2c34-49c5-808f-caa0ed1c3681" // id of the suceeding state
    }
Expected response
    HTTP 201 CREATED


Once the regulatory bodies and regulation statuses have been set. the regulator is one set to start regulating facilities.

1. getting a list of all facilities that need to be regulated.
    Do get to the url '/api/facilities/facility_regulation_status/'
    this will give a list of the facilities that have been modified and need to be regulated or the facilties that have been not yet been regulated.
    The response data will be similar to the sample respnse data below:
    {
        "count": 0,
        "next": null,
        "previous": null,
        "results": []
    }

to update the regulatory details of a facility.
Do a post to  the url with data payload similar to the payload shown below:
    {
        "created": null,
        "updated": null,
        "deleted": false,
        "active": false,
        "reason": "",
        "license_number": "",
        "is_confirmed": false,
        "is_cancelled": false,
        "created_by": null,
        "updated_by": null,
        "facility": null,
        "regulating_body": null,
        "regulation_status": null
    }


.. toctree::
    :maxdepth: 2
