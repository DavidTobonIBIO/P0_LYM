class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def build_tree(node_list):
    sorted_nodes = sorted(node_list, key=lambda x: x[0])
    root_tuple = sorted_nodes.pop()

    def is_child(parent, child):
        return parent[0] <= child[0] and parent[1] >= child[1]

    def add_children(parent_node, remaining_nodes):
        children = [node for node in remaining_nodes if is_child(node, parent_node.value)]
        for child in children:
            child_node = TreeNode(child)
            parent_node.children.append(child_node)
            remaining_nodes.remove(child)
            add_children(child_node, remaining_nodes)

    root = TreeNode(root_tuple)
    add_children(root, sorted_nodes)

    return root

def print_tree(node, depth=0):
    if node:
        print("  " * depth + str(node.value))
        for child in node.children:
            print_tree(child, depth + 1)

# Example usage:
node_list = [(1, 4), (5, 8), (10, 13), (14, 17), (18, 21), (9, 22), (0, 23)]
tree_root = build_tree(node_list)
print_tree(tree_root)
