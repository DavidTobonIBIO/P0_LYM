class ParenthesisParser():
    def __init__(self):
        pass
    
    def parse(self, tokens: list) -> bool:
        open_parenthesis: int = 0

        correct: bool = True
        i: int = 0
        while correct and (i < len(tokens)):
            line = tokens[i]
            for char in line:
                if char == "(":
                    open_parenthesis += 1
                elif char == ")":
                    if open_parenthesis > 0:
                        open_parenthesis -= 1
                    else:
                        correct = False
            i += 1

        if open_parenthesis != 0:
            correct = False
            
        return correct