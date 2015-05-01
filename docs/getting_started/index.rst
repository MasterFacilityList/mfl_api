Getting started
=================
The MFL v2 project subscribes to the `API First`_ approach. It is **built to
interoperate**. We "eat our own dog food" by insisting that the official
user interfaces be just one more set of API clients, with no special
privileges.

This guide is for the authors of client applications ( applications that
consume the RESTful web services ).

Those who would like to make changes to the MFL API server code itself
should refer to the :doc:`../contributing/index` guide.

.. _`API First`: http://www.api-first.com/

RESTful or not
----------------
Its "RESTish". We subscribe to the principles of `REST`_ but are not
pedantic about it. It is built using the excellent `Django REST Framework`_.

.. _`REST`: http://en.wikipedia.org/wiki/Representational_state_transfer
.. _`Django REST Framework`: http://www.django-rest-framework.org/

You can find more information about the API and its philosophy at
:doc:`api`.

Authentication
-----------------
A system like this has to consider the needs of programmatic clients
( like integrations into other systems ) and the needs of "actual users"
( in this case people logged in to the web interfaces ).

We chose to use OAuth 2.0 to implement our authentication mechanisms
for both. You can find more information at the excellent `rfc6749`_ and
at our :doc:`authentication` page.

.. _`rfc6749`: https://tools.ietf.org/html/rfc6749

Sandbox
----------
Our experience teaches us that the biggest roadblock to systems integration
is usually communication. Developers operate at a level of precision and
detail that is alien to most people. We've been spoilt by our past dabblings
with high quality API documentation sites like the `Stripe API site`_.

That inspired us to build the MFL API -  :doc:`sandbox`.

.. _`Stripe API site`: https://stripe.com/docs/api

.. toctree::
    :maxdepth: 2

    sandbox
    the_big_picture
    authentication
    api
    support_resources
    services
    facilities
    community_health_units
    regulation

