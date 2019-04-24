from unittest import TestCase
from upnpy.ssdp.SSDPDevice import SSDPDevice, DeviceService

with open('tests/xml/device_templates/TestDevice.xml') as xml_file:
    xml = xml_file.read()


class TestSSDPDevice(TestCase):
    def test_get_services(self):
        device = SSDPDevice(('192.168.1.1', 5431), xml)
        device.device_description = xml
        device_services = device.get_services()

        target_services = [
            DeviceService(
                'urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1',
                'urn:upnp-org:serviceId:WANCommonInterfaceConfig.1',
                '/dynsvc/WANCommonInterfaceConfig:1.xml',
                '/uuid:c8d12a3b-22a7-a722-3b2a-d1c8d13ba70001/WANCommonInterfaceConfig:1',
                '/uuid:c8d12a3b-22a7-a722-3b2a-d1c8d13ba70001/WANCommonInterfaceConfig:1',
                'http://192.168.1.1:5431'
            ),

            DeviceService(
                'urn:schemas-upnp-org:service:WANPPPConnection:1',
                'urn:upnp-org:serviceId:WANPPPConnection.1',
                '/dynsvc/WANPPPConnection:1.xml',
                '/uuid:c8d12a3b-22a7-a722-3b2a-d1c8d13ba70002/WANPPPConnection:1',
                '/uuid:c8d12a3b-22a7-a722-3b2a-d1c8d13ba70002/WANPPPConnection:1',
                'http://192.168.1.1:5431'
            )
        ]

        for device_service, target_service in zip(device_services, target_services):
            self.assertEqual(device_service.service, target_service.service)
            self.assertEqual(device_service.service_type, target_service.service_type)
            self.assertEqual(device_service.service_version, target_service.service_version)
            self.assertEqual(device_service.service_id, target_service.service_id)
            self.assertEqual(device_service.scpd_url, target_service.scpd_url)
            self.assertEqual(device_service.control_url, target_service.control_url)
            self.assertEqual(device_service.event_sub_url, target_service.event_sub_url)
            self.assertEqual(device_service.base_url, target_service.base_url)
