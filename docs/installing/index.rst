Installing
==============

Supported operating systems
-----------------------------
This system has been developed and tested on Ubuntu Linux ( any Ubuntu that is currently "in support" will do ). It should be *trivial* to get it working on any ``*NIX`` ( including OS X ). It is *possible* to get it running on Windows, but we have not put any work into it. If you've got a burning desire to see the server running on Windows, you are encouraged to test it there and send issue pull requests for any fixes that would be needed.

Kindly note that this restriction applies to the servers only, and not to any of the API clients e.g browsers and third party systems. Clients can run on any modern operating system.

System dependencies
--------------------
The system needs system level installations of ``postgresql``, ``postgis``, ``geos``, ``proj``, ``gdal``, ``elasticsearch`` and ``graphviz``.

If you are on a recent Ubuntu Linux, you can get them all with:

::

    sudo apt-get install binutils postgis gdal-bin libproj-dev
    libgeoip1 graphviz libgraphviz-dev

In order to build some of the Python dependencies in the virtualenv, some
libraries will need to be in place. Again, if you are on a recent Ubuntu, you
can get them at once with:

::

    sudo apt-get build-dep python-shapely python-gdal python-numpy
    cython python-psycopg2


.. toctree::
    :maxdepth: 2

    evaluator_install
    developer_install
    production_install
