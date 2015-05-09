Installing for production
============================
This server has been developed and tested on `Ubuntu`_ Linux ( any Ubuntu
that is currently "in support" will do ). It should be *trivial* to get it
working on any ``*NIX`` ( including OS X ). It is *possible* to get it
running on Windows, but we have not put any work into it. If you've got a
burning desire to see the server running on Windows, you are encouraged to
test it there and issue pull requests for any fixes that would be needed.

Kindly note that this restriction applies to the servers only, and not to
any of the API clients e.g browsers and third party systems. Clients can
run on any modern operating system.

We supply an `Ansible`_ playbook that automates this entire process.

.. _Ansible: http://www.ansible.com/home
.. _Ubuntu: http://www.ubuntu.com/


TBD - Add notes about removing LC forwarding from SSH config
TBD - **everything here is work in progress**

TODO - Django deploy checklist'
TODO - Can only be in a non-threaded server, because of ``GDAL``
( for those who will not use the supplied playbooks )


.. toctree::
    :maxdepth: 2
