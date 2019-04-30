# UPnPy
[![Build Status](https://travis-ci.org/5kyc0d3r/upnpy.svg?branch=master)](https://travis-ci.org/5kyc0d3r/upnpy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/upnpy.svg)](https://pypi.org/project/UPnPy/)
[![PyPI package version](https://img.shields.io/pypi/v/upnpy.svg)](https://pypi.org/project/UPnPy/)
[![MIT License](https://img.shields.io/badge/license-MIT-red.svg)](https://github.com/5kyc0d3r/upnpy/blob/master/LICENSE)

Lightweight UPnP client library for Python.

## Examples

#### Get the external IP address of an [Internet Gateway Device](https://en.wikipedia.org/wiki/Internet_Gateway_Device_Protocol):
```python
>>> import upnpy
>>> upnp = upnpy.UPnP()
>>>
>>> devices = upnp.discover()  # Discover UPnP devices on the network
>>> devices
[Device <Broadcom ADSL Router>]
>>>
>>> device = upnp.get_igd()  # Select the IGD
>>> # Or alternatively
>>> device = devices[0]
>>>
>>> device.get_services()  # Get the services available for this device
[<Service (Layer3Forwarding) id="Layer3Forwarding.1">, <Service (WANCommonInterfaceConfig) id="WANCommonInterfaceConfig.1">, <Service (WANPPPConnection) id="WANPPPConnection.1">]
>>>
>>> # We can now access a specific service on the device by its ID
>>> # The IDs for the services in this case contain illegal values so we can't access it by an attribute
>>> # so we access it like a dictionary instead.
>>> device['WANPPPConnection.1']
<Service (WANPPPConnection) id="WANPPPConnection.1">
>>> # Get the actions available for the service
>>> device['WANPPPConnection.1'].get_actions()
[<Action name="SetConnectionType">, <Action name="GetConnectionTypeInfo">, <Action name="RequestConnection">, <Action name="ForceTermination">, <Action name="GetStatusInfo">, <Action name="GetNATRSIPStatus">, <Action name="GetGenericPortMappingEntry">, <Action name="GetSpecificPortMappingEntry">, <Action name="AddPortMapping">, <Action name="DeletePortMapping">, <Action name="GetExternalIPAddress">]

>>> device['WANPPPConnection.1'].GetExternalIPAddress()  # Finally, get the external IP address
{'NewExternalIPAddress': 'xxx.xxx.xxx.xxx'}
```


#### Add a new port mapping to an [Internet Gateway Device](https://en.wikipedia.org/wiki/Internet_Gateway_Device_Protocol):
```python
>>> import upnpy
>>> upnp = upnpy.UPnP()
>>>
>>> devices = upnp.discover()  # Discover UPnP devices on the network
>>> devices
[Device <Broadcom ADSL Router>]
>>>
>>> device = upnp.get_igd()  # Select the IGD
>>> # Or alternatively
>>> device = devices[0]
>>>
>>> device.get_services()  # Get the services available for this device
[<Service (Layer3Forwarding) id="Layer3Forwarding.1">, <Service (WANCommonInterfaceConfig) id="WANCommonInterfaceConfig.1">, <Service (WANPPPConnection) id="WANPPPConnection.1">]
>>>
>>> # We can now access a specific service on the device by its ID
>>> # The IDs for the services in this case contain illegal values so we can't access it by an attribute
>>> # so we access it like a dictionary instead.
>>> device['WANPPPConnection.1']
<Service (WANPPPConnection) id="WANPPPConnection.1">
>>> # Get the actions available for the service
>>> device['WANPPPConnection.1'].get_actions()
[<Action name="SetConnectionType">, <Action name="GetConnectionTypeInfo">, <Action name="RequestConnection">, <Action name="ForceTermination">, <Action name="GetStatusInfo">, <Action name="GetNATRSIPStatus">, <Action name="GetGenericPortMappingEntry">, <Action name="GetSpecificPortMappingEntry">, <Action name="AddPortMapping">, <Action name="DeletePortMapping">, <Action name="GetExternalIPAddress">]

>>> device['WANPPPConnection.1'].AddPortMapping
<Action name="AddPortMapping">
>>>
>>> # Lets see what arguments the action accepts
>>> # (use the get_output_arguments() method for a list of output arguments)
>>> device['WANPPPConnection.1'].AddPortMapping.get_input_arguments()
[{'name': 'NewRemoteHost', 'data_type': 'string', 'allowed_value_list': []}, {'name': 'NewExternalPort', 'data_type': 'ui2', 'allowed_value_list': []}, {'name': 'NewProtocol', 'data_type': 'string', 'allowed_value_list': ['TCP', 'UDP']}, {'name': 'NewInternalPort', 'data_type': 'ui2', 'allowed_value_list': []}, {'name': 'NewInternalClient', 'data_type': 'string', 'allowed_value_list': []}, {'name': 'NewEnabled', 'data_type': 'boolean', 'allowed_value_list': []}, {'name': 'NewPortMappingDescription', 'data_type': 'string', 'allowed_value_list': []}, {'name': 'NewLeaseDuration', 'data_type': 'ui4', 'allowed_value_list': []}]
>>>
>>> # Yikes, lets pretty print that :)
>>> import json
>>> print(json.dumps(device['WANPPPConnection.1'].AddPortMapping.get_input_arguments(), indent=4))
[
    {
        "name": "NewRemoteHost",
        "data_type": "string",
        "allowed_value_list": []
    },
    {
        "name": "NewExternalPort",
        "data_type": "ui2",
        "allowed_value_list": []
    },
    {
        "name": "NewProtocol",
        "data_type": "string",
        "allowed_value_list": [
            "TCP",
            "UDP"
        ]
    },
    {
        "name": "NewInternalPort",
        "data_type": "ui2",
        "allowed_value_list": []
    },
    {
        "name": "NewInternalClient",
        "data_type": "string",
        "allowed_value_list": []
    },
    {
        "name": "NewEnabled",
        "data_type": "boolean",
        "allowed_value_list": []
    },
    {
        "name": "NewPortMappingDescription",
        "data_type": "string",
        "allowed_value_list": []
    },
    {
        "name": "NewLeaseDuration",
        "data_type": "ui4",
        "allowed_value_list": []
    }
]
>>> # Finally, add the new port mapping to the IGD
>>> device['WANPPPConnection.1'].AddPortMapping(
...     NewRemoteHost='',
...     NewExternalPort=80,
...     NewProtocol='TCP',
...     NewInternalPort=8000,
...     NewInternalClient='192.168.1.3',
...     NewEnabled=1,
...     NewPortMappingDescription='Test port mapping entry from UPnPy.',
...     NewLeaseDuration=0
... )
{}
```

## Documentation
Documentation is available at [https://upnpy.readthedocs.io/en/latest/](https://upnpy.readthedocs.io/en/latest/)

## License
This project is licensed under the terms of the [MIT License](https://github.com/5kyc0d3r/upnpy/blob/master/LICENSE).
