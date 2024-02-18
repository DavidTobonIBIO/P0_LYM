import re
from instructions.Command import Command
from instructions.Conditional import Conditional
from instructions.FunctionDefinition import FunctionDefinition
from instructions.FunctionCall import FunctionCall
from instructions.Loop import Loop
from instructions.Repeat import Repeat
from instructions.VariableDefinition import VariableDefinition
from instructions.VariableAssignment import VariableAssignment

from parsers.CommandParser import CommandParser
from parsers.ConditionalParser import ConditionalParser
from parsers.LoopParser import LoopParser
from parsers.RepeatParser import RepeatParser
from parsers.ParenthesisParser import ParenthesisParser
from parsers.VariableParser import VariableParser

from Block import Block
from constants import VALID_SYMBOLS, MOVE_COMMANDS, INSTRUCTION_CREATORS, CONDITIONALS
import os


class RobotParser:
    def __init__(self, program: str):
        self.program = program
        self.tokens = []
        self.parenthesisParser = ParenthesisParser()
        self.variableParser = VariableParser()
        self.commandsParser = CommandParser(self.variableParser)
        self.conditionalParser = ConditionalParser(self.variableParser)
        self.loopParser = LoopParser(self.conditionalParser)
        self.repeatParser = RepeatParser(self.variableParser)

    def tokenize(self) -> list[str]:
        """
        Tokeniza la cadena de programa dada.

        Args:
            program (str): La cadena de programa a tokenizar.

        Returns:
            list[str]: Una lista de tokens extraídos de la cadena de programa.
        """
        self.tokens = re.findall(r"\(|\)|[^\s()]+", self.program.upper())
        return self.tokens

    def parse(self, tokens: list[str]) -> bool:
        correct = False
        block = None
        displacement = 0
        if self.parenthesisParser.parse(tokens) and tokens[0] == '(':
            stack = [0]
            i = 1
            length = len(tokens)
            correct = True
            while correct and (i < length):
                if tokens[i] == "(":
                    stack.append(i)
                elif tokens[i] == ")":
                    start = stack.pop()
                    end = i
                # Bloque encontrado
                if not stack:
                    # print(start, end)
                    print("Block found: ", tokens[start:end + 1])
                    block = Block("block", tokens[start:end + 1])
                    if (tokens[start + 1] == "("):
                        correct, child, displacement = self.parse(tokens[start + 1 : end])
                        print("Child found: ", tokens[start + 1 : end])
                        block.addChild(child)
                        
                    elif tokens[start + 1] in INSTRUCTION_CREATORS:
                        # print("Instruction found: ", tokens[start: end + 1])
                        correct, block, displacement = self.newBlockParser(start, end, tokens)
                i += 1
        return correct, block, displacement

    def newBlockParser(
        self, start: int, end: int, tokens: list[str]
    ) -> tuple[bool, Block | None]:
        keyword = start + 1
        correct = False
        block = None
        displacement = 0
        if (tokens[keyword].isalnum()) or (tokens[keyword] in MOVE_COMMANDS):
            if self.isVariableDef(tokens[keyword]):
                words = tokens[start : end + 1]
                correct, name, value = self.variableParser.parse_definition(words)
                if correct:
                    block = Block("defvar", words)
                    
            elif self.isCommand(tokens[keyword]):
                correct, command_type, params = self.commandsParser.parse(
                    tokens[start : end + 1]
                )
                if correct:
                    block = Block("command", tokens[start : end + 1])
                    
            elif self.isConditional(tokens[keyword]):
                correct, displacement = self.conditionalParser.parse(
                    tokens[start : end + 1]
                )
                if correct:
                    block = Block("conditional", tokens[start : end + 1])
                    
            elif self.isLoop(tokens[keyword]):
                correct = self.loopParser.parse(tokens[start : end + 1])
                if correct:
                    block = Block("loop". tokens[start : end + 1])
                    
            elif self.isRepeat(tokens[keyword]):
                correct = self.repeatParser.parse(tokens[start : end + 1])
                if correct:
                    block = Block("repeat", tokens[start : end + 1])
                    
        elif (not tokens[keyword].isalnum()) and (tokens[keyword] in VALID_SYMBOLS):
            if self.isVariableAssignment(tokens[keyword]):
                words = tokens[start : end + 1]
                correct, name, value = self.variableParser.parse_assignment(words)
                if correct:
                    block = Block("assignment", tokens[start : end + 1])

        return correct, block, displacement
    
    def checkConditionals(self, block: Block | None) -> bool:
        if block:
            if block.content_type == "conditional":
                if len(block.children) != 2:
                    return False
                for child in block.children:
                    if child.content_type == "conditional":
                        return self.checkConditionals(child)
        return True

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
        if word in CONDITIONALS:
            return True
        return False

    def isFunction(self, word):
        if word == "DEFUN":
            return True
        return False
    
    def isLoop(self, word):
        if word == "LOOP":
            return True
        return False
    
    def isRepeat(self, word):
        if word == "REPEAT":
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
            robotParser = RobotParser(program)
            tokens = robotParser.tokenize()
            try:
                if robotParser.parse(tokens)[0]:
                    print("yes")
                else:
                    print("no")
            except:
                print("no")
    except FileNotFoundError:
        print("No se encontró el archivo")


if __name__ == "__main__":
    main()
