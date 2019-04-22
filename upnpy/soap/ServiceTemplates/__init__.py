from upnpy.soap.ServiceTemplates import WANIPConnection, WANPPPConnection

service_templates = {
    'WANIPConnection': {
        1: WANIPConnection.WANIPConnection
    },
    'WANPPPConnection': {
        1: WANPPPConnection.WANPPPConnection
    }
}
