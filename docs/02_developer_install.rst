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

.. note::

    This project has been tested with Python2. It may work with Python3 but it
    has not been tested

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

2. Activate the created vitualenv and run ``pip install -r requirements.txt``

3. Run the following commands sequentially:
    * fab setup_db
        This drops the database if it exists, creates the database and runs migrations.
    * fab load_demo_data
        This will load sample test data for the API if the project **DEBUG**
        attribute in settings is set to `True`.
    * fab recreate_search_index
        Creates an Elasticsearch  index. Before running this command ensure that
        Elasticsearch is up and running. This command causes the data that has been
        loaded in the database to be indexed in ElasticSearch.

.. note ::

    At times during development one may want to retain the database. To do so, 
    call ``fab load_demo_data`` and ``fab recreate_search_index``. 

    Also one may want to recreate the database. Calling ``fab setup_db`` drops the database, 
    creates it again and runs migrations. After this one may proceed to load the data 

    and create the search index as desired.

**B: Installing the system**
    Activate the virtualenv and run ``python setup.py install`` while in the project folder.


.. toctree::
    :maxdepth: 2
