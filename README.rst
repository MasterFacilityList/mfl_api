==========
Master Facility List API
==========
.. image:: https://circleci.com/gh/MasterFacilityList/mfl_api.svg?style=shield
    :target: https://circleci.com/gh/MasterFacilityList/mfl_api

This is the backend for the Master Facility list. 
It provides an api through which one is able to access various resources provided by master facility list; Including facilities and their services.

Read more at http://ehealth.or.ke/facilities/

Getting started
----------------
**A: Running the system from source code**

1. Create a virtualenv

2. Activate the created vitualenv and run ``pip install -r requirements.``

3. Run ``fab setup``
    Running this command will do the following:

    * Create the database.

    * Run migrations.

    * Load demo data if the project DEBUG is set to true in settings.

**B: Installing the system**


2. Activate the virtualenv and run ``python setup.py install`` while in the project folder.

Explore the API
---------------
Once all the steps above have been carried out, the system is ready to run and one can explore the API. 

There are two ways to explore the API:

**a. Through Swagger**
   This is the recommended way as one can easily try  ``GET``, ``POST``, ``PUT``,  ``PATCH``, ``DELETE`` and ``OPTIONS`` on an endpoint if they are allowed.

   To explore the endpoint throught swagger visit the url ``api/explore/``. 

**b. Through accessing the urls directly**
The list of the endpoints availble is located at ``api/common/api_root/``.

Data Formats Supported
----------------------
The formats supported are xml, json, csv and xlsx.
The default data format is json. To access xml append ``?format=xml`` to an endpoint. To access data in csv append ``?format=csv`` and similarly to access xlsx append ``?format=xlsx``. 
The different data formats can also be accessed through content negotiation.
    to access csv
    to access xml
    to access xlsx

Authentication 
TODO

Running tests
------------
TODO