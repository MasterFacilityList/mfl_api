Installing for production
============================
TBD - **everything here is work in progress**



Deployment notes
-----------------
Because this server uses ``GDAL``, which is not threadsafe, it should not be
deployed behind a threaded server / WSGI server.


.. toctree::
    :maxdepth: 2
