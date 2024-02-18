import re
from VariableParser import VariableParser
from FunctionParser import FunctionParser
from CommandParser import CommandParser
from ConditionalParser import ConditionalParser
from ParenthesisParser import ParenthesisParser
from constants import VALID_SYMBOLS, MOVE_COMMANDS
import os


class RobotParser:
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
        self.tokens = re.findall(r"\(|\)|[^\s()]+", program.upper())
        return self.tokens

    def parse(self, program: str) -> bool:
        self.tokens: list[str] = self.tokenize(program)
        print(self.tokens)
        correct = False
        if self.parenthesisParser.parse(self.tokens) and self.tokens[0] == '(':
            correct = True
            stack = [0]
            i = 1
            length = len(self.tokens)
            while correct and (i < length):
                if self.tokens[i] == '(':
                    stack.append(i)
                    i += 1
                elif self.tokens[i] == ')':
                    start = stack.pop()-1
                    end = i
                    if (not (self.tokens[start] == '(')) and (not (self.tokens[end] == ')')):
                        if (self.tokens[start].isalnum()) or (self.tokens[start] in MOVE_COMMANDS):
                            if self.isVariableDef(self.tokens[start]):
                                words = self.tokens[start - 1 : end+1]
                                correct = self.variableParser.parse_definition(words)
                                i += 4
                            elif self.isCommand(self.tokens[start]):
                                correct, next_pos = self.commandsParser.parse_action(self.tokens[start-1:end+1])
                                i += next_pos
                            elif self.isConditional(self.tokens[start]):
                                correct, block_pos = self.conditionalParser.parse(self.tokens[start - 1 : end+1])
                                
                                block1, next_block_pos = self.isBlock(block_pos)
                                block2, next_pos = self.isBlock(next_block_pos)
                                
                                if not (block1 and block2):
                                    correct = False
                                i += next_pos
                    elif (not self.tokens[i].isalnum()) and (self.tokens[i] in VALID_SYMBOLS):
                        if self.isVariableAssignment(self.tokens[i]):
                            words = self.tokens[i-1:i+4]
                            correct = self.variableParser.parse_assignment(words)
                            i += 4
                        else:
                            correct = False
                else:
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
    
    def isBlock(self, start_pos):
        block_stack = [start_pos]
        i = start_pos
        length = len(self.tokens)
        correct = True
        while correct and (i < length) and (block_stack): 
            if self.tokens[i] == '(':
                block_stack.append(i)
                i += 1
            elif self.tokens[i] == ')':
                start = block_stack.pop() + 1
                end = i
                if (not (self.tokens[start] == '(')) and (not (self.tokens[end] == ')')):
                    if (self.tokens[start].isalnum()) or (self.tokens[start] in MOVE_COMMANDS):
                        if self.isVariableDef(self.tokens[start]):
                            words = self.tokens[start - 1 : end+1]
                            correct = self.variableParser.parse_definition(words)
                            i += 4
                        elif self.isCommand(self.tokens[start]):
                            correct, next_pos = self.commandsParser.parse_action(self.tokens[start-1:end+1])
                            i += next_pos
                        elif self.isConditional(self.tokens[start]):
                            correct, block_pos = self.conditionalParser.parse(self.tokens[start - 1 : end+1])
                            
                            block1, next_block_pos = self.isBlock(block_pos)
                            block2, next_pos = self.isBlock(next_block_pos)
                            
                            if not (block1 and block2):
                                correct = False
                            i += next_pos
                elif (not self.tokens[i].isalnum()) and (self.tokens[i] in VALID_SYMBOLS):
                    if self.isVariableAssignment(self.tokens[i]):
                        words = self.tokens[i-1:i+4]
                        correct = self.variableParser.parse_assignment(words)
                        i += 4
                    else:
                        correct = False
            else:
                i += 1
        return correct, i                            

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
