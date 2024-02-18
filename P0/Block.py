class Block:
    def __init__(self, content_type, content: list[str], children=[]):
        self.content_type: str = content_type
        self.content = content
        self.children: list[Block] = children
        
    def add_child(self, child):
        self.children.append(child)
        # print(f"Parent: {self.content}")
        # print(f"Added child {child.content}")
        
    def __str__(self):
        return f"Block: {self.content_type}, children: {[child.content_type for child in self.children]}"
    
    def __repr__(self):
        return f"Block: {self.content_type}, children: {[child.content_type for child in self.children]}"