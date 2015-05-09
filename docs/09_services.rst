MFL APIs: The Service Catalogue
=========================================
This chapter assumes that the reader is familiar with the general
principles explained in the :doc:`06_api` chapter.

This chapter concerns itself with the setup of the **service catalog**.
The service catalog has two primary goals:

 * to model healthcare services in a manner that is flexible and future proof
 * to standardize service codes

.. note::

    Standardization of service codes is a pre-requisite for interoperability
    between the MFL and other systems.

.. note::

    The flexibility will allow the MFL to keep pace with changes in healthcare
    and policy.

Service Categories
---------------------
Service categories are the "broad headings" under which healthcare services are
classified. An example is "Comprehensive Emergency Obstetric Care (CEOC)", an
umbrella for services that respond to life-threatening emergency complications
and are offered by facilities whose human resources include doctors and whose
infrastructure includes operating theatres and incubators.

Existing service categories can be listed by issuing a ``GET`` to
``/api/facilities/service_categories/``.

To add a new service category, ``POST`` to the same URL a payload similar to
this:

.. code-block:: javascript

    {
        "name": "A new service category",
        "description": "What is it really about",
        "abbreviation": "ABBR"
    }

Services
-----------
Services are the granular "product" delivered to end users. Some examples are
"Provider Initiated Counselling and Testing" and Oral Health Services (Dental Services)".

Existing services can be listed at ``/api/facilities/services/``.

When creating a new service, ``POST`` the ``name``, ``description``,
``abbreviation`` and ``category``. For example:

.. code-block:: javascript

    {
        "name": "A new service",
        "description": "The best new service since bread slicing",
        "abbreviation": "ANS",
        "category": "2bdfd814-5cba-4673-916e-96b6a98cf1c9"
    }

.. note::

    Services get auto-assigned ``code`` s. A service code is immutable once
    issued. The service codes are expected to become a standard identifier for
    services.

Options and service options
-----------------------------
In order to understand the options API, we'll take a look at the Facility
Creation Form from the 2010 Master Facility List Implementation Guide
( the guiding document for the previous edition of the MFL ).

.. figure:: /_images/new_facility_form.png
    :scale: 50%
    :alt: New Facility Addition Form (from the MFL Implementation Guide, 2010)

In the form above, many services have ``Yes`` and ``No`` options. Some services
require a numeric level ( levels ``1`` to ``6`` from the Kenya Essential
Package for Health [ KEPH ] ), while obstetric services are classified into
``Basic`` or ``Comp`` ( comprehensive ).

That form is far from comprehensive ( that was found out in practice ). A naive
implementation of that form would hobble the system if a new standard
service catalog emerged.

This API responds to that challenge by creating a mechanism by which a service
can be associated with an arbitrary range of options.

.. note::
    This approach will make
    API clients ( including the official web front-ends ) do a lot more work;
    but in this case, we think that it is worthwhile.

Options
---------
"Options" are the possible "choices" in a service questionnare, like the one
shown above.

Using that example: "Yes" and "No" are options for the services under the
"HIV Prevention Services" category, while the numbers "1,2,3,4,5,6" are
options for the KEPH service classification section.

The known service options can be listed and created at ``/api/facilities/options/``. To create a new option, you need to ``POST`` a payload that includes the
following fields:

====================== ====================================================================
Field                   Description
====================== ====================================================================
value                   The value that will be stored in the database, and analyzed. This should be a constant that is friendly to analytical tools e.g one that does not have unnecessary punctuation and spacing. This will be a string.
display_text            The description that will be displayed to the user wherever the option appears in the user interface. This should be plain text. It cannot be blank.
is_exclusive_option     This is a **boolean** value; if ``true``, only one of the exclusive options can be selected for a specific facility and service. A user interface should intepret this by implementing a control that behaves like radio buttons.
option_type             The choices are ``BOOLEAN``, ``INTEGER``, ``DECIMAL`` and ``TEXT``. This controls the type of response data that is valid for that option.
====================== ====================================================================

Here is an example of a valid ``POST`` payload:

.. code-block:: javascript

    {
        "value": "YES",
        "display_text": "Yes",
        "is_exclusive_option": true,
        "option_type": "BOOLEAN"
    }

Service Options
------------------
The service options resource is used to link services and options. To use an
example from the form above, the service "Home Based Care (HBC)" should be
linked with the options ``Yes`` and ``No``. Service options can be viewed and
configured at ``/api/facilities/service_options/``. To create a new link, you
need to know the ``id`` of the service and the option.

For example: to link an option with the ``id`` ``53c3f729-97d1-4c9d-9fff-d2edc797b185`` with the service with the ``id`` ``80613650-f765-4032-a9d3-bb0fc9cc37cc``, ``POST`` to ``/api/facilities/options/`` the following payload:

.. code-block:: javascript

    {
        "service": "80613650-f765-4032-a9d3-bb0fc9cc37cc",
        "option": "53c3f729-97d1-4c9d-9fff-d2edc797b185"
    }


Linking facilities to services
--------------------------------
The final step is to link a facility to the services that it offers.
**Facilities are linked to services through service options.**

If the service option that we created above has the ``id``
``f09af53e-5c6f-468d-a41d-df51693e51a3`` and we'd like to link it to a
facility whose ``id`` is ``c4169b23-5cbb-4ed8-a556-8a4fc43af17e``, ``POST``
to ``/facilities/facility_services/`` the following payload:

.. code-block:: javascript

    {
        "facility": "c4169b23-5cbb-4ed8-a556-8a4fc43af17e",
        "selected_option": "f09af53e-5c6f-468d-a41d-df51693e51a3"
    }

.. toctree::
    :maxdepth: 2
