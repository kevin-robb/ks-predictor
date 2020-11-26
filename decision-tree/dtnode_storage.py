from dtnode import Node
#from numpy import savetxt
from typing import List, Tuple

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

    def __init__(self, root_node:Node=None, fname:str=None):
        self.root = root_node
        self.arr = []
        self.filename = fname
    
    def max_nodes(self, root_node:Node) -> int:
        # find the max number of nodes in this tree.
        # need this info to initialize arr.
        height = self.tree_height(root_node)
        return 2**height - 1

    def tree_height(self, node:Node) -> int:
        # recursively find the height of the tree.
        if node is None:
            return 0
        else:
            return max(self.tree_height(node.c1), self.tree_height(node.c2)) + 1

    def populate_arr(self, node:Node, pos:int=0):
        # traverse tree inorder and store each node in the right place.
        if node is None:
            return
        self.arr[pos] = [node.split_var, node.split_thresh]
        if node.c1 is not None:
            self.populate_arr(node.c1, pos=2*pos+1)
        if node.c2 is not None:
            self.populate_arr(node.c2, pos=2*pos+2)

    def tree_to_arr(self, root_node:Node) -> List:
        # initialize all nodes with None. This allows us to use a non-complete tree.
        self.arr = [None for i in range(self.max_nodes(root_node))]
        # populate the array from the tree
        self.populate_arr(root_node, pos=0)
        return self.arr
    
    def populate_tree(self, node:Node, n:int, pos:int=0):
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

    def arr_to_tree(self) -> Node:
        # need to discard all None values in arr as empty space, not nodes.
        if self.arr is None or self.arr[0] is None:
            print("arr does not contain a valid tree")
            return None
        # populate the root node (arr[0]) recursively and return it
        self.root = Node(split_var=self.arr[0][0], split_thresh=self.arr[0][1])
        self.populate_tree(self.root, n=len(self.arr), pos=0)
        return self.root

    def print_tree_inorder(self,node:Node):
        # helper function for printing tree inorder
        if node is None:
            return
        self.print_tree_inorder(node.c1)
        print(node)
        self.print_tree_inorder(node.c2)
    
    def print_tree_preorder(self,node:Node):
        # helper function for printing tree preorder
        if node is None:
            return
        print(node)
        self.print_tree_preorder(node.c1)
        self.print_tree_preorder(node.c2)

    def print_arr(self):
        # helper function to print arr.
        for i in range(len(self.arr)):
            print(self.arr[i])

    ## File I/O
    def tree_to_file(self, root_node:Node=None, filename:str=None):
        if filename == None:
            filename = self.filename
        # first make sure self.arr is using this node as root.
        if root_node is not None:
            self.root = root_node
        self.tree_to_arr(root_node)
        # clear the file first (w=write mode).
        file1=open("trees/" + filename + ".txt","w")
        file1.write("")
        file1.close()
        # don't overwrite with each statement (a=append).
        file1=open("trees/" + filename + ".txt","a")
        # make sure everything goes out as a string.
        for i in range(len(self.arr)):
            for j in range(len(self.arr[0])):
                if j != 0:
                    file1.write(" ")
                file1.write(str(self.arr[i][j]))
            file1.write("\n")
        file1.close()

    def file_to_tree(self, filename:str=None) -> Node:
        if filename == None:
            filename = self.filename
        # open file in read mode.
        file1=open("trees/" + filename + ".txt", "r+")
        # read each line & return as each a string element in a list.
        file_content = file1.readlines()
        # initialize array to store data from file.
        self.arr = [None for i in range(len(file_content))]
        # go through and parse each line as a row in arr.
        # make sure everything comes in as a float.
        # make sure to skip None rows.
        for i in range(len(file_content)):
            if file_content[i] is None or file_content[i] == "None":
                continue
            row_str = file_content[i].split(" ")
            row = [None for l in range(len(row_str))]
            for j in range(len(row)):
                row[j] = float(row_str[j])
            self.arr[i] = row
        # convert arr to tree and return
        self.root = self.arr_to_tree()
        return self.root

