from dtnode import Node
from numpy import savetxt
# node storage class for turning our tree into an array,
# writing it to a file, reading from a file, and recreating the tree.
# referenced https://www.ritambhara.in/storing-binary-tree-in-a-file/,
# and translated their code from C into Python.
class NodeStorage:
    # root node of tree
    root = None
    # array to store the tree data
    arr = None
    # filename being written to
    filename = None

    def __init__(self, root_node, fname):
        self.root = root_node
        self.arr = []
        self.filename = fname
    
    def max_nodes(self, root_node):
        # find the max number of nodes in this tree.
        # need this info to initialize arr.
        height = self.tree_height(root_node)
        return 2**height - 1

    def tree_height(self, node):
        # recursively find the height of the tree.
        if node is None:
            return 0
        else:
            return max(self.tree_height(node.c1), self.tree_height(node.c2)) + 1

    def populate_arr(self, node, pos=0):
        # traverse tree inorder and store each node in the right place.
        if node is None:
            return
        self.arr[pos] = [node.split_var, node.split_thresh]
        if node.c1 is not None:
            self.populate_arr(node.c1, pos=2*pos+1)
        if node.c2 is not None:
            self.populate_arr(node.c2, pos=2*pos+2)

    def tree_to_arr(self, root_node):
        # initialize all nodes with None. This allows us to use a non-complete tree.
        self.arr = [None for i in range(self.max_nodes(root_node))]
        # populate the array from the tree
        self.populate_arr(root_node, pos=0)
        return self.arr
    
    def populate_tree(self, node, n, pos=0):
        # pos = position of parent "node" in array
        # n = length of arr
        if node is None or self.arr is None or n==0:
            return
        # set left subtree of parent
        new_pos = 2*pos+1
        if new_pos < n and self.arr[new_pos] is not None:
            node.c1 = Node(split_var=self.arr[new_pos][0], split_thresh=self.arr[new_pos][1])
            self.populate_tree(node.c1, n, new_pos)
        # set the right subtree of parent
        new_pos = 2*pos+2
        if new_pos < n and self.arr[new_pos] is not None:
            node.c2 = Node(split_var=self.arr[new_pos][0], split_thresh=self.arr[new_pos][1])
            self.populate_tree(node.c2, n, new_pos)

    def arr_to_tree(self):
        # need to discard all None values in arr as empty space, not nodes.
        if self.arr is None or self.arr[0] is None:
            print("arr does not contain a valid tree")
            return None
        # populate the root node (arr[0]) recursively and return it
        self.root = Node(split_var=self.arr[0][0], split_thresh=self.arr[0][1])
        self.populate_tree(self.root, n=len(self.arr), pos=0)
        return self.root

    def print_tree_inorder(self,root_node=None):
        # helper function for printing tree inorder
        if root_node is None:
            return
        self.print_tree_inorder(root_node.c1)
        print(root_node)
        self.print_tree_inorder(root_node.c2)
    
    def print_tree_preorder(self,root_node=None):
        # helper function for printing tree preorder
        if root_node is None:
            return
        print(root_node)
        self.print_tree_preorder(root_node.c1)
        self.print_tree_preorder(root_node.c2)

    def print_arr(self):
        # helper function to print arr
        for i in range(len(self.arr)):
            print(self.arr[i])

    def write_to_file(self, filename=None):
        # convert the root node to arr and write to file
        if filename == None:
            filename = self.filename
        savetxt(filename, self.tree_to_arr(self.root))
