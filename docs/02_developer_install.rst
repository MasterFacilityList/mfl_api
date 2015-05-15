Installing for development
============================

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
    libxml2-dev libxslt1-dev libffi-dev



.. _virtualenv: https://virtualenv.pypa.io/en/latest/

.. note::

    You must ensure that ElasticSearch is running. In a typical Ubuntu install
    ( from the `.deb` supplied by ElasticSearch ), the search server is not
    started by default.

Getting started
----------------
**A: Running the system from source code**

1. Create a virtualenv

2. Activate the created vitualenv and run ``pip install -r requirements.``

3. Run ``fab setup``
    Running this command will do the following:

    * Create the database.

    * Run migrations.

    * Load demo data if the project **DEBUG** attribute in settings is set to true .

**B: Installing the system**


2. Activate the virtualenv and run ``python setup.py install`` while in the project folder.


.. toctree::
    :maxdepth: 2
