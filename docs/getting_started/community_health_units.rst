MFL APIs: Community Health Units
==================================
This chapter assumes that the reader is familiar with the general
principles explained in the :doc:`api` chapter.

This chapter concerns itself with the resources that model community health
units and link them to facilities.

.. note::

    Community health units are an extension of the Master Facilities List. A
    community health unit is a health service delivery structure within a
    defined geographic area covering a population of approximately 5,000
    people.

    Each unit is assigned 2 Community Health Extension Workers ( CHEWs ) and community health volunteers who offer promotie, preventative and basic
    curative services.

    Each unit is governed by a Community Health Committee ( CHC ) and is
    **linked to a specific health facility**.

    The role of a community health unit is to bring services closer to the
    people that need them. Those services include:

        * Water and sanitation hygiene; e.g. Faecal management, Household water treatment and demonstrations on hand washing with soap, etc.
        * Advice on maternal and child health e.g. Immunization, Individual birth plan, etc.
        * Provision of Family planning commodities.
        * Growth monitoring for children under 5 years.
        * Deworming of children.
        * Provision of Long Lasting Insecticide Treated Nets (LLITNs).
        * Management of diarrhea, injuries, wounds, jiggers and other minor illnesses.
        * Provision of Information, Education & Communication (IEC) materials
        * Defaulter tracing (ART, TB and Immunization)
        * Referrals to health facilities
        * First Aid Services

The implementation of community health units in this API is semi-independent.
The units connect to the rest of MFL at only one point - their linkage to
facilities.

Community Health Unit Approvers
----------------------------------
The community health approvers resource holds the details of entities that are
involved in approval of community health units.

The known approvers can be listed by issuing a ``GET`` to ``/api/chul/approvers/``. To register a new approving entity, you need to supply a
``name``, ``description`` and ``abbreviation``. The following example
illustrates that:

.. code-block:: javascript

    {
        "name": "Division of Community Health Services",
        "description": "Division of Community Health Services, Ministry of Health",
        "abbreviation": "DCHS"
    }

Community Health Unit Statuses
--------------------------------
The community health unit statuses that are known / available can be listed at
``/api/chul/statuses/`` via ``GET``. These will be used to mark the current
status of a community health unit, and when analysing the status of registered
community health units.

To create a new status, you need to ``POST`` a ``name`` and a ``description``.
Here is an example payload:

.. code-block:: javascript

    {
        "name": "ACTIVE",
        "description": "Actively Deployed"
    }

.. note::

    This reflects the operational status of the Community Health Unit.

Community Health Units
------------------------
Community health units can be listed via ``GET`` to ``/api/chul/units/``.

To add a new community health unit, ``POST`` to ``/api/chul/units/``, ``POST``
a payload that has a ``name``, ``facility`` and ``status``. For the facility
and status, the ``id`` s are sent ( foreign keys ).

For example:

.. code-block:: javascript

    {
        "name": "Gachie Health Unit",
        "facility": "2927d31f-b1a0-4d17-93b0-ea648af7b9f0",
        "status": "0e2ba3fc-9c81-4c30-b52e-b62664462cb7"
    }

.. note::

    The community health unit ``code`` is auto-assigned. Immediately after
    creating the facility record, the code ( and other auto-assigned fields )
    will be inserted in the response.

Community Health Unit Contacts
+++++++++++++++++++++++++++++++++
A community health unit may be linked to zero or more contacts. The contacts
will have been created at ``/api/common/contacts/`` using APIs that are
discussed in the :doc:`support_resources` chapter.

Community health unit contacts can be listed and created at
``/api/common/contacts/``. To list a community health unit to a contact,
``POST`` to that endpoint the ``id`` of the contact and the ``id`` of the
community health unit. The example payload below illustrates that:

.. code-block:: javascript

    {
        "health_unit": "2d425ab7-0002-4b95-9cd1-638972efb75d",
        "contact": "7dd62ab9-94c2-48d6-a10f-d903bd57acd5"
    }

Community Health Unit Approvals
++++++++++++++++++++++++++++++++++
The approval status of community health units is listed / maintained at
``/api/chul/unit_approvals/``.

To record a new approval, you should supply a ``comment``, ``approval_date``,
``approver``, ``approval_status`` and ``health_unit``.

The ``approver`` is the ``id`` of an approver registered at
``/api/chul/approvers/``. The ``approval_status`` is the ``id`` of an
approval status registered at ``/api/chul/approval_statuses/``.
The ``health_unit`` is the ``id`` of a community health unit registered at
``/api/chul/units/``. The ``comment`` is a free-text explanation, while the
``approval_date`` is an ISO 8601 **date** ( not datetime ) string that
represents the date when the approval occured.

The following example is a valid ``POST`` payload:

.. code-block:: javascript

    {
        "comment": "For documentation / training purposes",
        "approval_date": "2015-05-09",
        "approver": "02b610c1-067f-4e0c-9bad-31cc029f6ee3",
        "approval_status": "44c2abfd-3944-484f-ae4c-b30778e25398",
        "health_unit": "96645d26-8e4e-4078-9e10-a5176f5432df"
    }

.. note::

    This reflects the approval status of the Community Health Unit.

Community Health Workers
--------------------------
Community health workers are attached to community health units. They are
listed and maintained at ``/api/chul/workers/``.

When registering a new community health worker, supply a ``first_name``,
``last_name``, ``surname``, ``id_number`` and ``health_unit``. The
``health_unit`` is the ``id`` of the community health unit that the worker
is attached to, and can be retrieved from ``/api/chul/units/``.

.. code-block:: javascript

    {
        "first_name": "Does",
        "last_name": "Not",
        "surname": "Exist",
        "id_number": 545432,
        "health_unit": "96645d26-8e4e-4078-9e10-a5176f5432df"
    }

Community Health Workers Contacts
------------------------------------
A community health worker can be linked to a contact that has already been
registered at ``/api/common/contacts/`` by ``POST`` ing to
``/api/chul/workers_contacts/`` the ``id`` of the worker and the ``id`` of the
contact.

For example:

.. code-block:: javascript

    {
        "health_worker": "db04b653-b0f7-434f-a224-3ea4d93b69c1",
        "contact": "2d04afdc-46a8-4b11-85b8-63f5c035366f"
    }

Community Health Workers Approvals
-------------------------------------
The approval status of community health workers is maintained at
``/api/chul/worker_approvals/``.

The key pieces of information to maintain about each approval are
the ``approver`` ( an ``id`` of an approver registered at
``/api/chul/approvers/`` ), ``approval_status`` ( ``id`` of an
approval status registered at ``/api/chul/approval_statuses/`` )
and ``health_worker`` ( ``id`` of a health worker registered at
``/api/chul/workers/`` ) and a free-form ``comment``.

The example below is a valid ``POST`` payload:

.. code-block:: javascript

    {
        "approver": "02b610c1-067f-4e0c-9bad-31cc029f6ee3",
        "approval_status": "44c2abfd-3944-484f-ae4c-b30778e25398",
        "health_worker": "db04b653-b0f7-434f-a224-3ea4d93b69c1",
        "comment": "Documentation example"
    }

.. toctree::
    :maxdepth: 2
