# UPnPy
[![Build Status](https://travis-ci.org/5kyc0d3r/upnpy.svg?branch=master)](https://travis-ci.org/5kyc0d3r/upnpy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/upnpy.svg)](https://pypi.org/project/UPnPy/)
[![PyPI package version](https://img.shields.io/pypi/v/upnpy.svg)](https://pypi.org/project/UPnPy/)
[![MIT License](https://img.shields.io/badge/license-MIT-red.svg)](https://github.com/5kyc0d3r/upnpy/blob/master/LICENSE)

Lightweight UPnP client library for Python.

## Install
```
$ pip install upnpy
```

## Examples

#### Get the external IP address of an [Internet Gateway Device](https://en.wikipedia.org/wiki/Internet_Gateway_Device_Protocol):
```python
import upnpy

upnp = upnpy.UPnP()

# Discover UPnP devices on the network
# Returns a list of devices e.g.: [Device <Broadcom ADSL Router>]
devices = upnp.discover()

# Select the IGD
# alternatively you can select the device directly from the list
# device = devices[0]
device = upnp.get_igd()

# Get the services available for this device
# Returns a list of services available for the device
# e.g.: [<Service (WANPPPConnection) id="WANPPPConnection.1">, ...]
device.get_services()

# We can now access a specific service on the device by its ID
# The IDs for the services in this case contain illegal values so we can't access it by an attribute
# If the service ID didn't contain illegal values we could access it via an attribute like this:
# service = device.WANPPPConnection

# We will access it like a dictionary instead:
service = device['WANPPPConnection.1']

# Get the actions available for the service
# Returns a list of actions for the service:
#   [<Action name="SetConnectionType">,
#   <Action name="GetConnectionTypeInfo">,
#   <Action name="RequestConnection">,
#   <Action name="ForceTermination">,
#   <Action name="GetStatusInfo">,
#   <Action name="GetNATRSIPStatus">,
#   <Action name="GetGenericPortMappingEntry">,
#   <Action name="GetSpecificPortMappingEntry">,
#   <Action name="AddPortMapping">,
#   <Action name="DeletePortMapping">,
#   <Action name="GetExternalIPAddress">]
service.get_actions()

# Finally, get the external IP address
# Execute the action by its name
# Returns a dictionary: {'NewExternalIPAddress': 'xxx.xxx.xxx.xxx'}
service.GetExternalIPAddress()
```

#### Add a new port mapping to an [Internet Gateway Device](https://en.wikipedia.org/wiki/Internet_Gateway_Device_Protocol):
```python
import upnpy

upnp = upnpy.UPnP()

# Discover UPnP devices on the network
# Returns a list of devices e.g.: [Device <Broadcom ADSL Router>]
devices = upnp.discover()

# Select the IGD
# alternatively you can select the device directly from the list
# device = devices[0]
device = upnp.get_igd()

# Get the services available for this device
# Returns a list of services available for the device
# e.g.: [<Service (WANPPPConnection) id="WANPPPConnection.1">, ...]
device.get_services()

# We can now access a specific service on the device by its ID
# The IDs for the services in this case contain illegal values so we can't access it by an attribute
# If the service ID didn't contain illegal values we could access it via an attribute like this:
# service = device.WANPPPConnection

# We will access it like a dictionary instead:
service = device['WANPPPConnection.1']

# Get the actions available for the service
# Returns a list of actions for the service:
#   [<Action name="SetConnectionType">,
#   <Action name="GetConnectionTypeInfo">,
#   <Action name="RequestConnection">,
#   <Action name="ForceTermination">,
#   <Action name="GetStatusInfo">,
#   <Action name="GetNATRSIPStatus">,
#   <Action name="GetGenericPortMappingEntry">,
#   <Action name="GetSpecificPortMappingEntry">,
#   <Action name="AddPortMapping">,
#   <Action name="DeletePortMapping">,
#   <Action name="GetExternalIPAddress">]
service.get_actions()

# The action we are looking for is the "AddPortMapping" action
# Lets see what arguments the action accepts
# Use the get_input_arguments() or get_output_arguments() method of the action
# for a list of input / output arguments.
# Example output of the get_input_arguments method for the "AddPortMapping" action
# Returns a dictionary:
# [
#     {
#         "name": "NewRemoteHost",
#         "data_type": "string",
#         "allowed_value_list": []
#     },
#     {
#         "name": "NewExternalPort",
#         "data_type": "ui2",
#         "allowed_value_list": []
#     },
#     {
#         "name": "NewProtocol",
#         "data_type": "string",
#         "allowed_value_list": [
#             "TCP",
#             "UDP"
#         ]
#     },
#     {
#         "name": "NewInternalPort",
#         "data_type": "ui2",
#         "allowed_value_list": []
#     },
#     {
#         "name": "NewInternalClient",
#         "data_type": "string",
#         "allowed_value_list": []
#     },
#     {
#         "name": "NewEnabled",
#         "data_type": "boolean",
#         "allowed_value_list": []
#     },
#     {
#         "name": "NewPortMappingDescription",
#         "data_type": "string",
#         "allowed_value_list": []
#     },
#     {
#         "name": "NewLeaseDuration",
#         "data_type": "ui4",
#         "allowed_value_list": []
#     }
# ]
service.AddPortMapping.get_input_arguments()

# Finally, add the new port mapping to the IGD
# This specific action returns an empty dict: {}
service.AddPortMapping(
    NewRemoteHost='',
    NewExternalPort=80,
    NewProtocol='TCP',
    NewInternalPort=8000,
    NewInternalClient='192.168.1.3',
    NewEnabled=1,
    NewPortMappingDescription='Test port mapping entry from UPnPy.',
    NewLeaseDuration=0
)
```

## Documentation
Documentation is available at [https://upnpy.readthedocs.io/en/latest/](https://upnpy.readthedocs.io/en/latest/)

## License
This project is licensed under the terms of the [MIT License](https://github.com/5kyc0d3r/upnpy/blob/master/LICENSE).
