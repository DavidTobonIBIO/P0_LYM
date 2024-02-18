import re

from parsers.CommandParser import CommandParser
from parsers.ConditionalParser import ConditionalParser
from parsers.FunctionParser import FunctionParser
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
        self.functionParser = FunctionParser(self.variableParser)

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

    def parse_parentesis(self, tokens: list[str]) -> bool:
        return self.parenthesisParser.parse(tokens)

    def parse(self, tokens: list[str]) -> bool:
        correct = False
        block = None
        if tokens[0] == "(":
            stack = [0]
            i = 1
            length = len(tokens)
            correct = True
            while correct and (i < length) and (not block):
                if tokens[i] == "(":
                    stack.append(i)
                elif tokens[i] == ")":
                    start = stack.pop()
                    end = i
                # Bloque encontrado
                if not stack:
                    # crear nuevo bloque
                    block = Block("block", tokens[start : end + 1])
                    if tokens[start + 1] == "(":
                        # Si empieza con parentesis, es un bloque anidado
                        correct, child = self.parse(tokens[start + 1 : end])
                        end = len(child.content) + start
                        while (tokens[end + 1] == "(") and correct:
                            correct, new_child = self.parse(tokens[end + 1 :])
                            if correct:
                                block.add_child(new_child)
                                end = len(new_child.content) + end

                        block.add_child(child)
                        print(block.children)
                    elif (
                        tokens[start + 1] in INSTRUCTION_CREATORS
                        or tokens[start + 1] in self.functionParser.functions
                    ):
                        correct, block = self.new_instruction_parser(
                            tokens[start : end + 1]
                        )
                    else:
                        correct = False
                else:
                    i += 1
        return correct, block

    def new_instruction_parser(self, tokens: list[str]) -> tuple[bool, Block | None]:
        keyword = 1
        correct = False
        block = None
        if (tokens[keyword].isalnum()) or (tokens[keyword] in MOVE_COMMANDS):

            if self.is_defvar(tokens[keyword]):
                correct = self.variableParser.parse_definition(tokens)
                if correct:
                    block = Block("defvar", tokens)

            elif self.is_command(tokens[keyword]):
                correct = self.commandsParser.parse(tokens)
                if correct:
                    block = Block("command", tokens)

            elif self.is_conditional(tokens[keyword]):
                correct, displacement = self.conditionalParser.parse(tokens)
                if correct:
                    block = Block("conditional", tokens)

            elif self.is_loop(tokens[keyword]):
                correct = self.loopParser.parse(tokens)
                if correct:
                    block = Block("loop", tokens)

            elif self.is_repeat(tokens[keyword]):
                correct = self.repeatParser.parse(tokens)
                if correct:
                    block = Block("repeat", tokens)

            elif self.is_defun(tokens[keyword]):
                correct = self.functionParser.parse_definition(tokens)
                if correct:
                    block = Block("defun", tokens)

            elif self.is_func_call(tokens[keyword]):
                correct = self.functionParser.parse_call(tokens)
                if correct:
                    block = Block("func_call", tokens)

        elif (not tokens[keyword].isalnum()) and (tokens[keyword] in VALID_SYMBOLS):
            if self.is_var_assign(tokens[keyword]):
                correct = self.variableParser.parse_assignment(tokens)
                if correct:
                    block = Block("assignment", tokens)

        return correct, block

    def check_conditionals(self, block: Block | None) -> bool:
        if block:
            if block.content_type == "conditional":
                if len(block.children) != 2:
                    return False
                for child in block.children:
                    if child.content_type == "conditional":
                        return self.check_conditionals(child)
        return True

    def is_defvar(self, word):
        if word == "DEFVAR":
            return True
        return False

    def is_var_assign(self, word):
        if word == "=":
            return True
        return False

    def is_command(self, word):
        if word in MOVE_COMMANDS:
            return True
        return False

    def is_conditional(self, word):
        if word in CONDITIONALS:
            return True
        return False

    def is_loop(self, word):
        if word == "LOOP":
            return True
        return False

    def is_repeat(self, word):
        if word == "REPEAT":
            return True
        return False

    def is_defun(self, word):
        if word == "DEFUN":
            return True
        return False

    def is_func_call(self, word):
        if word in self.functionParser.functions:
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
            if robotParser.parse_parentesis(tokens):
                # try:
                if robotParser.parse(tokens)[0]:
                    print("yes")
                else:
                    print("no")
                # except:
                    # print("no")
    except FileNotFoundError:
        print("No se encontró el archivo")


if __name__ == "__main__":
    main()
