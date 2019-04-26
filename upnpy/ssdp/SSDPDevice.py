from urllib.parse import urlparse
from xml.dom import minidom
from functools import wraps

import upnpy.utils as utils
from upnpy.ssdp import SSDPFilters
from upnpy.soap.ServiceTemplates import service_templates


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


class SSDPDevice:

    """
        **Represents an SSDP device**

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
        self.selected_service = None

    @_device_services_required
    def select_service(self, service):

        """
            **Select a service to use**

            Select a service to use available on the selected device.

            :param service: The service to select
            :type service: str, SSDPDevice.Service
            :return: True if selection was successful or raises a ValueError exception upon failure
            :rtype: bool
        """

        if type(service) == str:
            service = service
        elif type(service) == SSDPDevice.Service:
            service = service.service
        else:
            raise ValueError('Service must be either a str or SSDPDevice.Service object.')

        for device_service in self.get_services():
            if device_service.service == service:
                self.selected_service = device_service
                return True

        raise ValueError(f'The "{service}" service is not available for this device.')

    def get_selected_service(self):

        """
            **Get the selected service**

            Get the selected service for this device.

            :return: Return the currently selected service on this device
            :rtype: SSDPDevice.Service
        """

        if self.selected_service:
            return self.selected_service
        raise ValueError('No service has been selected.')

    @_device_description_required
    @_base_url_required
    def get_services(self):

        """
            **Get the services offered by the device**

            Gets a list of services available on the device.

            :return: List of services offered by the device
            :rtype: list
        """

        if not self.device_services:
            device_services = []
            root = minidom.parseString(self.device_description)

            for service in root.getElementsByTagName('service'):
                device_services.append(
                    self.Service(
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

    @staticmethod
    def filter_by(devices, **filters):

        """
            **Device filter**

            Filter out devices with specific parameters.

            :param devices: A list containing devices to filter
            :type devices: list
            :param filters: Specify filters (choose from ``host``, ``port``, ``headers``)
            :type filters: str, dict
            :return: List of filtered devices
            :rtype: list
        """

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

    class Service:

        """
            **Device service**

            Represents a service available on the device.

            :param service: Full service string (e.g.: ``urn:schemas-upnp-org:service:WANIPConnection:1``)
            :type service: str
            :param service_id: ID of the service
            :type service_id: str
            :param scpd_url: SCPD URL of the service
            :type scpd_url: str
            :param control_url: Control URL of the service
            :type control_url: str
            :param event_sub_url: Event Sub URL of the service
            :type event_sub_url: str
            :param base_url: Base URL of the service
            :type base_url: str
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
            self.actions = []
            self.description = None

        def get_type(self):

            """
                **Get the type of the service**

                Gets the <serviceType> portion of a full service string.

                :return: Service type
                :rtype: str
            """

            return self.service_type

        def get_version(self):

            """
                **Get the version of the service**

                Gets the <v> portion of a full service string.

                :return: Service version
                :rtype: int
            """

            return self.service_version

        def get_description(self):

            """
                **Get the description of the service**

                Gets the service description by sending a request to the SCPD URL of the service.

                :return: Service description
                :rtype: str
            """

            if self.description is None:
                service_description = utils.make_http_request(self.base_url + self.scpd_url).read()
                return service_description.decode()
            return self.description

        def get_actions(self):

            """
                **Get the service actions**

                Gets the actions available for the service.

                :return: List of actions available for the service
                :rtype: list
            """

            all_actions = []
            service_description = self.get_description()

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
                            self.Action.Argument(
                                argument_name, argument_direction, argument_return_value,
                                argument_related_state_variable
                            )
                        )

                all_actions.append(self.Action(action_name, action_arguments))

            return all_actions

        def execute(self, action, *action_args, **action_kwargs):

            """
                **Invoke an action for the selected service**

                Invokes an action for the current service.

                :param action: The action to invoke
                :type action: str, SOAPAction
                :param action_args: If the action requires parameters, pass them here
                :param action_kwargs: If the action requires parameters, pass them here
                :return: The response of the invoked action
                :rtype: dict
            """

            if type(action) == str:
                action_name = action
            elif type(action) == SSDPDevice.Service.Action:
                action_name = action.name
            else:
                raise ValueError('Action must be either a str or SSDPDevice.Service.Action object.')

            for service_action in self.get_actions():

                if service_action.name == action_name:
                    service_type = self.get_type()
                    service_version = self.get_version()

                    if service_type in service_templates.keys():
                        if service_version in service_templates[service_type].keys():
                            service_template = service_templates[service_type][service_version]
                            return service_template(
                                service=self,
                                action=service_action
                            ).actions[service_action.name](*action_args, **action_kwargs)

                        raise NotImplementedError(f'No service template was found for service "{service_type}"'
                                                  f' with version "{service_version}".')

                    raise NotImplementedError(f'No service template was found for service "{service_type}".')

            raise ValueError(f'The "{action_name}" action is not available for the selected service.')

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

        class Action:
            def __init__(self, name, argument_list):
                self.name = name
                self.arguments = argument_list

            class Argument:
                def __init__(self, name, direction, return_value, related_state_variable):
                    self.name = name
                    self.direction = direction
                    self.return_value = return_value
                    self.related_state_variable = related_state_variable
