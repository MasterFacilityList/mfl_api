Installing for evaluation
============================
In this scenario, you do not plan to make any changes to the MFL API server
but you need to have a local copy against which you can test a new API
client or a new third party integration.

We recommend that you use `Vagrant`_ and `Virtualbox`_ to create a test
server for yourself.

.. _Vagrant: https://www.vagrantup.com/
.. _Virtualbox: https://www.virtualbox.org/

If you are an expert Vagrant user, you can substitute Virtualbox with VMWare
Desktop / Player, HyperV etc. You'll have an easier time if you are on a
``_nix`` e.g Ubuntu or OS X.


TBD - complete this

Deployment Assumptions
-----------------------
The deployment scripts will fail unless the following are true:

  * you are on a recent Ubuntu ( Ubuntu 14.04LTS or newer should work, other Debian derivatives *may* work )
  * you have run ``ssh-keygen`` and have a public key at ``$HOME/.ssh/id_rsa.pub``

Vagrant
----------
You will need to have the vagrant-env plugin - https://github.com/gosuri/vagrant-env .


.. toctree::
    :maxdepth: 2
