from constants import CONSTANTS

class RepeatParser:
    def __init__(self, variableParser):
        self.variableParser = variableParser
        
    def parse(self, words: list[str]) -> tuple:
        if words[0] == "(":
            if words[1] == "REPEAT":
                if (words[2].isdigit()) or (words[2] in self.variableParser.declared_variables) or (words[2] in CONSTANTS):
                    return words[-1] == ")"

        return False