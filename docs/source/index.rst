UPnPy Documentation
=================================

.. _Internet Gateway Device: https://en.wikipedia.org/wiki/Internet_Gateway_Device_Protocol

.. image:: https://travis-ci.org/5kyc0d3r/upnpy.svg?branch=master
    :target: https://travis-ci.org/5kyc0d3r/upnpy

.. image:: https://img.shields.io/pypi/pyversions/upnpy.svg
    :target: https://pypi.org/project/upnpy

.. image:: https://img.shields.io/badge/license-MIT-red.svg
    :target: https://github.com/5kyc0d3r/upnpy/blob/master/LICENSE


Lightweight UPnP client library for Python.


What is UPnPy?
^^^^^^^^^^^^^^
UPnPy is a lightweight UPnP client library for Python. It can discover devices and invoke UPnP actions.


Install
+++++++

::

    $ pip install upnpy


.. toctree::
   :maxdepth: 2
   :caption: Table of Contents:

   Install
   Introduction
   modules


Examples:
^^^^^^^^^
**Get the external IP address of an** `Internet Gateway Device`_ **:**

::

        import upnpy

        upnp = upnpy.UPnP()
        upnp.discover()  # Discover UPnP devices on the network

        upnp.select_igd()  # Select the IGD

        # Select the service which implements the "GetExternalIPAddress" action
        # Some routers don't implement WANIPConnection but WANPPPConnection instead:
        # urn:schemas-upnp-org:service:WANPPPConnection:1
        upnp.select_service('urn:schemas-upnp-org:service:WANIPConnection:1')

        # Execute the "GetExternalIPAddress" action
        upnp.execute('GetExternalIPAddress')

If the above code executed successfully, it should return a dictionary containing the external IP Address:

::

    {'NewExternalIPAddress': 'xxx.xxx.xxx.xxx'}




**Add a new port mapping to an** `Internet Gateway Device`_ **:**

::

    import upnpy

    upnp = upnpy.UPnP()
    upnp.discover()  # Discover UPnP devices on the network

    upnp.select_igd()  # Select the IGD

    # Select the service which implements the "AddPortMapping" action
    # Some routers don't implement WANIPConnection but WANPPPConnection instead:
    # urn:schemas-upnp-org:service:WANPPPConnection:1
    upnp.select_service('urn:schemas-upnp-org:service:WANIPConnection:1')

    # Execute the "AddPortMapping" action
    upnp.execute('AddPortMapping', 80, 'TCP', 8000, '192.168.1.3', 'Test UPnPy entry')

If the above code executed successfully, a new port mapping should've been created on your router.

If the above code executed successfully, a new port mapping should've been created on your router.

``80`` is the port that will be opened on the WAN side of the router

``TCP`` is the transport protocol you want to use (can also be UDP)

``8000`` is the port of the internal client where a server will be listening

``192.168.1.3`` is the IP of the internal client where connections should be forwarded to

``Test UPnPy entry`` is a description of the port mapping.

Returns an empty dictionary:

::

    {}


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
