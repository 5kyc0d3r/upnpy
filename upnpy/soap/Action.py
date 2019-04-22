class SOAPAction:
    def __init__(self, name, argument_list):
        self.name = name
        self.arguments = argument_list

    class Argument:
        def __init__(self, name, direction, return_value, related_state_variable):
            self.name = name
            self.direction = direction
            self.return_value = return_value
            self.related_state_variable = related_state_variable
