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

MFL 2: The Big Picture
------------------------
The Master Facilities List is one of the building blocks of the Kenyan
national health information system. You can read more about its role
at :doc:`the_big_picture`.

Using the API: Basic Principles
----------------------------------
Its "RESTish". We subscribe to the principles of `REST`_ but are not
pedantic about it. It is built using the excellent `Django REST Framework`_.

.. _`REST`: http://en.wikipedia.org/wiki/Representational_state_transfer
.. _`Django REST Framework`: http://www.django-rest-framework.org/

You can find more information about the API and its philosophy at
:doc:`api`.

Authentication and Authorization
----------------------------------
A system like this has to consider the needs of programmatic clients
( like integrations into other systems ) and the needs of "actual users"
( in this case people logged in to the web interfaces ).

We chose to use OAuth 2.0 to implement our authentication mechanisms
for both. You can find more information at the excellent `rfc6749`_ and
at our :doc:`authentication` page.

.. _`rfc6749`: https://tools.ietf.org/html/rfc6749

The API Sandbox
------------------
Our experience teaches us that the biggest roadblock to systems integration
is usually communication. Developers operate at a level of precision and
detail that is alien to most people. We've been spoilt by our past dabblings
with high quality API documentation sites like the `Stripe API site`_.

That inspired us to build for the MFL API :doc:`sandbox`.

.. _`Stripe API site`: https://stripe.com/docs/api

MFL APIs: Shared Resources and properties
-----------------------------------------------------
The MFL's job description is to standardize the management of information
relating to facilities ( including community health units ), provide a standard
catalogue of available healthcare services and act as a central ingress
point for regulation.

However, in order to do this, the MFL needs to have a constellation of
support resources in its data model. The :doc:`support_resources` page
documents this part of the data model.

MFL APIs: The Service Catalogue
-------------------------------------------
In order for the MFL to do its job as the keystone of the Kenyan national
health information system, there needs to be a standard registry of
healthcare services.

At the time when this edition of the MFL was built, no such thing existed.
The MFL therefore took on the responsibility of providing that registry.
For more information, see :doc:`services`.

MFL APIs: Facilities
--------------------------------
The MFL is not merely a "list" of facilities; it has rich APIs to manage their
life cycles and to support interaction with other healthcare systems. You can
read more about that at :doc:`facilities`.

MFL APIs: Community Health Units
--------------------------------------------
Kenya's community health strategy relies on community health workers for
outreach at the lowest levels ( embedded into communities ). These workers are
organized into community health units. The second edition of the Master
Facilities List provides APIs for the management of community health units.
You can read more at :doc:`community_health_units`.

MFL APIs: Regulation
----------------------------------
Every healthcare facility falls under the regulatory scope of at least one
regulator. For example - at the time of writing, most healthcare facilities
are licensed by the Kenya Medical Practitioners and Dentists Board.

Regulators have their own information systems. The MFL provides APIs that can
facilitate two way data flow between the regulators' systems and the Master
Facilities List. You can read more at :doc:`regulation`.

MFL APIs: GIS Support
------------------------
The MFL 2 API server uses the excellent `GeoDjango`_ and `PostGIS`_ to provide
services that can be used to generate facility maps, perform geographic
queries and validate facility coordinate data. You can read more about this at
the :doc:`gis` page.

.. _`GeoDjango`: https://docs.djangoproject.com/en/dev/ref/contrib/gis/
.. _`PostGIS`: http://postgis.net/

.. toctree::
    :maxdepth: 3

    the_big_picture
    api
    authentication
    sandbox
    support_resources
    services
    facilities
    community_health_units
    regulation
    gis

