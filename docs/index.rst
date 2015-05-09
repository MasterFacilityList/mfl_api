Master Facility List API server documentation
===============================================

This is documentation for the API server for the second generation Kenyan Ministry of Health Master Facility List ( MFL ).

The MFL system's "home" is at http://ehealth.or.ke/facilities/ .

This documentation is aimed at developers ( both MFL developers and those developing third party systems that use the MFL API ) and system administrators.

There is a `downloadable PDF version`_ of this documentation, a
`mobile friendly EPUB version`_ and a `downloadable HTML version`_.

.. _`downloadable PDF version`: https://media.readthedocs.org/pdf/mfl-api/latest/mfl-api.pdf
.. _`mobile friendly EPUB version`: http://readthedocs.org/projects/mfl-api/downloads/epub/latest/
.. _`downloadable HTML version`: http://readthedocs.org/projects/mfl-api/downloads/htmlzip/latest/

Installing
==============
There are three different installation scenarios, depending on the goal
of the person installing.

Installing for evaluation
---------------------------
In this scenario, you do not plan to make any changes to the MFL API server
but you need to have a local copy against which you can test a new API
client or a new third party integration.

We recommend that you use `Vagrant`_ and `Virtualbox`_ to create a test
server for yourself.

.. _Vagrant: https://www.vagrantup.com/
.. _Virtualbox: https://www.virtualbox.org/

You can find more information at :doc:`evaluator_install`. If you are an
expert Vagrant user, you can substitute Virtualbox with VMWare
Desktop / Player, HyperV etc. You'll have an easier time if you are on a
``_nix`` e.g Ubuntu or OS X.

Installing on a production server
-----------------------------------
This server has been developed and tested on `Ubuntu`_ Linux ( any Ubuntu
that is currently "in support" will do ). It should be *trivial* to get it
working on any ``*NIX`` ( including OS X ). It is *possible* to get it
running on Windows, but we have not put any work into it. If you've got a
burning desire to see the server running on Windows, you are encouraged to
test it there and issue pull requests for any fixes that would be needed.

Kindly note that this restriction applies to the servers only, and not to
any of the API clients e.g browsers and third party systems. Clients can
run on any modern operating system.

You can find more information at :doc:`production_install`. We supply an
`Ansible`_ playbook that automates this entire process.

.. _Ansible: http://www.ansible.com/home
.. _Ubuntu: http://www.ubuntu.com/

Installing on a developer's computer
--------------------------------------
You'll have an easier time if you are on a current Ubuntu. On Ubuntu, the
key dependencies can be installed with:

::

    sudo apt-get install postgresql binutils postgis gdal-bin libproj-dev
    libgeoip1 graphviz libgraphviz-dev

**You may need to install distribution specific packages** e.g on Ubuntu 14.04
with the default PosgreSQL 9.3:

::

    sudo apt-get install postgresql-9.3-postgis-2.1

In order to build some of the Python dependencies in the `virtualenv`, some
libraries will need to be in place. Again, if you are on a recent Ubuntu, you
can get them at once with:

::

    sudo apt-get build-dep python-shapely python-numpy cython python-psycopg2

You can find more information at :doc:`developer_install`.

.. _virtualenv: https://virtualenv.pypa.io/en/latest/

Using the API
=================
The MFL v2 project subscribes to the `API First`_ approach. It is **built to
interoperate**. We "eat our own dog food" by insisting that the official
user interfaces be just one more set of API clients, with no special
privileges.

This guide is for the authors of client applications ( applications that
consume the RESTful web services ).

Those who would like to make changes to the MFL API server code itself
should refer to the :doc:`workflow` guide.

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

Contributing
==============
MFL API v2 is a liberally licensed ( `MIT`_ license ) project. All development
occurs in the open on the `MFL API Github project`_. We use the
`MFL API Github issue list`_ to manage bug reports and enhancement requests.

.. _`MIT`: http://choosealicense.com/licenses/mit/
.. _`MFL API Github project`: https://github.com/MasterFacilityList/mfl_api
.. _`MFL API Github issue list`: https://github.com/MasterFacilityList/mfl_api/issues

Workflow
-------------
This project uses the ``git-flow`` workflow. You can learn more about it
from https://github.com/nvie/gitflow .

You can find more information at our :doc:`workflow` page.

Code of conduct
-----------------
We have an open-door policy when it comes to contributions. However - we
expect all participants in the MFL project to be respectful and considerate.

You can find more information at our :doc:`code_of_conduct` page.

Contents
===========

.. toctree::
    :maxdepth: 3

    evaluator_install
    developer_install
    production_install
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
    workflow
    code_of_conduct

.. include:: ../CHANGELOG.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
