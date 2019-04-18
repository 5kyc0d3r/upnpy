import urllib.request
import upnpy.utils as utils
from upnpy.ssdp import SSDPFilters


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

    def get_device_description(self):
        device_description_url = utils.parse_http_header(self.response, 'Location')
        device_description = urllib.request.urlopen(device_description_url).read()
        self.device_description = device_description.decode()
        return self.device_description

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
