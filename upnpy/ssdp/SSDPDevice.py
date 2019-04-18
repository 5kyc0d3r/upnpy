import urllib.request
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

    def get_device_description(self):
        device_description_url = utils.parse_http_header(self.response, 'Location')
        device_description = urllib.request.urlopen(device_description_url).read()
        self.device_description = device_description.decode()
        return self.device_description

    def get_device_services(self):
        while True:
            if self.device_description:
                root = minidom.parseString(self.device_description)

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
            else:
                self.get_device_description()
                continue

            break

        return self.device_services

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
