from constants import KEYWORDS, CONSTANTS


class VariableParser:
    def __init__(self):
        self.valid_types: set = {bool, int}
        self.declared_variables: dict = {}

    def parse_declaraction(self, words: list[str]) -> bool:
        correct = True

        if len(words) != 5:
            correct = False
        elif (words[2] in KEYWORDS) or (words[2] in CONSTANTS) or (not words[2].isalnum()):
            correct = False
        elif (words[1] == "DEFVAR") and (type(words[3]) in self.valid_types) and (words[0] == '(' and words[-1] == ')'):
            self.declared_variables[words[2]] = self.set_variable_type(words[3])

        return correct

    def parse_assignment(self, words: list[str]) -> bool:
        correct = True

        if len(words) != 5:
            correct = False
        elif words[2] not in self.declared_variables:
            correct = False
        elif (words[1] == "=") and (type(words[3]) in self.valid_types) and (words[0] == '(' and words[-1] == ')'):
            self.declared_variables[words[2]] = words[3]

        return correct

    def set_variable_type(self, value: str) -> bool | int:
        if value.isdigit():
            return int(value)
        # if value.replace(".", "", 1).isdigit():
        #     return float(value)
        if value == "TRUE":
            return True
        if value == "FALSE":
            return False
        return value
    
# if __name__ == '__main__':
#     l = ['(', '=', 'XD1', '1', ')']
#     variableParser = VariableParser()
#     variableParser.declared_variables = {'XD1': 0}
#     print(variableParser.parse_assignment(l))
