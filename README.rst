==========
Master Facility List API
==========
.. image:: https://circleci.com/gh/MasterFacilityList/mfl_api.svg?style=svg
    :target: https://circleci.com/gh/MasterFacilityList/mfl_api

This is the backend for the Master Facility list. 
It provides an api through which one is able to access various resources provided by master facility list; Including facilities and their services.



Getting started
----------------
A: Running the system from source code
-----------------------------------
1. Create a virtualenv

2. Activate the created vitualenv and run ``pip install -r requirements.``

3. Run ``fab setup``
    Running this command will do the following:

    * Create the database.

    * Run migrations.

    * Load demo data if the project is in development mode.

B: Installing the system
-------------------------
1. Create a virtaulenv.
2. Activate the virtualenv and run ``python setup.py install`` while in the project folder.


Once all the steps above have been carried out, the system is ready to run and one can explore the api. 

There are two ways to explore the api:

a. Through ``swagger``. 
   This is the recommended way as one can easily try  ``GET``, ``POST``, ``PUT``,  ``PATCH``, ``DELETE``, ``OPTIONS`` on an endpoint if they are allowed.

   To explore the endpoint throught swagger visit the url ``api/explore/``. 

b. Through accessing the urls directly

Below is a listing of the urls in the project:

**Counties**
``api/common/counties/``

**Constituencies**
``api/common/constituencies``

**Contacts**
``api/common/contacts/``

**Physical address**
``api/common/address/``

**Sub counties**
``api/common/sub_counties/``

**Users**
``api/common/users/``

**Roles**
``api/roles/``

**Permissions**
``api/roles/permissions/``

**Owners**
``api/facitilies/owners/``

**Facitlities**
``api/facilities/``

**Services**
``api/facilities/services/``


Data Formats Supported
----------------------
The formats supported are xml, json, csv and xlsx.
The default data format is json. To access xml append ``?format=xml`` to an endpoint. To access data in csv append ``?format=csv`` and similarly to access xlsx append ``?format=xlsx``. 