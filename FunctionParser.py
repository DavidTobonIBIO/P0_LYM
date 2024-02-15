from VariableParser import VariableParser
from Function import Function
from constants import KEYWORDS, CONSTANTS

class FunctionParser:
    def __init__(self, variableParser: VariableParser):
        self.variableParser = variableParser
        self.functions: dict[str, list[str]] = {}

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
                fun_name = words[2]
                j = 4
                params = []
                while (j < len(words)) and (words[j] != ')'):
                    params.append(words[j])
                    j += 1
                    
                self.functions[fun_name] = params

        return correct
