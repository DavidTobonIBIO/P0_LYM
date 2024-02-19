from constants import CONDITIONALS, ITEMS, ORIENTATIONS, CONSTANTS


class ConditionalParser:
    def __init__(self, variableParser):
        self.variableParser = variableParser

    def parse(self, words: list[str]) -> tuple:
        if (words[0] == "("):
            if words[1] in CONDITIONALS:
                if words[1] == "NOT":
                    if (words[2] == '('):
                        if self.check_facing_and_can_move(words[3:]):
                            return (words[5] == ')') and (words[6] == ')')
                        elif self.check_can_put_can_pick(words[3:]):
                            return (words[6] == ')') and (words[7] == ')')
                        elif self.check_blocked(words[3:]):
                            return (words[4] == ')') and (words[5] == ')')
                        elif self.check_is_zero(words[3:]):
                            return (words[5] == ')') and (words[6] == ')')
                else:
                    if self.check_facing_and_can_move((words[1:])):
                        return words[3] == ')'
                    if self.check_can_put_can_pick(words[1:]):
                        return words[4] == ')'
                    elif self.check_blocked(words[1:]):
                        return words[2] == ')'
                    elif self.check_is_zero(words[1:]):
                        return words[3] == ')'
        return False

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
                (words[1].isdigit())
                or (words[1] in self.variableParser.declared_variables)
                or (words[1] in CONSTANTS)
            )
        
    
