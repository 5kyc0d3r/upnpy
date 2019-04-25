class SOAPError(Exception):

    """
        **Custom SOAP exception**

        Custom SOAP exception class.
        Raised whenever an error response has been received during action invocation.
    """

    def __init__(self, description, code):
        self.description = description
        self.error = code
