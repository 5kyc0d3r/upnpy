from upnpy.ssdp.SSDPRequest import SSDPRequest
from upnpy.ssdp.SSDPDevice import SSDPDevice

from functools import wraps


def _device_required(func):
    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        if instance.selected_device:
            return func(instance, *args, **kwargs)
        raise ValueError('No device has been selected.')
    return wrapper


class UPnP:

    """
        **UPnP object**

        A UPnP object used for device discovery and service action invocation.
    """

    def __init__(self):
        self.ssdp = SSDPRequest()
        self.soap = None
        self.discovered_devices = []
        self.selected_device = None

    def discover(self, delay=2, st='ssdp:all', **headers):

        """
            **Find UPnP devices on the network**

            Find available UPnP devices on the network by sending an M-SEARCH request.

            :param delay: Discovery delay, amount of time in seconds to wait for a reply from devices
            :type delay: int
            :param st: Discovery search target (defaults to ssdp:all)
            :type st: str
            :param headers: Optional headers for the request
            :return: The amount of devices discovered
            :rtype: int
        """

        discovered_devices = []
        for device in self.ssdp.m_search(discover_delay=delay, st=st, **headers):
            discovered_devices.append(device)

        self.discovered_devices = discovered_devices
        return len(self.discovered_devices)

    @_device_required
    def get_services(self):

        """
            **Get the services offered by the device**

            Gets a list of services available on the currently selected device.

            :return: List of services offered by the currently selected device
            :rtype: list
        """

        return self.selected_device.get_services()

    @_device_required
    def get_actions(self):

        """
            **Get the service actions**

            Gets the actions available for the currently selected service.

            :return: List of actions available for the current service
            :rtype: list
        """

        return self.selected_device.get_selected_service().get_actions()

    def select_igd(self):

        """
            **Select the Internet Gateway Device if available**

            Selects the Internet Gateway device if it's available after discovery.

            :return: True if successful or raises a ValueError exception upon failure
            :rtype: bool
        """

        device_filter = SSDPDevice.filter_by(
            self.discovered_devices,
            headers={'ST': 'urn:schemas-upnp-org:device:InternetGatewayDevice:1'}
        )

        device_filter_length = len(device_filter)

        if device_filter_length == 1:
            igd = device_filter[0]
            self.selected_device = igd
            return True

        elif device_filter_length > 1:
            raise ValueError('Multiple IGDs found.')

        else:
            raise ValueError('No IGDs found.')

    @_device_required
    def select_service(self, service):

        """
            **Select a service to use**

            Select a service to use available on the selected device.

            :param service: The service to select
            :type service: str, SSDPDevice.Service
            :return: True if selection was successful or raises a ValueError exception upon failure
            :rtype: bool
        """

        return self.selected_device.select_service(service)

    def execute(self, action, *action_args, **action_kwargs):

        """
            **Invoke an action for the selected service**

            :param action: The action to invoke
            :type action: str, SOAPAction
            :param action_args: If the action requires parameters, pass them here
            :param action_kwargs: If the action requires parameters, pass them here
            :return: The response of the invoked action
            :rtype: dict
        """

        return self.selected_device.get_selected_service().execute(action, *action_args, **action_kwargs)
