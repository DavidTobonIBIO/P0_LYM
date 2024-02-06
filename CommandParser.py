from RobotParser import RobotParser
from VariableParser import VariableParser


class CommandsParser:
    def __init__(self, variableParser: VariableParser):
        self.simple_commands = ["MOVE", "SKIP", "TURN", "FACE"]
        self.commands = ["PUT", "PICK", "MOVE-DIR", "MOVE-FACE", "RUN-DIRS"]
        self.directions = [":FRONT", ":RIGHT", ":LEFT", ":BACK"]
        self.orientations = [":NORTH", ":SOUTH", ":EAST", ":WEST"]
        self.items = [":BALLOONS", ":CHIPS"]
        self.variableParser = variableParser

    def parse_action(self, line: str) -> bool:
        correct = True

        words = line.strip().split(" ")
        if len(words) < 3:
            correct = self.parse_simple_action_command(words)
        if len(words) >= 3:
            correct = self.parse_action_command(words)

        return correct

    def parse_simple_action_command(self, words: list[str]) -> bool:
        correct = False

        if words[0] == "NULL" and len(words) == 1:
            correct = True
        elif words[0] in ["MOVE", "SKIP"]:
            if (
                (words[1].isdigit())
                or (words[1] in self.variableParser.declared_variables)
                or (words[1] in RobotParser.CONSTANTS)
            ):
                correct = True
        elif (words[0] == "TURN") and (words[1] in self.directions):
            correct = True
        elif (words[0] == "FACE") and (words[1] in self.orientations):
            correct = True

        return correct

    def parse_action_command(self, words: list[str]) -> bool:
        correct = False

        if words[0] in ["PUT", "PICK"]:
            if (words[1] in self.items) and (
                (words[2].isdigit())
                or (words[2] in self.variableParser.declared_variables)
            ):
                correct = True
        if words[0] == "MOVE-DIR":
            if (
                words[1].isdigit() or words[1] in self.variableParser.declared_variables
            ) and (words[2] in self.directions):
                correct = True
        elif words[0] == "MOVE-FACE":
            if (
                words[1].isdigit() or words[1] in self.variableParser.declared_variables
            ) and (words[2] in self.orientations):
                correct = True
        elif words[0] == "RUN-DIRS":
            if all(d in self.directions for d in words[1:]):
                correct = True

        return correct
