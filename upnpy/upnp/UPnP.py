from upnpy.ssdp.SSDPRequest import SSDPRequest
from upnpy.ssdp.SSDPDevice import SSDPDevice, DeviceService
from upnpy.soap.ServiceTemplates import service_templates
from upnpy.soap.Action import SOAPAction

from functools import wraps


def _device_required(func):
    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        if instance.selected_device:
            return func(instance, *args, **kwargs)
        raise ValueError('No device has been selected.')
    return wrapper


def _service_required(func):
    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        if instance.selected_service:
            return func(instance, *args, **kwargs)
        raise ValueError('No service has been selected.')
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
        self.selected_service = None

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
            :type service: str, DeviceService
            :return: True if selection was successful or raises a ValueError exception upon failure
            :rtype: bool
        """

        if type(service) == str:
            service = service
        elif type(service) == DeviceService:
            service = service.service
        else:
            raise ValueError('Service must be either a str or DeviceService object.')

        for device_service in self.selected_device.get_services():
            if device_service.service == service:
                self.selected_service = device_service
                return True

        raise ValueError(f'The "{service}" service is not available for the selected device.')

    @_service_required
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

        if type(action) == str:
            action_name = action
        elif type(action) == SOAPAction:
            action_name = action.name
        else:
            raise ValueError('Action must be either a str or SOAPAction object.')

        for service_action in self.selected_device.get_actions(self.selected_service.service):

            if service_action.name == action_name:
                service_type = self.selected_service.service_type
                service_version = self.selected_service.service_version

                if service_type in service_templates.keys():
                    if service_version in service_templates[service_type].keys():
                        service_template = service_templates[service_type][service_version]
                        return service_template(
                            service=self.selected_service,
                            action=service_action
                        ).actions[service_action.name](*action_args, **action_kwargs)

                    raise NotImplementedError(f'No service template was found for service "{service_type}"'
                                              f' with version "{service_version}".')

                raise NotImplementedError(f'No service template was found for service "{service_type}".')

        raise ValueError(f'The "{action_name}" action is not available for the selected service.')
