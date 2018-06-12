Master Facility List API
===========================
.. image:: https://circleci.com/gh/MasterFacilityList/mfl_api.svg?style=shield
    :target: https://circleci.com/gh/MasterFacilityList/mfl_api

.. image:: https://badge.fury.io/py/mfl.svg
    :target: http://badge.fury.io/py/mfl

.. image:: https://readthedocs.org/projects/mfl-api-docs/badge/?version=latest
    :target: http://mfl-api-docs.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status


.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/MasterFacilityList/mfl_api
   :target: https://gitter.im/MasterFacilityList/mfl_api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://requires.io/github/MasterFacilityList/mfl_api/requirements.svg?branch=develop
     :target: https://requires.io/github/MasterFacilityList/mfl_api/requirements/?branch=develop
     :alt: Requirements Status

.. image:: https://www.quantifiedcode.com/api/v1/project/5512ed77922647478a419056baf3431c/badge.svg
  :target: https://www.quantifiedcode.com/app/project/5512ed77922647478a419056baf3431c
  :alt: Code issues


This is the API server for the second generation Kenyan Ministry of Health Master Facility List ( MFL ).

The "home" of the canonical / production version is at http://ehealth.or.ke/facilities/ . The latest documentation can always be found at http://mfl-api-docs.readthedocs.org/en/latest/ . That includes installation instructions, guidance for contributors and API documentation.

Quick Dev Setup & Installation Guide
+++++++++++++++++++++++++++++++++++++
NB:
 - This quick setup guide covers Linux **Debian** distributions.
 - Assumes python >=2.7.x is installed (Not python 3.x.x)
 - Assumes the this repository is cloned and available locally.
 - Assumes relevant db is available locally.

1. Go to `PosgreSQL Downloads page`_ and the **The PostgreSQL apt repository**. Do not run any other commands first.
   You can run ``apt-get update`` though. Make sure this is for PostgreSQL 9.x (9.6 tested and worked)
2. Once you've added that apt repository and done with the apt update, run this to install PostgreSQL and the
   relevant support packages.

``apt-get install postgresql-9.6 postgresql-client-9.6 postgresql-contrib-9.6 libpq-dev postgresql-server-dev-9.6 postgresql-9.6-postgis-2.3``

3. Now go ahead and run ``pip install -r requirements.txt`` in the mfl_api virtualenv

.. _PosgreSQL Downloads page: https://www.postgresql.org/download/linux/debian/



Credits
--------
Developed by `Savannah Informatics Limited`_ | info@savannahinformatics.com

.. _Savannah Informatics Limited: http://savannahinformatics.com/


Maintained by `HealthIT | UoN`_ | swaweru@healthit.uonbi.ac.ke

.. _HealthIT | UoN: http://healthit.uonbi.ac.ke/
