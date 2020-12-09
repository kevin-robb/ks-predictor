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
    # array to store the tree data [var_index,var_thresh,decision]
    arr = None
    # filename being written to
    filename = None
    # list of variable names
    header = None

    def __init__(self, root_node:Node=None, fname:str=None, header:List=None):
        self.root = root_node
        self.arr = []
        self.filename = fname
        self.header = header
    
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
        self.arr[pos] = [node.split_var, node.split_thresh, node.decision]
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
            node.c1 = Node(split_var=self.arr[new_pos][0], split_thresh=self.arr[new_pos][1], decision=self.arr[new_pos][2])
            self.populate_tree(node.c1, n, new_pos)
        # set the right subtree of parent
        new_pos = 2*pos+2
        if new_pos < n and self.arr[new_pos] is not None:
            node.c2 = Node(split_var=self.arr[new_pos][0], split_thresh=self.arr[new_pos][1], decision=self.arr[new_pos][2])
            self.populate_tree(node.c2, n, new_pos)

    def arr_to_tree(self) -> Node:
        # need to discard all None values in arr as empty space, not nodes.
        if self.arr is None or self.arr[0] is None:
            print("arr does not contain a valid tree")
            return None
        # populate the root node (arr[0]) recursively and return it
        self.root = Node(split_var=self.arr[0][0], split_thresh=self.arr[0][1], decision=self.arr[0][2])
        self.populate_tree(self.root, n=len(self.arr), pos=0)
        return self.root

    def print_tree_inorder(self, node:Node, print_to_console:bool=True):
        # helper function for printing tree inorder
        if node is None:
            return
        if print_to_console:
            self.print_tree_inorder(node.c1)
            print(self.print_node(node))
            self.print_tree_inorder(node.c2)
        else:
            # store tree in list rather than printing
            ls = []
            left = self.print_tree_inorder(node.c1,print_to_console)
            if left is not None:
                for el in left:
                    ls.append(el)
            ls.append(self.print_node(node))
            right = self.print_tree_inorder(node.c2,print_to_console)
            if right is not None:
                for el in right:
                    ls.append(el)
            return ls
    
    def print_tree_preorder(self, node:Node, print_to_console:bool=True):
        # helper function for printing tree preorder
        if node is None:
            return
        if print_to_console:
            print(self.print_node(node))
            self.print_tree_preorder(node.c1)
            self.print_tree_preorder(node.c2)
        else:
            # store tree in list rather than printing
            ls = [self.print_node(node)]
            left = self.print_tree_preorder(node.c1,print_to_console)
            if left is not None:
                for el in left:
                    ls.append(el)
            right = self.print_tree_preorder(node.c2,print_to_console)
            if right is not None:
                for el in right:
                    ls.append(el)
            return ls
        

    def print_node(self, node:Node):
        # helper function to print a single node
        spacing = "|" + "-" * (node.depth - 1)
        # use the header to put var names and values
        if node.is_terminal:
            return spacing+"Node "+str(node.node_id)+": decision="+str(node.decision)
        else:
            if node.var_type == 1: #numeric, use <=
                return spacing+"Node "+str(node.node_id)+": "+self.header[node.split_var]+" <= "+str(node.split_thresh)
            else: #boolean, use ==
                return spacing+"Node "+str(node.node_id)+": "+self.header[node.split_var]+" == "+str(node.split_thresh)

    def print_arr(self):
        # helper function to print arr.
        for i in range(len(self.arr)):
            print(self.arr[i])

    ## File I/O
    def tree_to_file(self, root_node:Node=None, filename:str=None):
        # store the tree to a file in a recoverable format
        if filename is None:
            filename = self.filename
        # use the true root node if one is not provided
        if root_node is None:
            root_node = self.root
        self.tree_to_arr(root_node)
        # clear the file first (w=write mode).
        file1=open("tree_storage/" + filename + ".txt","w")
        file1.write("")
        file1.close()
        # don't overwrite with each statement (a=append).
        file1=open("tree_storage/" + filename + ".txt","a")
        # make sure everything goes out as a string.
        for i in range(len(self.arr)):
            # we will have a None row for missing nodes that needs to be accounted for.
            if self.arr[i] is None:
                # mark the row as empty in the file (using -1 index).
                file1.write("-1,0,-1")
            else:
                # store the node's var, thresh, & decision.
                # terminal nodes will be None,None,int.
                # other nodes will be int,float,None.
                file1.write(str(self.arr[i][0])+","+str(self.arr[i][1])+","+str(self.arr[i][2]))
            file1.write("\n")
        file1.close()

    def file_to_tree(self, filename:str=None) -> Node:
        # read from a file and store the contents as a tree
        if filename is None:
            filename = self.filename
        # open file in read mode.
        file1=open("tree_storage/" + filename + ".txt", "r+")
        # read each line & return as each a string element in a list.
        file_content = file1.readlines()
        # initialize array to store data from file.
        self.arr = [None for i in range(len(file_content))]
        # go through and parse each line as a row in arr.
            # -1,0,-1: no node.
            # None,None,int: terminal nodes.
            # int,float,None: other nodes.
        # make sure to skip None rows (denoted "-" in file).
        for i in range(len(file_content)):
            row_str = file_content[i].split(",")
            if row_str[0] == "None": # terminal node.
                self.arr[i] = [None,None,int(row_str[2])]
            elif int(row_str[0]) == -1: # no node. leave None.
                continue
            else: # non-terminal node.
                self.arr[i] = [int(row_str[0]), float(row_str[1]), None]
        # convert arr to tree and return
        self.root = self.arr_to_tree()
        return self.root
    
    def tree_to_file_readable(self, root_node:Node=None, filename:str=None, acc:float=-1):
        # print tree to file in readable format for analysis by humans
        if filename is None:
            filename = self.filename
        # use the true root node if one is not provided
        if root_node is None:
            root_node = self.root
        # get our array to print
        tree = self.print_tree_preorder(node=root_node,print_to_console=False)
        # clear the file first (w=write mode).
        file1=open("trees/" + filename + "_readable" + ".txt","w")
        file1.write("")
        file1.close()
        # don't overwrite with each statement (a=append).
        file1=open("trees/" + filename + "_readable" + ".txt","a")
        # write the tree (list of strings) to the file
        for l in tree:
            file1.write(l + "\n")
        # write the accuracy at the end
        file1.write("\nThe Accuracy is " + str(acc))
        file1.close()

