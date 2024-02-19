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
        self.correct = True
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
        self.correct = False
        block = None
        if tokens[0] == "(":
            stack = [0]
            i = 1
            length = len(tokens)
            self.correct = True
            block_coords = []
            while self.correct and (i < length) and (not block):
                if tokens[i] == "(":
                    stack.append(i)
                elif tokens[i] == ")":
                    start = stack.pop()
                    end = i
                    block_coords.append((start, end))
                if not stack:
                    coords = block_coords.pop()
                    start, end = coords
                    contents = tokens[start : end + 1]
                    new_block = Block(coords, 'block', contents)
                    
                    parsing_answer = self.new_instruction_parser(contents)
                    if parsing_answer:
                        new_block.content_type = parsing_answer
                    else:
                        self.correct = False

                    if self.correct:
                        tree = {new_block : {}}
                        self.new_block_parser(tokens, block_coords, tree)
                        self.correct = self.check_conditionals(tree, new_block)
                        self.correct = self.check_loop(tree, new_block)
                        print(tree)
                i += 1
        return self.correct


    def add_child(self, tokens, block: Block, tree: dict[Block, dict]):
        start, end = block.coords
        is_child = False
        for k in tree:
            s, e = k.coords
            if (start > s) and (end < e):
                is_child = True
                self.add_child(tokens, block, tree[k])
        if not is_child:
            tree[block] = {}
                
    def new_block_parser(
        self, tokens: list[str], block_coords: list[tuple[int, int]], tree: dict[Block, dict]
    ) -> bool:
        if block_coords:
            coords = block_coords.pop()
            start, end = coords
            content = tokens[start : end + 1]
            
            new_block = Block(coords, 'block', content)
            parsing_answer = self.new_instruction_parser(content)
            if parsing_answer:
                new_block.content_type = parsing_answer
            else:
                self.correct = False
                        
            is_child = False
            for key in tree:
                s, e = key.coords
                if (start > s) and (end < e):
                    is_child = True
                    self.add_child(tokens, new_block, tree[key])
            if not is_child:
                tree[new_block] = {}
            self.new_block_parser(tokens, block_coords, tree)
                
            self.correct = self.check_conditionals(tree, new_block)
            self.correct = self.check_loop(tree, new_block)

    def new_instruction_parser(self, tokens: list[str]) -> tuple[bool, Block | None]:
        keyword = 1
        correct = False
        if (tokens[keyword].isalnum()) or (tokens[keyword] in MOVE_COMMANDS):

            if self.is_defvar(tokens[keyword]):
                correct = self.variableParser.parse_definition(tokens)
                if correct:
                    return 'defvar'

            elif self.is_command(tokens[keyword]):
                correct = self.commandsParser.parse(tokens)
                if correct:
                    return 'command'

            elif self.is_loop(tokens[keyword]):
                correct = self.loopParser.parse(tokens)
                if correct:
                    return "loop"

            elif self.is_repeat(tokens[keyword]):
                correct = self.repeatParser.parse(tokens)
                if correct:
                    return "repeat"

            elif self.is_defun(tokens[keyword]):
                correct = self.functionParser.parse_definition(tokens)
                if correct:
                    return "defun"

            elif self.is_func_call(tokens[keyword]):
                correct = self.functionParser.parse_call(tokens)
                if correct:
                    return "func_call"

            elif tokens[keyword] == 'IF':
                return 'if'
            
            elif self.is_conditional(tokens[keyword]):
                correct = self.conditionalParser.parse(tokens)
                if correct:
                    return 'conditional'
            
        elif (not tokens[keyword].isalnum()) and (tokens[keyword] in VALID_SYMBOLS):
            if self.is_var_assign(tokens[keyword]):
                correct = self.variableParser.parse_assignment(tokens)
                if correct:
                    return "assignment"
                
        elif tokens[keyword] == "(":
            return 'block'
        
        elif self.is_conditional(tokens[keyword]):
            correct = self.conditionalParser.parse(tokens)
            if correct:
                return 'conditional'
            
        return correct

    def check_conditionals(self, tree: dict[Block, dict], block: Block | None) -> bool:
        if block.content_type == "if":
            first_child = list(tree[block])[-1]
            print(first_child)
            if (len(tree[block]) != 3) or (first_child.content_type != 'conditional'):
                return False
            for child in tree[block]:
                if child.content_type == "if":
                    return self.check_conditionals(tree[block], child)
        return True

    def check_loop(self, tree: dict[Block, dict], block: Block | None) -> bool:
        if block.content_type == "loop":
            first_child = list(tree[block])[-1]
            if (len(tree[block]) != 2) or (first_child.content_type != 'conditional'):
                return False
            for child in tree[block]:
                if child.content_type == "loop":
                    return self.check_loop(tree[block], child)
                
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
                try:
                    if robotParser.parse(tokens):
                        print("yes")
                    else:
                        print("no")
                except:
                    print("no")
    except FileNotFoundError:
        print("No se encontró el archivo")


if __name__ == "__main__":
    main()
