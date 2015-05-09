MFL 2: The Big Picture
=========================
The Master Facilities List is one of the building blocks of the Kenyan
national health information system. The second edition of the MFL is focused
on interoperability, standardization and unification.

Interoperability
------------------
This system adopts an **API First** approach, as explained in the :doc:`06_api`
chapter.

The authors have gone to great lengths to make it easy for other systems
- with the correct authorization - to read and write MFL data.

Standardization
-----------------
The MFL's core mission includes the standardization of facility codes. In this
edition, the core mission has been expanded to include the standardization of
service codes. You can read more about that in the :doc:`09_services` chapter.

Unification
--------------
The first generation of the Master Facilities List ( and its "satellites" )
had five semi-independent systems: public and administration systems for the
"core" MFL, a mirror of those two for the Master Community Units List and
a regulators interface.

This release unifies them all under a single API. That API is client agnostic
- the client could be a web or mobile application, another system or even a
reporting tool.

.. note::

    A future release of this system could standardize more things e.g
    practitioner codes.

.. toctree::
    :maxdepth: 2
