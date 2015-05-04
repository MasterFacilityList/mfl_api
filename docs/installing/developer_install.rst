Installing for development
============================
TBD - **everything here is work in progress**

TODO - Add notes about removing LC forwarding from SSH config


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
    :maxdepth: 3
