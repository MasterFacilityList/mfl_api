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

.. _`Ansible`: http://www.ansible.com/home
.. _`Ubuntu`: http://www.ubuntu.com/

Setting up the environment
----------------------------
This server is built as a `Twelve-Factor App`_. For that reason, the key
configuration parameters are stored in the environment - set up directly in
the operating system as environment variables or as a `.env` file in the
application's root folder.

The ``.env`` file holds confidential configuration information. For that
reason, it is not tracked in revision control ( revision control has an example
``.env`` whose values should **not** be used in production ).

A proper ``.env`` file should set the following values up:

.. code-block:: text

    SECRET_KEY=pleasechangetoanewlygeneratedsecretkey
    DEBUG=off  # NEVER run with Debug=True in production

    EMAIL_HOST=email-smtp.us-east-1.amazonaws.com  # This is an example
    EMAIL_HOST_USER=donotleakthisvalue
    EMAIL_HOST_PASSWORD=keepthisonesecretalso


    # Here because the original user was too lazy to write ruby code for the VagrantFile
    DATABASE_USER=mfl  # Change this
    DATABASE_PASSWORD=mfl  # **CHANGE** this, no matter how lazy you feel
    DATABASE_NAME=mfl  # Change this

    # Make sure you change this in lockstep with the three DATABASE_* vars above
    DATABASE_URL='postgres://mfl:mfl@localhost:5432/mfl'


.. _Twelve-Factor App: http://12factor.net/

.. warning::

    Please make sure that you have set up secure values.

    You will need to save a copy of the ``.env`` at a secure location ( not in
    the code repository ). If you loose the ``.env`` / forget the values, you
    could lose the ability to maintain the deployed production system.

The pre-deploy checklist
---------------------------
You **MUST** work your way through the `Django deployment checklist`_.

.. _`Django deployment checklist`: https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

Configuring the ansible inventory
-------------------------------------
There is an ``inventory`` file in the ``playbooks`` folder. This file should
be edited to have a line for each server that is managed by Ansible.

The following is an example:

.. code-block:: text

    azure_test_server             ansible_ssh_host=mfl.azure.slade360.co.ke     ansible_ssh_port=22     ansible_ssh_user=azureuser     ansible_ssh_private_key_file=/home/ngurenyaga/.ssh/id_rsa

The template breaks down roughly to this:

.. code-block:: text

    <a descriptive name we choose for the server>
    ansible_ssh_host=<an IP address or host name>
    ansible_ssh_port=<the port over which the SSL daemon is listening on the remote machine>
    ansible_ssh_user=<the username to log in with on the remote machine>
    ansible_ssh_private_key_file=<a path to a local SSH private key>

.. warning::

    The SSH private key must be kept private.

.. warning::

    If you are working off a recent Ubuntu Linux on your laptop, you should
    comment out ``SendEnv LANG LC_*`` in ``/etc/ssh/ssh_config``.

    The forwarding of language environment variables from the local computer
    is known to cause mischief on the remote server.

.. warning::

    This server should only be run on a non-threaded server e.g ``gunicorn``
    in the standard multi-process configuration.

    This is because the geographic features rely on ``GDAL``, which is not
    thread safe.


.. toctree::
    :maxdepth: 2
