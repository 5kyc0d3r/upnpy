from upnpy.soap.ServiceTemplates.__BaseTemplate import __BaseTemplate
from upnpy.soap import SOAP


class _BaseWANIPPPPConnection(__BaseTemplate):

    def __init__(self, service, action):
        super().__init__(service=service, action=action)

        self.actions = {
            'GetExternalIPAddress': self.get_external_ip_address
        }

    def set_connection_type(self):
        pass

    def get_connection_type_info(self):
        pass

    def configure_connection(self):
        pass

    def request_connection(self):
        pass

    def request_termination(self):
        pass

    def force_termination(self):
        pass

    def set_auto_disconnect_time(self):
        pass

    def set_idle_disconnect_time(self):
        pass

    def set_warn_disconnect_delay(self):
        pass

    def get_status_info(self):
        pass

    def get_link_layer_max_bit_rates(self):
        pass

    def get_ppp_encryption_protocol(self):
        pass

    def get_ppp_authentication_protocol(self):
        pass

    def get_username(self):
        pass

    def get_password(self):
        pass

    def get_auto_disconnect_time(self):
        pass

    def get_idle_disconnect_time(self):
        pass

    def get_warn_disconnect_delay(self):
        pass

    def get_nat_rsip_status(self):
        pass

    def get_generic_port_mapping_entry(self):
        pass

    def get_specific_port_mapping_entry(self):
        pass

    def add_port_mapping(self):
        pass

    def delete_port_mapping(self):
        pass

    def get_external_ip_address(self):
        return SOAP.send(service=self.service, action=self.action)
