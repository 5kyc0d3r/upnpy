from upnpy.soap.ServiceTemplates.__BaseTemplate import __BaseTemplate
from upnpy.soap import SOAP


class _BaseWANIPPPPConnection(__BaseTemplate):

    def __init__(self, service, action):
        super().__init__(service=service, action=action)

        self.actions = {
            'SetConnectionType': self.set_connection_type,
            'GetConnectionTypeInfo': self.get_connection_type_info,
            'ConfigureConnection': self.configure_connection,
            'RequestConnection': self.request_connection,
            'RequestTermination': self.request_termination,
            'ForceTermination': self.force_termination,
            'SetAutoDisconnectTime': self.set_auto_disconnect_time,
            'SetIdleDisconnectTime': self.set_idle_disconnect_time,
            'SetWarnDisconnectDelay': self.set_warn_disconnect_delay,
            'GetStatusInfo': self.get_status_info,
            'GetLinkLayerMaxBitRates': self.get_link_layer_max_bit_rates,
            'GetPPPEncryptionProtocol': self.get_ppp_encryption_protocol,
            'GetPPPCompressionProtocol': self.get_ppp_compression_protocol,
            'GetPPPAuthenticationProtocol': self.get_ppp_authentication_protocol,
            'GetUsername': self.get_username,
            'GetPassword': self.get_password,
            'GetAutoDisconnectTime': self.get_auto_disconnect_time,
            'GetIdleDisconnectTime': self.get_idle_disconnect_time,
            'GetWarnDisconnectDelay': self.get_warn_disconnect_delay,
            'GetNATRSIPStatus': self.get_nat_rsip_status,
            'GetGenericPortMappingEntry': self.get_generic_port_mapping_entry,
            'GetSpecificPortMappingEntry': self.get_specific_port_mapping_entry,
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

    def configure_connection(self, new_username, new_password):

        """
        A client may send this command to configure a PPP connection on the WAN device and change
        ConnectionStatus to Disconnected from Unconfigured. By doing so, the client is implicitly
        allowing any other client in the residential network to initiate a connection using this configuration.
        The client may choose an instance of a connection service in the Unconfigured state and
        configure it, or change an existing configuration on a Disconnected connection. By passing NULL
        values for the parameters, this command may also be used to set the ConnectionStatus from
        Disconnected to Unconfigured.
        NOTE: Gateway implementations may choose to keep sensitive information such as Password
        from being read by a client.

        :param new_username:
        :param new_password:
        :return: Action response
        :rtype: dict
        """

        return SOAP.send(
            self.service, self.action,
            NewUsername=new_username,
            NewPassword=new_password
        )

    def request_connection(self):

        """
        A client sends this action to initiate a connection on an instance of a connection service that has
        a configuration already defined. RequestConnection causes the ConnectionStatus to
        immediately change to Connecting (if implemented) unless the action is not permitted in the
        current state of the IGD or the specific service instance. This change of state will be evented.
        RequestConnection should synchronously return at this time in accordance with UPnP
        architecture requirements that mandate that an action can take no more than 30 seconds to
        respond synchronously. However, the actual connection setup may take several seconds more to
        complete. For example, in the case of POTS dial-up connections, the RequestConnection
        action may trigger the IGD to dial several previously configured phone numbers in sequence and
        report a failure only if all connection attempts fail. If the connection setup is successful,
        ConnectionStatus will change to Connected and will be evented. If the connection setup is
        not successful, ConnectionStatus will eventually revert back to Disconnected and will be
        evented. LastConnectionError will be set appropriately in either case. While this may be
        obvious, it is worth noting that a control point must not source packets to the Internet until
        ConnectionStatus is updated to Connected, or the IGD may drop packets until it transitions
        to the Connected state.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def request_termination(self):

        """
        A client may send this command to any connection instance in Connected, Connecting or
        Authenticating state to change ConnectionStatus to Disconnected. Connection state changes
        to PendingDisconnect depending on the value of WarnDisconnectDelay variable. Connection
        termination will depend on whether other clients intend to continue to use the connection.
        If successful, ConnectionStatus is changed to Disconnected.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def force_termination(self):

        """
        A client may send this command to any connection instance in Connected, Connecting,
        Authenticating, PendingDisconnect or Disconnecting state to change ConnectionStatus to
        Disconnected. Connection state immediately transitions to Disconnected irrespective of the
        setting of WarnDisconnectDelay variable.
        If successful, ConnectionStatus is changed to Disconnected.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def set_auto_disconnect_time(self, new_auto_disconnect_time):

        """
        This action sets the time (in seconds) after which an active connection is automatically
        disconnected.

        :param new_auto_disconnect_time:
        :return: Action response
        :rtype: dict
        """

        return SOAP.send(
            self.service, self.action,
            NewAutoDisconnectTime=new_auto_disconnect_time
        )

    def set_idle_disconnect_time(self, new_idle_disconnect_time):

        """
        This action specifies the idle time (in seconds) after which a connection may be disconnected.
        The actual disconnect will occur after WarnDisconnectDelay time elapses.

        :param new_idle_disconnect_time:
        :return: Action response
        :rtype: dict
        """

        return SOAP.send(
            self.service, self.action,
            NewIdleDisconnectTime=new_idle_disconnect_time
        )

    def set_warn_disconnect_delay(self, new_warn_disconnect_delay):

        """
        This action specifies the number of seconds of warning to each (potentially) active user of a
        connection before a connection is terminated.

        :param new_warn_disconnect_delay:
        :return: Action response
        :rtype: dict
        """

        return SOAP.send(
            self.service, self.action,
            NewWarnDisconnectDelay=new_warn_disconnect_delay
        )

    def get_status_info(self):

        """
        This action retrieves the values of state variables pertaining to connection status.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_link_layer_max_bit_rates(self):

        """
        This action retrieves the maximum upstream and downstream bit rates for the connection.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_ppp_encryption_protocol(self):

        """
        This action retrieves the link layer (PPP) encryption protocol used for this connection.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_ppp_compression_protocol(self):

        """
        This action retrieves the link layer (PPP) compression protocol used for this connection.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_ppp_authentication_protocol(self):

        """
        This action retrieves the link layer (PPP) authentication protocol for this connection.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_username(self):

        """
        This action retrieves the user name used for the activation of a connection.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_password(self):

        """
        This action retrieves the password used for the activation of a connection.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_auto_disconnect_time(self):

        """
        This action retrieves the time (in seconds) after which an active connection is automatically
        disconnected.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_idle_disconnect_time(self):

        """
        This action retrieves the idle time (in seconds) after which a connection may be disconnected.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_warn_disconnect_delay(self):

        """
        This action retrieves the number of seconds of warning to each (potentially) active user of a
        connection before a connection is terminated.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_nat_rsip_status(self):

        """
        This action retrieves the current state of NAT and RSIP on the gateway for this connection.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(self.service, self.action)

    def get_generic_port_mapping_entry(self, new_port_mapping_index):

        """
        This action retrieves NAT port mappings one entry at a time. Control points can call this action
        with an incrementing array index until no more entries are found on the gateway. If
        PortMappingNumberOfEntries is updated during a call, the process may have to start over.
        Entries in the array are contiguous. As entries are deleted, the array is compacted, and the
        evented variable PortMappingNumberOfEntries is decremented. Port mappings are logically
        stored as an array on the IGD and retrieved using an array index ranging from 0 to
        PortMappingNumberOfEntries-1.

        :param new_port_mapping_index:
        :return: Action response
        :rtype: dict
        """

        return SOAP.send(
            self.service, self.action,
            NewPortMappingIndex=new_port_mapping_index
        )

    def get_specific_port_mapping_entry(self, new_external_port, new_protocol, new_remote_host=''):

        """
        This action reports the Static Port Mapping specified by the unique tuple of RemoteHost,
        ExternalPort and PortMappingProtocol.

        :param new_external_port:
        :param new_protocol:
        :param new_remote_host:
        :return: Action response
        :rtype: dict
        """

        return SOAP.send(
            self.service, self.action,
            NewRemoteHost=new_remote_host,
            NewExternalPort=new_external_port,
            NewProtocol=new_protocol
        )

    def add_port_mapping(self, new_external_port, new_protocol, new_internal_port, new_internal_client,
                         new_port_mapping_description, new_enabled=1, new_lease_duration=0, new_remote_host=''):

        """
        This action creates a new port mapping or overwrites an existing mapping with the same internal
        client. If the ExternalPort and PortMappingProtocol pair is already mapped to another
        internal client, an error is returned.

        NOTE: Not all NAT implementations will support:
          * Wildcard value (i.e. 0) for ExternalPort
          * InternalPort values that are different from ExternalPort
          * Dynamic port mappings i.e. with non-Infinite PortMappingLeaseDuration

        :param new_external_port:
        :param new_protocol:
        :param new_internal_port:
        :param new_internal_client:
        :param new_port_mapping_description:
        :param new_enabled:
        :param new_lease_duration:
        :param new_remote_host:
        :return: Action response
        :rtype: dict
        """

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

        """
        This action deletes a previously instantiated port mapping. As each entry is deleted, the array is
        compacted, and the evented variable PortMappingNumberOfEntries is decremented.

        :param new_external_port:
        :param new_protocol:
        :param new_remote_host:
        :return: Action response
        :rtype: dict
        """

        return SOAP.send(
            self.service, self.action,
            NewRemoteHost=new_remote_host,
            NewExternalPort=new_external_port,
            NewProtocol=new_protocol
        )

    def get_external_ip_address(self):

        """
        This action retrieves the value of the external IP address on this connection instance.

        :return: Action response
        :rtype: dict
        """

        return SOAP.send(service=self.service, action=self.action)
