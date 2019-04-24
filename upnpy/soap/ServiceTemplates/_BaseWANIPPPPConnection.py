from upnpy.soap.ServiceTemplates.__BaseTemplate import __BaseTemplate
from upnpy.soap import SOAP


class _BaseWANIPPPPConnection(__BaseTemplate):

    def __init__(self, service, action):
        super().__init__(service=service, action=action)

        self.actions = {
            'SetConnectionType': self.set_connection_type,
            'GetConnectionTypeInfo': self.get_connection_type_info,
            'AddPortMapping': self.add_port_mapping,
            'DeletePortMapping': self.delete_port_mapping,
            'GetExternalIPAddress': self.get_external_ip_address
        }

    def set_connection_type(self, new_connection_type):

        """
        This action sets the connection to a specific type.
        SetConnectionType depends on the PossibleConnectionTypes state variable.
        :param new_connection_type:
        :return: Action response
        :rtype: dict
        """

        return SOAP.send(
            self.service, self.action,
            NewConnectionType=new_connection_type
        )

    def get_connection_type_info(self):

        """
        This action retrieves the values of the current connection type and allowable connection types.
        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

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

    def add_port_mapping(self, new_external_port, new_protocol, new_internal_port, new_internal_client,
                         new_port_mapping_description, new_enabled=1, new_lease_duration=0, new_remote_host=''):
        return SOAP.send(
            self.service, self.action,
            NewRemoteHost=new_remote_host,
            NewExternalPort=new_external_port,
            NewProtocol=new_protocol,
            NewInternalPort=new_internal_port,
            NewInternalClient=new_internal_client,
            NewEnabled=new_enabled,
            NewPortMappingDescription=new_port_mapping_description,
            NewLeaseDuration=new_lease_duration
        )

    def delete_port_mapping(self, new_external_port, new_protocol, new_remote_host=''):
        return SOAP.send(
            self.service, self.action,
            NewRemoteHost=new_remote_host,
            NewExternalPort=new_external_port,
            NewProtocol=new_protocol
        )

    def get_external_ip_address(self):
        return SOAP.send(service=self.service, action=self.action)
