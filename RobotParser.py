import re
from VariableParser import VariableParser
from FunctionParser import FunctionParser
from CommandParser import CommandParser
from ConditionalParser import ConditionalParser
from ParenthesisParser import ParenthesisParser
from constants import VALID_SYMBOLS, MOVE_COMMANDS


class RobotParser:

    VALID_TYPES: set = {bool, int}

    def __init__(self) -> None:
        self.parenthesisParser = ParenthesisParser()
        self.variableParser = VariableParser()
        self.commandsParser = CommandParser(self.variableParser)
        self.conditionalParser = ConditionalParser(self.variableParser)
        self.functionParser = FunctionParser(self.variableParser, self.commandsParser)

    def tokenize(self, program: str) -> list[str]:
        """
        Tokeniza la cadena de programa dada.

        Args:
            program (str): La cadena de programa a tokenizar.

        Returns:
            list[str]: Una lista de tokens extraídos de la cadena de programa.
        """
        tokens = re.findall(r"\(|\)|[^\s()]+", program.upper())
        return tokens

    def parse(self, program: str) -> bool:
        tokens: list[str] = self.tokenize(program)
        print(tokens)
        correct = False
        if self.parenthesisParser.parse(tokens):
            correct = True
            i = 0
            
            while correct and (i < len(tokens)):
                if (tokens[i].isalnum()) or (tokens[i] in MOVE_COMMANDS):
                    if self.isVariableDef(tokens[i]):
                        words = tokens[i - 1 : i + 4]
                        correct = self.variableParser.parse_definition(words)
                        i += 4
                        
                    elif self.isCommand(tokens[i]):
                        j = i
                        while tokens[j] != ')':
                            j += 1
                        correct = self.commandsParser.parse_action(tokens[i-1:j+1])
                        i += j+1
                    elif self.isConditional(tokens[i]):
                        j = i
                        while tokens[j] != ')':
                            j += 1
                        correct = self.conditionalParser.parse(tokens[i-1:j+1])
                        i += j+1
                    # elif self.isFunction(tokens[i]):
                    #     correct = self.functionParser.parse_definition()

                elif (not tokens[i].isalnum()) and (tokens[i] in VALID_SYMBOLS):
                    if self.isVariableAssignment(tokens[i]):
                        words = tokens[i-1:i+4]
                        correct = self.variableParser.parse_assignment(words)
                        i += 4
                    else:
                        correct = False
                i += 1
        return correct

    def isVariableDef(self, word):
        if word == "DEFVAR":
            return True
        return False

    def isVariableAssignment(self, word):
        if word == "=":
            return True
        return False

    def isCommand(self, word):
        if word in MOVE_COMMANDS:
            return True
        return False
    
    def isConditional(self, word):
        if word == 'IF':
            return True
        return False
    
    def isFunction(self, word):
        if word == "DEFUN":
            return True
        return False


def main():

    file = input("Escribe la ruta del archivo: ")
    if not file.endswith(".txt"):
        file += ".txt"

    try:
        with open(file, "r") as f:

            program = f.read()

            if RobotParser().parse(program):
                print("yes")
            else:
                print("no")
    except FileNotFoundError:
        print("No se encontró el archivo")


if __name__ == "__main__":
    main()
