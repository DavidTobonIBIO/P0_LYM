from RobotParser import RobotParser


class VariableParser:
    def __init__(self):
        self.valid_types: set = {bool, int}
        self.declared_variables: dict = {}

    def parse_declaraction(self, line: str) -> bool:
        correct = True
        words = line.strip().split(" ")

        if len(words) != 3:
            correct = False
        elif (words[1] in RobotParser.KEYWORDS) or (words[1] in RobotParser.CONSTANTS):
            correct = False
        elif (words[0] == "DEFVAR") and (type(words[2]) in self.valid_types):
            self.declared_variables[words[1]] = self.set_variable_type(words[2])

        return correct

    def parse_assignment(self, line: str) -> bool:
        correct = True
        words = line.strip().split(" ")

        if len(words) != 3:
            correct = False
        elif words[1] not in self.declared_variables:
            correct = False
        elif (words[0] == "=") and (type(words[2]) in self.valid_types):
            self.declared_variables[words[1]] = words[2]

        return correct

    def set_variable_type(self, value: str) -> bool | int | float | str:
        if value.isdigit():
            return int(value)
        if value.replace(".", "", 1).isdigit():
            return float(value)
        if value == "TRUE":
            return True
        if value == "FALSE":
            return False
        return value
