Installing for evaluation
============================
In this scenario, you do not plan to make any changes to the MFL API server
but you need to have a local copy against which you can test a new API
client or a new third party integration.

We recommend that you use `Vagrant`_ and `Virtualbox`_ to create a test
server for yourself.

.. _Vagrant: https://www.vagrantup.com/
.. _Virtualbox: https://www.virtualbox.org/
.. _Ansible: https://docs.ansible.org

If you are an expert Vagrant user, you can substitute Virtualbox with VMWare
Desktop / Player, HyperV etc. You'll have an easier time if you are on a
``_nix`` e.g Ubuntu or OS X.


Deployment Assumptions
-----------------------
The deployment scripts will fail unless the following are true:

  * you are on a vagrant supported OS ( so far Ubuntu 14.04LTS and ArchLinux have been tested )
  * you have run ``ssh-keygen`` and have a public key at ``$HOME/.ssh/id_rsa.pub``

Vagrant
----------
Before installation, you will need to have the vagrant-env plugin - https://github.com/gosuri/vagrant-env .
The installation is as simple as running

::

    vagrant plugin install vagrant-env


`Ansible`_ is used to provision the vagrant box. An understanding of ansible is recommended though not required.


Installation
-----------------

1. Ensure vagrant is installed

2. Create a python virtual environment and activate the created virtual environment.

3. Install ``ansible`` in the virtual environment.

4. Set the following environment variables:

    - ``DATABASE_NAME`` the name of the database to user
    - ``DATABASE_USER`` the database user to use
    - ``DATABASE_PASSWORD`` the database password to use

5. Run ``vagrant up``. It shall download and setup everything in the virtual machine.

6. The system is ready to use

.. toctree::
    :maxdepth: 2
