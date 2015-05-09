Facilities
=============
This chapter assumes that the reader is familiar with the general
principles explained in the :doc:`06_api` chapter.

The MFL is not merely a "list" of facilities; it has rich APIs to manage their
life cycles and to support interaction with other healthcare systems. This
chapter concerns itself with what is arguably the "core" of the MFL system
- the maintenance of facility information. Facilities APIs fall into the
following groups:

============================== ================================================
Function                       Resources / APIs
============================== ================================================
Facility Information storage    * Facility
                                * Facility Physical Addresses
                                * Facility Contacts
                                * Facility Units
                                * Facility Services

Facility Workflow / Life cycle  * Approval
                                * Publishing ( synchronization )
                                * Regulation
                                * Upgrade
                                * Downgrade

Facility ratings                * Facility service ratings
                                * Facility ratings report

Facility downloads              * Facility cover letters
                                * Facility correction templates
                                * Facility excel exports

Facility dashboard APIS         * Analysis by administrative units
                                * Analysis by type
                                * Analysis by owner and owner category
                                * Analysis by regulator and regulation status
============================== ================================================

.. note::

    One of the things associated with facilities that are registered on the
    Master Facilities List is a **Master Facilities List ( MFL ) Code**.

    The MFL code is a unique number ( integral ) that is *sequential* and
    *immutable*. The immutability is taken seriously - the MFL codes that
    were issued under the first generation system will not be re-issued under
    the second generation MFL system.

    Codes that are issued under MFL 2 will start at `100000`.

Facility information storage
-------------------------------

.. note::

    These APIs are the "heart" of the MFL system. A well-behaved front-end
    should take an integrated approach, presenting output from these APIs
    under one set of screens ( instead of five sets, one for each resource
    type ).

Facilities
+++++++++++++
Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The facilities that are currently registered can be listed at
``/api/facilities/facilities/``.

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each facility has a UUID ``id``. A facility's detail record can be listed
at ``/api/facilities/facilities/<id>/``. For example: if a facility
record's ``id`` is ``2927d31f-b1a0-4d17-93b0-ea648af7b9f0``, the detail
URL for the facility record will be ``/api/facilities/facilities/2927d31f-b1a0-4d17-93b0-ea648af7b9f0/``.

Filtering and search
~~~~~~~~~~~~~~~~~~~~~~~
Facilities - as listed at ``/api/facilities/facilities/`` can be filtered using
the following:

==================== ==========================================================
Filter               Explanation
==================== ==========================================================
name                 This does a *case insensitive partial match* but accepts only one name to filter by e.g ``/api/facilities/facilities/?name=molo``.
code                 Filter by **one or more** facility codes e.g ``/api/facilities/facilities/?code=15003,15002``. The ``,`` is used to separate individual parameters. This does exact matches.
description          Similar to ``name`` but operating on descriptions e.g ``/api/facilities/facilities/?name=molo``
facility_type        Filter by the ``id``s of one or more facility types e.g ``/api/facilities/facilities/?facility_type=f25ba517-3b8d-4692-ba7b-3524f6ec58e5,b2225473-08f1-4e86-a47a-0a61cf75e731``. Facility types can be listed at ``/api/facilities/facility_types/``.
operation_status    Filter by the ``id`` of one or more operation statuses from ``/api/facilities/facility_status/``
ward
owner
officer_in_charge
number_of_beds
number_of_cots
open_whole_day
open_whole_week
is_classified
is_published
is_regulated
updated_before
created_before
updated_after
created_after
updated_on
created_on
is_active
search               Perform a full text search that looks through all fields. e.g ``/api/facilities/facilities/?search=endebess`` gives back all facilities that have "endebess" anywhere in their name, description or attributes.
==================== ==========================================================

.. note::

    These filters can be combined / chained.

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
TBD

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
TBD

Facility physical addresses
++++++++++++++++++++++++++++++
Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Filtering and search
~~~~~~~~~~~~~~~~~~~~~~~
TBD

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
TBD

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
TBD

Facility contacts
+++++++++++++++++++
Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Filtering and search
~~~~~~~~~~~~~~~~~~~~~~~
TBD

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
TBD

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
TBD

Facility units
++++++++++++++++
Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Filtering and search
~~~~~~~~~~~~~~~~~~~~~~~
TBD

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
TBD

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
TBD

Facility services
++++++++++++++++++++
Listing multiple records
~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Retrieving a single record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Filtering and search
~~~~~~~~~~~~~~~~~~~~~~~
TBD

Adding a new record
~~~~~~~~~~~~~~~~~~~~~~
TBD

Updating an existing record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

Deleting a record
~~~~~~~~~~~~~~~~~~~~~
TBD

Facility workflows
---------------------

.. note::

    These five workflows are the day-to-day operations performed on the MFL
    system. A well behaved front-end should integrate them into the facility
    information screens that handle the facility information services mentioned
    above, rather than give each of these its own set of screens.

TBD Draw state diagram

The Facility approval workflow
+++++++++++++++++++++++++++++++++
TBD - Makers, checkers

The facility "publishing" workflow
++++++++++++++++++++++++++++++++++++
TBD

The facility regulation workflow
+++++++++++++++++++++++++++++++++++
TBD

The facility upgrade workflow
+++++++++++++++++++++++++++++++
TBD - implement a transitions graph in the database ( setup ); owner type linked
TBD - add data for that
TBD - document!

The facility downgrade workflow
++++++++++++++++++++++++++++++++++
TBD

Facility ratings
-------------------

.. note::

    The facility ratings APIs will be used by both the public and
    administration user interfaces. The public interface's concern is to
    facilitate ratings by the general public. The admninistration interface
    will present read-only summary information.

Facility service ratings
+++++++++++++++++++++++++++
TBD

Facility rating reports
++++++++++++++++++++++++++
TBD

Facility downloads
-----------------------

.. note::

    Some of these downloads e.g the facility correction template are there for
    historical reasons. A better approach would involve the use of mobile
    interfaces ( supported by this server's APIs ) to facilitate data
    collection and data updates in the field.

Facility cover letters
++++++++++++++++++++++++++
TBD

Facility correction templates
++++++++++++++++++++++++++++++++
TBD

Facility Excel reports
+++++++++++++++++++++++++

.. note::

    The authors of this API treated Excel and CSV output as simply **one more
    format that data can be exported into**. Excel and CSV data comes from the
    same serializers that produce the standard API JSON and XML output. This
    has two positive effects:

        * it can use all the available filters
        * every API ( not just the facilities API ) can produce CSV and Excel

TBD

Facility dashboard APIs
--------------------------
TBD - overall explanation of simple dashboards purpose / role

Analysis of facilities by administrative units
++++++++++++++++++++++++++++++++++++++++++++++++++
TBD

Analysis of facilities by type
++++++++++++++++++++++++++++++++
TBD

Analysis of facilities by owner and owner category
+++++++++++++++++++++++++++++++++++++++++++++++++++++
TBD

Analysis of facilities by regulator and regulation status
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
TBD

.. toctree::
    :maxdepth: 2
