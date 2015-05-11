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

. warn::

    If you are working off a recent Ubuntu Linux on your laptop, you will do
    yourself a great 1TBD]a

TBD - Add warning about removing LC forwarding from SSH config
TBD - **everything here is work in progress**

TODO - Can only be in a non-threaded server, because of ``GDAL``
( for those who will not use the supplied playbooks )
TODO - Warning about using this on a production server


.. toctree::
    :maxdepth: 2
