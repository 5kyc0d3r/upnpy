from upnpy.ssdp.SSDPRequest import SSDPRequest
from upnpy.ssdp.SSDPDevice import SSDPDevice


class UPnP:
    def __init__(self):
        self.ssdp = SSDPRequest()
        self.devices = []
        self.selected_device = None

    def discover(self, delay=2, **headers):
        for device in self.ssdp.m_search(discover_delay=delay, **headers):
            self.devices.append(device)

    def select_igd(self):
        device_filter = SSDPDevice.filter_by(
            self.devices,
            headers={'ST': 'urn:schemas-upnp-org:device:InternetGatewayDevice:1'}
        )

        device_filter_length = len(device_filter)

        if device_filter_length == 1:
            igd = device_filter[0]
            self.selected_device = igd

        elif device_filter_length > 1:
            raise ValueError('Multiple IGDs found.')

        else:
            raise ValueError('No IGDs found.')
