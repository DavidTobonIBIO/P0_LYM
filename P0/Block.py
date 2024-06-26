class Block:
    def __init__(self, coords: tuple[int, int], content_type, content: list[str]):
        self.coords: tuple[int, int] = coords
        self.content_type: str = content_type
        self.content = content
        self.parent: Block | None = None
        self.children: list[Block] = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def set_parent(self, parent):
        self.parent = parent
        
    def __str__(self):
        return f"(Block: {self.coords}, type: {self.content_type}, father: {self.parent})"
    
    def __repr__(self):
        return f"(Block: {self.coords},  type: {self.content_type}, father: {self.parent})"