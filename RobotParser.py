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
        ##self.functionParser = FunctionParser(self.variableParser, self.commandsParser)

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
        if self.parenthesisParser.parse(tokens) and tokens[0] == '(':
            correct = True
            stack = [tokens[0]]
            i = 1
            length = len(tokens)
            while correct and (i < length):
                if tokens[i] == '(':
                    stack.append(i)
                elif tokens[i] == ')':
                    start = stack.pop()+1
                    end = i
                    if (not (tokens[start] == '(')) and (not (tokens[start] == ')')):
                        if (tokens[start].isalnum()) or (tokens[start] in MOVE_COMMANDS):
                            if self.isVariableDef(tokens[start]):
                                words = tokens[start - 1 : end+1]
                                correct = self.variableParser.parse_definition(words)
                                
                            elif self.isCommand(tokens[start]):
                                print(tokens[start])
                                correct = self.commandsParser.parse_action(tokens[start-1:end+1])
                            
                        
                        
            
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
