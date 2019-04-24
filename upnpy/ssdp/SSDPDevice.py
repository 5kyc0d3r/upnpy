from urllib.parse import urlparse
from xml.dom import minidom
from functools import wraps

import upnpy.utils as utils
from upnpy.ssdp import SSDPFilters
from upnpy.soap.Action import SOAPAction


def _device_description_required(func):

    """
    Decorator for retrieving the device description.
    """

    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        if instance.device_description is None:
            device_description_url = utils.parse_http_header(instance.response, 'Location')
            device_description = utils.make_http_request(device_description_url).read()
            instance.device_description = device_description.decode()
        return func(instance, *args, **kwargs)
    return wrapper


def _device_services_required(func):

    """
    Decorator for retrieving services provided by the device.
    """

    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        if not instance.device_services:
            instance.get_services()
        return func(instance, *args, **kwargs)
    return wrapper


def _base_url_required(func):

    """
    Decorator for constructing the BaseURL (from device response LOCATION header
    or <URLBase> element in device description).
    """

    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        if instance.base_url is None:
            location_header_value = utils.parse_http_header(instance.response, 'Location')
            root = minidom.parseString(instance.device_description)

            try:
                parsed_url = urlparse(root.getElementsByTagName('URLBase')[0].firstChild.nodeValue)
                base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
            except IndexError:
                parsed_url = urlparse(location_header_value)
                base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

            instance.base_url = base_url

        return func(instance, *args, **kwargs)
    return wrapper


class DeviceService:

    """
    Object for representing a device service.
    """

    def __init__(self, service, service_id, scpd_url, control_url, event_sub_url, base_url):
        self.service = service
        self.service_type = self._get_service_type(service)
        self.service_version = self._get_service_version(service)
        self.service_id = service_id
        self.scpd_url = scpd_url
        self.control_url = control_url
        self.event_sub_url = event_sub_url
        self.base_url = base_url

    @staticmethod
    def _get_service_type(service):

        """
        Parse the service type <serviceType> portion of the service.
        """

        return service.split(':')[3]

    @staticmethod
    def _get_service_version(service):

        """
        Parse the service version <v> portion of the service.
        """

        return int(service.split(':')[4])


class SSDPDevice:

    """
    Object for representing an SSDP device.

    :param address: SSDP device address
    :type address: tuple
    :param response: Device discovery response data
    :type response: str
    """

    def __init__(self, address, response):
        self.address = address
        self.host = address[0]
        self.port = address[1]
        self.response = response

        self.base_url = None
        self.device_description = None
        self.device_services = []
        self.soap_actions = []

    @_device_description_required
    @_base_url_required
    def get_services(self):

        """
        Get the services offered by the device.

        :return: List of services offered by the device
        :rtype: list
        """

        device_services = []
        root = minidom.parseString(self.device_description)

        for service in root.getElementsByTagName('service'):
            device_services.append(
                DeviceService(
                    service=service.getElementsByTagName('serviceType')[0].firstChild.nodeValue,
                    service_id=service.getElementsByTagName('serviceId')[0].firstChild.nodeValue,
                    scpd_url=service.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue,
                    control_url=service.getElementsByTagName('controlURL')[0].firstChild.nodeValue,
                    event_sub_url=service.getElementsByTagName('eventSubURL')[0].firstChild.nodeValue,
                    base_url=self.base_url
                )
            )

        self.device_services = device_services
        return self.device_services

    def get_service_description(self, service_type):

        """
        Get the description of the specified service.

        :param service_type:
        :return: Service description
        :rtype: str
        """

        # TODO: Allow passing a DeviceService object instead of just the service type

        for service in self.device_services:

            if service_type == service.service:
                service_description = utils.make_http_request(service.base_url + service.scpd_url).read()
                return service_description.decode()

        raise ValueError(f'No service found with service type "{service_type}".')

    def get_actions(self, service_type):

        """
        Get the actions available for the specified service.

        :param service_type:
        :return: List of actions available for the specified service
        :rtype: list
        """

        all_actions = []
        service_description = self.get_service_description(service_type)

        root = minidom.parseString(service_description)
        actions = root.getElementsByTagName('action')

        for action in actions:
            action_name = action.getElementsByTagName('name')[0].firstChild.nodeValue
            action_arguments = []

            # An action's argument list is only required if the action has parameters according to UPnP spec
            try:
                action_argument_list = action.getElementsByTagName('argumentList')[0]
            except IndexError:
                action_argument_list = None

            if action_argument_list:
                action_arguments_elements = action_argument_list.getElementsByTagName('argument')

                for argument in action_arguments_elements:
                    argument_name = argument.getElementsByTagName('name')[0].firstChild.nodeValue
                    argument_direction = argument.getElementsByTagName('direction')[0].firstChild.nodeValue

                    # Argument return value is optional according to UPnP spec
                    try:
                        argument_return_value = argument.getElementsByTagName('retval')[0].firstChild.nodeValue
                    except IndexError:
                        argument_return_value = None

                    argument_related_state_variable = argument.getElementsByTagName(
                        'relatedStateVariable'
                    )[0].firstChild.nodeValue

                    action_arguments.append(
                        SOAPAction.Argument(
                            argument_name, argument_direction, argument_return_value, argument_related_state_variable
                        )
                    )

            all_actions.append(SOAPAction(action_name, action_arguments))

        return all_actions

    @staticmethod
    def filter_by(devices, **filters):

        filtered_devices = {}
        enabled_filters = [filter_ for filter_ in filters]
        final_filtered_devices = []

        for device in devices:
            filtered_devices[device] = {'successful_filters': []}

            for user_filter, user_filter_value in filters.items():

                if user_filter == 'host':
                    if SSDPFilters.host_filter(device, host=user_filter_value):
                        filtered_devices[device]['successful_filters'].append(user_filter)
                        continue

                elif user_filter == 'port':
                    if SSDPFilters.port_filter(device, port=user_filter_value):
                        filtered_devices[device]['successful_filters'].append(user_filter)
                        continue

                elif user_filter == 'headers':
                    if SSDPFilters.header_filter(device, headers=user_filter_value):
                        filtered_devices[device]['successful_filters'].append(user_filter)
                        continue

                else:
                    raise KeyError(f'Unknown filter "{user_filter}".')

            filters_successful_on_device = all(
                enabled_filter in filtered_devices[device]['successful_filters'] for enabled_filter in enabled_filters
            )

            if filters_successful_on_device:
                final_filtered_devices.append(device)

        return final_filtered_devices
