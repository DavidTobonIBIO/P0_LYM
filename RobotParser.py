import re
from VariableParser import VariableParser
from FunctionParser import FunctionParser
from CommandParser import CommandsParser


class RobotParser:

    KEYWORDS: set = {
        "DEFVAR",
        "DEFUN",
        "MOVE",
        "SKIP",
        "TURN",
        "NULL",
        "PUT",
        "PICK",
        "MOVE-DIR",
        "MOVE-FACE",
        "RUN-DIRS",
        ":FRONT",
        ":RIGHT",
        ":LEFT",
        ":BACK",
        ":NORTH",
        ":SOUTH",
        ":EAST",
        ":WEST",
    }

    CONSTANTS: set = {
        "DIM",
        "MYXPOS",
        "MYYPOS",
        "MYCHIPS",
        "MYBALLOONS",
        "BALLOONSHERE",
        "CHIPSHERE",
        "SPACES",
    }

    VALID_TYPES: set = {bool, int}

    def __init__(self) -> None:
        self.variableParser = VariableParser()
        self.commandsParser = CommandsParser(self.variableParser)
        self.functionParser = FunctionParser(self.variableParser)

    def tokenize(self, program: str) -> list[str]:
        """
        Tokeniza la cadena de programa dada.

        Args:
            program (str): La cadena de programa a tokenizar.

        Returns:
            list[str]: Una lista de tokens extraídos de la cadena de programa.
        """
        tokens = re.findall(r"\(|\)|[^\s()]+", program.lower())
        return tokens

    def parse(self, program: str) -> bool:
        tokens = self.tokenize(program)
        correct = True
        return correct


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
