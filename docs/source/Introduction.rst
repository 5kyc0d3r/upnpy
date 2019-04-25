Introduction
============

.. _Internet Gateway Device: https://en.wikipedia.org/wiki/Internet_Gateway_Device_Protocol

UPnPy can discover UPnP devices, get a list of its services and invoke actions for the services.
See below for the basic usage of UPnPy.

Quickstart
^^^^^^^^^^

**Get the external IP address of an** `Internet Gateway Device`_ **:**
----------------------------------------------------------------------

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
-----------------------------------------------------------------

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
