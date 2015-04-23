Understanding the API
============================
TBD - **everything here is work in progress**

TODO - API root and metadata

TODO - Plagiarize chomba ( connecting etc )

Explore the API
-----------------
Once all the steps above have been carried out, the system is ready to run and one can explore the API.

There are two ways to explore the API:

**a. Through Swagger**
   This is the recommended way as one can easily try  ``GET``, ``POST``, ``PUT``,  ``PATCH``, ``DELETE`` and ``OPTIONS`` on an endpoint if they are allowed.

   To explore the endpoint throught swagger visit the url ``api/explore/``.

**b. Through accessing the urls directly**
The list of the endpoints availble is located at ``api/common/api_root/``.

Resource Formats Supported
----------------------------
The formats supported are xml, json, csv and xlsx.
The default data format is json. To access xml append ``?format=xml`` to an endpoint. To access data in csv append ``?format=csv`` and similarly to access xlsx append ``?format=xlsx``.

The different resource formats can also be accessed through **HTTP content negotiation**.

For example if there is a resource called user, it can be accessed in the four different formats as shown below:

**To get json**

     curl -i -H "Accept: application/json" -H "Content-Type: application/json" http://localhost:8000/api/user

**To get csv**

     curl -i -H "Accept: application/csv" -H "Content-Type: application/csv" http://localhost:8000/api/user

**To get xml**

    curl -i -H "Accept: application/xml" -H "Content-Type: application/xml" http://localhost:8000/api/user

**To get resource in Microsoft Excel format**

    curl -i -H "Accept: application/xlsx" -H "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" http://localhost:8000/api/user


.. toctree::
    :maxdepth: 2
