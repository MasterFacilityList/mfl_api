The API sandbox
============================
Our experience teaches us that the biggest roadblock to systems integration
is usually communication. Developers operate at a level of precision and
detail that is alien to most people. We've been spoilt by our past dabblings
with high quality API documentation sites like the `Stripe API site`_.

.. _`Stripe API site`: https://stripe.com/docs/api

Swagger
--------
The API is interactively browsable through Swagger from the link ``/api/explore``

The Browsable API
--------------
The  API is accesible from the URL ``/api``. This is the entry point into the 
entire list of all the URLS in the API and the methods and that are allowed on an 
endpoint.

API Metadata support
--------------------
The ``api`` URL has been designed to make it easy for a client accessing an endpoint 
to know the methods that are allowed on the endpoint. The metadata support also allows
a client to know the fields that an endpoint accepts and whether they are required or
not.

.. toctree::
    :maxdepth: 2
