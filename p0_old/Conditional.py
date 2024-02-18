class Conditional:
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2
        
    def addBlock(self, block):
        if self.b1:
            self.b2 = block
        else:
            self.b1 = block