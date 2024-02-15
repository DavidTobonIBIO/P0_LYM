from VariableParser import VariableParser
from constants import KEYWORDS, CONSTANTS

class FunctionParser:
    def __init__(self, variableParser: VariableParser):
        self.variableParser = variableParser

    def parse_declaraction(self, line: str) -> bool:
        correct = True
        words = line.strip().split(" ")

        if len(words) < 4:
            correct = False
        elif words[0] != "DEFUN":
            correct = False
        elif (words[1] in KEYWORDS) or (words[1] in CONSTANTS):
            correct = False
        elif words[2].startswith("(") and words[2].endswith(")"):
            params = words[2].split(",")

        return correct
