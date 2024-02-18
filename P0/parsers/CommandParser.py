from constants import CONSTANTS, ITEMS, ORIENTATIONS, RUN_DIRECTIONS, TURN_DIRECTIONS

class CommandParser:
    def __init__(self, variableParser):
        self.variableParser = variableParser

    def parse(self, words: list[str]) -> bool:
        correct = True
        if words[0] == '(':
            if len(words) <= 4:
                correct = self.parse_simple_action_command(words)
            elif len(words) == 5:
                correct = self.parse_action_command(words)
            elif len(words) >= 4:
                correct = self.parse_run_dirs_command(words)

        return correct

    def parse_simple_action_command(self, words: list[str]) -> bool:
        correct = False
        if (words[1] == "NULL") and (len(words) == 3):
            correct = True
            command_type = words[1]
            params = None
        elif words[3] == ')':
            if words[1] in ["MOVE", "SKIP"]:
                if (
                    (words[2].isdigit())
                    or (words[2] in self.variableParser.declared_variables)
                    or (words[2] in CONSTANTS)
                ):
                    correct = True
            elif (words[1] == "TURN") and (words[2] in TURN_DIRECTIONS):
                correct = True
            elif (words[1] == "FACE") and (words[2] in ORIENTATIONS):
                correct = True

        return correct

    def parse_action_command(self, words: list[str]) -> bool:
        correct = False
        if words[4] == ')':
            if words[1] in ["PUT", "PICK"]:
                if (words[2] in ITEMS) and (
                    (words[3].isdigit())
                    or (words[3] in self.variableParser.declared_variables or words[3] in CONSTANTS)
                ):
                    correct = True
            elif words[1] == "MOVE-DIR":
                if (
                    words[2].isdigit() or words[2] in self.variableParser.declared_variables
                ) and (words[3] in RUN_DIRECTIONS):
                    correct = True
            elif words[1] == "MOVE-FACE":
                if (
                    words[2].isdigit() or words[2] in self.variableParser.declared_variables
                ) and (words[3] in ORIENTATIONS):
                    correct = True
    
        return correct    
    
    def parse_run_dirs_command(self, words: list[str]) -> bool:
        correct = False
        if (words[-1] == ')') and (words[1] == "RUN-DIRS"):
            if all(d in RUN_DIRECTIONS for d in words[2:-1]):
                correct = True
        return correct
