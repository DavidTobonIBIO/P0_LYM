import re
from instructions.Command import Command
from instructions.Conditional import Conditional
from instructions.FunctionDefinition import FunctionDefinition
from instructions.FunctionCall import FunctionCall
from instructions.Repeat import Repeat
from instructions.RepeatTimes import RepeatTimes
from instructions.VariableDefinition import VariableDefinition
from instructions.VariableAssignment import VariableAssignment

from parsers.CommandParser import CommandParser
from parsers.ConditionalParser import ConditionalParser
from parsers.VariableParser import VariableParser

from Block import Block
from constants import VALID_SYMBOLS, MOVE_COMMANDS
import os

class RobotParser:
    def __init__(self):
        self.variableParser = VariableParser()
        self.commandsParser = CommandParser(self.variableParser)
        self.conditionalParser = ConditionalParser(self.variableParser)
        
    def tokenize(self, program: str) -> list[str]:
        """
        Tokeniza la cadena de programa dada.

        Args:
            program (str): La cadena de programa a tokenizar.

        Returns:
            list[str]: Una lista de tokens extraídos de la cadena de programa.
        """
        self.tokens = re.findall(r"\(|\)|[^\s()]+", program.upper())
        return self.tokens
    
    def parse(self, program: str) -> bool:
        self.tokens: list[str] = self.tokenize(program)
        print(self.tokens)
        correct = False
        if self.tokens[0] == '(':
            stack = [0]
            instructions_list = []
            i = 1
            length = len(self.tokens)
            correct = True
            while correct and (i < length):
                if self.tokens[i] == '(':
                    stack.append(i)
                elif self.tokens[i] == ')':
                    start = stack.pop()
                    end = i
                # Bloque encontrado    
                if not stack:
                    block = Block('block')
                    if self.tokens[start+1] == '(':
                        block.addChild(self.parse(self.tokens[start:end+1]))
                    else:
                        correct, child = self.newChildParser(self, start, end)
                        if correct:
                            block.addChild(child)
                                    
                    instructions_list.append(block)
                i += 1
        print(instructions_list)
        return correct
    
    def newChildParser(self, start, end):
        keyword = start+1
        child = None
        if (self.tokens[keyword].isalnum()) or (self.tokens[keyword] in MOVE_COMMANDS):
            if self.isVariableDef(self.tokens[keyword]):
                words = self.tokens[start : end+1]
                correct, name, value = self.variableParser.parse_definition(words)
                if correct:
                    child = Block('defvar')
            elif self.isCommand(self.tokens[keyword]):
                correct, command_type, params = self.commandsParser.parse(self.tokens[start:end+1])
                if correct:
                    child = Block('command')
            elif self.isConditional(self.tokens[keyword]):
                pass
        elif (not self.tokens[keyword].isalnum()) and (self.tokens[keyword] in VALID_SYMBOLS):
            if self.isVariableAssignment(self.tokens[keyword]):
                words = self.tokens[start:end+1]
                correct, name, value = self.variableParser.parse_assignment(words)
                if correct:
                    child = Block('assignment')
                
        return correct, child
            
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
    file_name = input("Escribe la ruta del archivo: ")
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    if not file_path.endswith(".txt"):
        file_path += ".txt"

    try:
        with open(file_path, "r") as f:

            program = f.read()

            if RobotParser().parse(program):
                print("yes")
            else:
                print("no")
    except FileNotFoundError:
        print("No se encontró el archivo")


if __name__ == "__main__":
    main()
