from constants import CONDITIONALS, ITEMS, ORIENTATIONS, CONSTANTS
from VariableParser import VariableParser


class ConditionalParser:
    def __init__(self, variableParser: VariableParser) -> None:
        self.variableParser = variableParser

    def parse(self, words: list[str]) -> bool:
        if (words[0] == "(") and (words[-1] == ")"):
            if words[2] in CONDITIONALS:
                if words[2] == "NOT":
                    return (
                        self.check_facing_and_can_move(words[3:])
                        or self.check_can_put_can_pick(words[3:])
                        or self.check_blocked(words[3:])
                        or self.check_is_zero(words[3:])
                    )
                else:
                    return (
                        self.check_facing_and_can_move((words[2:]))
                        or self.check_can_put_can_pick(words[2:])
                        or self.check_blocked(words[2:])
                        or self.check_is_zero(words[2:])
                    )

    def check_facing_and_can_move(self, words):
        return ((words[0] == "FACING?") or (words[0] == "CAN-MOVE?")) and (
            words[1] in ORIENTATIONS
        )

    def check_can_put_can_pick(self, words):
        return (
            ((words[0] == "CAN-PUT?") or (words[0] == "CAN-PICK?"))
            and (words[1] in ITEMS)
            and (
                (words[2].isdigit())
                or (words[2] in self.variableParser.declared_variables)
                or (words[2] in CONSTANTS)
            )
        )

    def check_blocked(self, words):
        return words[0] == 'BLOCKED?'

    def check_is_zero(self, words):
        return (words[0] == 'ISZERO?') and (
                (words[2].isdigit())
                or (words[2] in self.variableParser.declared_variables)
                or (words[2] in CONSTANTS)
            )
        
    
