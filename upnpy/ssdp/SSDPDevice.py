from urllib.parse import urlparse
from xml.dom import minidom

import upnpy.utils as utils
from upnpy.ssdp import SSDPFilters


class DeviceService:
    def __init__(self, service_type, service_id, scpd_url, control_url, event_sub_url):
        self.service_type = service_type
        self.service_id = service_id
        self.scpd_url = scpd_url
        self.control_url = control_url
        self.event_sub_url = event_sub_url


class SSDPDevice:

    """

    SSDP device data

    :param address: SSDP device address
    :type address: tuple

    """

    def __init__(self, address, response):
        self.address = address
        self.host = address[0]
        self.port = address[1]
        self.response = response

        self.device_description = None
        self.device_services = []

    def _check_device_description(self):
        while True:
            if self.device_description is not None:
                return True
            else:
                device_description_url = utils.parse_http_header(self.response, 'Location')
                device_description = utils.make_http_request(device_description_url).read()
                self.device_description = device_description.decode()
                continue

    def get_description(self):
        if self._check_device_description():
            return self.device_description

    def get_services(self):
        device_description = self.get_description()
        root = minidom.parseString(device_description)

        for service in root.getElementsByTagName('service'):
            self.device_services.append(
                DeviceService(
                    service_type=service.getElementsByTagName('serviceType')[0].firstChild.nodeValue,
                    service_id=service.getElementsByTagName('serviceId')[0].firstChild.nodeValue,
                    scpd_url=service.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue,
                    control_url=service.getElementsByTagName('controlURL')[0].firstChild.nodeValue,
                    event_sub_url=service.getElementsByTagName('eventSubURL')[0].firstChild.nodeValue
                )
            )

        return self.device_services

    def get_service_description(self, service_type):

        # Construct the BaseURL (from device response LOCATION header or <URLBase> element in device description)

        device_description = self.get_description()
        location_header_value = utils.parse_http_header(self.response, 'Location')

        root = minidom.parseString(device_description)

        try:
            base_url = root.getElementsByTagName('URLBase')[0].firstChild.nodeValue
        except IndexError:
            parsed_url = urlparse(location_header_value)
            base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

        for service in self.device_services:

            if service_type == service.service_type:
                service_description = utils.make_http_request(base_url + service.scpd_url).read()
                return service_description.decode()

        raise ValueError(f'No service found with service type "{service_type}".')

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
