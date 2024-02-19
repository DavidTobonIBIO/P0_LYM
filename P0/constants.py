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
    "IF",
    "FACING?",
    "BLOCKED?",
    "CAN-PUT?",
    "CAN-PICK?",
    "CAN-MOVE?",
    "ISZERO?",
    "NOT",
    "LOOP",
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

VALID_SYMBOLS: set = {":", "-", "?", "="}

MOVE_COMMANDS: set = {
    "MOVE",
    "SKIP",
    "TURN",
    "FACE",
    "PUT",
    "PICK",
    "MOVE-DIR",
    "MOVE-FACE",
    "RUN-DIRS",
    "NULL",
}

CONDITIONALS: set = {
    "FACING?",
    "BLOCKED?",
    "CAN-PUT?",
    "CAN-PICK?",
    "CAN-MOVE?",
    "ISZERO?",
    "NOT",
}

ITEMS: set = {":BALLOONS", ":CHIPS"}

ORIENTATIONS: set = {":NORTH", ":SOUTH", ":EAST", ":WEST"}

RUN_DIRECTIONS: set = {":FRONT", ":RIGHT", ":LEFT", ":BACK"}

TURN_DIRECTIONS: set = {":LEFT", ":RIGHT", ":AROUND"}

INSTRUCTION_CREATORS: set = {
    "DEFVAR",
    "DEFUN",
    "=",
    "MOVE",
    "SKIP",
    "TURN",
    "NULL",
    "PUT",
    "PICK",
    "MOVE-DIR",
    "MOVE-FACE",
    "RUN-DIRS",
    "LOOP",
    "REPEAT"
}
