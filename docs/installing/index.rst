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


.. toctree::
    :maxdepth: 3

    evaluator_install
    developer_install
    production_install
