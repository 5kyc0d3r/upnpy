class SOAPError(Exception):
    def __init__(self, description, code):
        self.description = description
        self.error = code
