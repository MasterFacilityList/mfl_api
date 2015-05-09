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

Facility Information Storage
-------------------------------
Facilities
+++++++++++++
TBD

Facility Physical Addresses
++++++++++++++++++++++++++++++
TBD

Facility Contacts
+++++++++++++++++++
TBD

Facility Units
++++++++++++++++
TBD

Facility Services
++++++++++++++++++++
TBD

Facility Workflows
---------------------
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
Facility service ratings
+++++++++++++++++++++++++++
TBD

Facility rating reports
++++++++++++++++++++++++++
TBD

Facility downloads
-----------------------
TBD - explain the "filterable report" approach
TBD - templates for this should live in data ( no static stuff )
TBD - create in data the starter templates

Facility cover letters
++++++++++++++++++++++++++
TBD

Facility correction templates
++++++++++++++++++++++++++++++++
TBD

Facility Excel reports
+++++++++++++++++++++++++
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
