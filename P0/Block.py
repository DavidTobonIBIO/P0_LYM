class Block:
    def __init__(self, content_type, parent=None, children=[]):
        self.content_type: str = content_type
        # self.parent: Block = parent
        self.children: list[Block] = children
        
    def addChild(self, child):
        self.children.append(child)
        # child.parent = self
        
    def __str__(self):
        return f"Block: {self.content_type}, children: {self.children}"
    
    def __repr__(self):
        return f"Block: {self.content_type}, children: {self.children}"