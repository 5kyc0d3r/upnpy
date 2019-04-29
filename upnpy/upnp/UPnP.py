from upnpy.ssdp.SSDPRequest import SSDPRequest
import upnpy.utils as utils

from functools import wraps


def _device_required(func):

    """
    Decorator for checking whether a device was selected or not.
    """

    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        if instance.selected_device is None:
            raise ValueError('No device has been selected.')
        return func(instance, *args, **kwargs)
    return wrapper


class UPnP:

    """
        **UPnP object**

        A UPnP object used for device discovery and service action invocation.
    """

    def __init__(self):
        self.ssdp = SSDPRequest()
        self.discovered_devices = []
        self.selected_device = None

    def discover(self, delay=2, **headers):

        """
            **Find UPnP devices on the network**

            Find available UPnP devices on the network by sending an M-SEARCH request.

            :param delay: Discovery delay, amount of time in seconds to wait for a reply from devices
            :type delay: int
            :param headers: Optional headers for the request
            :return: List of discovered devices
            :rtype: list
        """

        discovered_devices = []
        for device in self.ssdp.m_search(discover_delay=delay, st='upnp:rootdevice', **headers):
            discovered_devices.append(device)

        self.discovered_devices = discovered_devices
        return self.discovered_devices

    def select_igd(self):

        """
            **Select the Internet Gateway Device if available**

            Selects the Internet Gateway device if it's available after discovery.

            :return: True if successful or raises a ValueError exception upon failure
            :rtype: bool
        """

        ig_devices = []

        for device in self.discovered_devices:
            device_type = utils.parse_device_type(device.type_)
            if device_type == 'InternetGatewayDevice':
                ig_devices.append(device)

        if len(ig_devices) == 1:
            self.selected_device = ig_devices[0]
            return True
        elif len(ig_devices) > 1:
            raise ValueError('Multiple IGDs found. Specify one manually.')
        else:
            raise ValueError('No IGD found.')

    @_device_required
    def get_services(self):

        """
            **Return a list of services available for the device**

            Returns a list of available services for the device.

            :return: List of services available for this device
            :rtype: list
        """

        return self.selected_device.get_services()

    def __getattr__(self, service_id):

        """
            **Allow access to a specific service through an attribute**

            Allows the user to access a specific service by its ID for the selected device through an attribute.

            :param service_id: ID for the service to select
            :return: Instance of SSDPDevice.Service for the service with the specified service ID
            :rtype: SSDPDevice.Service
        """

        try:
            return self.selected_device.services[service_id]
        except AttributeError:
            raise AttributeError('No device has been selected.')
        except KeyError:
            raise KeyError(f'No service found with ID "{service_id}".')

    def __getitem__(self, service_id):

        """
            **Allow access to a specific service through a dictionary**

            Allows the user to access a specific service by its ID for the selected device through a dictionary key.

            :param service_id: ID for the service to select
            :return: Instance of SSDPDevice.Service for the service with the specified service ID
            :rtype: SSDPDevice.Service
        """

        try:
            return self.selected_device.services[service_id]
        except AttributeError:
            raise AttributeError('No device has been selected.')
        except KeyError:
            raise KeyError(f'No service found with ID "{service_id}".')
