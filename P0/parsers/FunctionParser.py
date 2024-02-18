from instructions.Function import Function
from constants import KEYWORDS, CONSTANTS

class FunctionParser:
    def __init__(self, variableParser):
        self.variableParser = variableParser
        self.functions: dict[str, Function] = {}

    def parse_definition(self, words: list[str]) -> bool:
        correct = True

        if len(words) < 6:
            correct = False
        if (words[0] == '(') and (words[-1] == ')'):
            if words[1] != "DEFUN":
                correct = False
            elif (words[2] in KEYWORDS) or (words[2] in CONSTANTS) or (words[2] in self.variableParser.declared_variables):
                correct = False
            elif (words[3] == "("):
                func_name = words[2]
                i = 4
                params = []
                while (i < len(words)) and (words[i] != ')'):
                    params.append(words[i])
                    i += 1
                    
                self.functions[func_name] = Function(func_name, params)

        return correct
    
    def parse_call(self, words: list[str]) -> bool:
        correct = True
        if (words[0] == '(') and (words[-1] == ')'):
            if words[1] in self.functions:
                correct = len(self.functions[words[1]].params) == len(words[2:-1])
            else:
                correct = False
        else:
            correct = False
        return correct
