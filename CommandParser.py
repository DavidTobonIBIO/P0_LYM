from VariableParser import VariableParser
from constants import CONSTANTS, ITEMS, ORIENTATIONS

class CommandParser:
    def __init__(self, variableParser: VariableParser):
        self.simple_commands = ["MOVE", "SKIP", "TURN", "FACE"]
        self.commands = ["PUT", "PICK", "MOVE-DIR", "MOVE-FACE", "RUN-DIRS"]
        self.run_directions = [":FRONT", ":RIGHT", ":LEFT", ":BACK"]
        self.turn_directions = [":LEFT", ":RIGHT", ":AROUND"]
        self.variableParser = variableParser

    def parse_action(self, words: list[str]) -> bool:
        correct = True
        if len(words) <= 4:
            correct = self.parse_simple_action_command(words)
        elif len(words) == 5:
            correct = self.parse_action_command(words)
        elif len(words) >= 4:
            correct = self.parse_run_dirs_command(words)

        return correct

    def parse_simple_action_command(self, words: list[str]) -> bool:
        correct = False

        if words[1] == "NULL" and len(words) == 3:
            correct = True
        elif (words[0] == '(') and (words[3] == ')'):
            if words[1] in ["MOVE", "SKIP"]:
                if (
                    (words[2].isdigit())
                    or (words[2] in self.variableParser.declared_variables)
                    or (words[2] in CONSTANTS)
                ):
                    correct = True
            elif (words[1] == "TURN") and (words[2] in self.turn_directions):
                correct = True
            elif (words[1] == "FACE") and (words[2] in ORIENTATIONS):
                correct = True

        return correct

    def parse_action_command(self, words: list[str]) -> bool:
        correct = False
        if (words[0] == '(') and (words[4] == ')'):
            if words[1] in ["PUT", "PICK"]:
                if (words[2] in ITEMS) and (
                    (words[3].isdigit())
                    or (words[3] in self.variableParser.declared_variables)
                ):
                    correct = True
            if words[1] == "MOVE-DIR":
                if (
                    words[2].isdigit() or words[2] in self.variableParser.declared_variables
                ) and (words[3] in self.run_directions):
                    correct = True
            elif words[1] == "MOVE-FACE":
                if (
                    words[2].isdigit() or words[2] in self.variableParser.declared_variables
                ) and (words[3] in self.orientations):
                    correct = True
    
        return correct
    
    
    def parse_run_dirs_command(self, words: list[str]) -> bool:
        correct = False
        if (words[0] == '(') and (words[-1] == ')') and (words[1] == "RUN-DIRS"):
            if all(d in self.run_directions for d in words[2:-1]):
                correct = True
        return correct
