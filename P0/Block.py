class Block:
    def __init__(self, content_type, content, children=[]):
        self.content_type: str = content_type
        self.content = content
        # if parent is None:
        #     self.parent = Block()
        # else:
        #     self.parent = parent
        self.children: list[Block] = children
        
    def addChild(self, child):
        self.children.append(child)
        # child.parent = self
        
    def __str__(self):
        return f"Block: {self.content_type}, children: {[child.content_type for child in self.children]}"
    
    def __repr__(self):
        return f"Block: {self.content_type}, children: {[child.content_type for child in self.children]}"