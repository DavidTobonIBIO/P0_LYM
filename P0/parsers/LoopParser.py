class LoopParser:
    def __init__(self, conditionalParser):
        self.conditionalParser = conditionalParser
    
    def parse(self, words: list[str]) -> tuple:
        if words[0] == "(":
            if words[1] == "LOOP":
                if self.conditionalParser.parse(words[2:]):
                    return words[-1] == ")"
                    
        return False