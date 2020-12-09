## Decision trees algorithm to predict Kickstarter project success

# get our custom classes/functions
from dtnode import Node
from dtnode_storage import NodeStorage
# regular imports
from math import pow
from typing import List, Tuple

class DecisionTree:
    root_node = None
    # parameters for stopping split recursion
    max_depth, min_node_size = None, None
    # make unique ID for all nodes. just for readability.
    cur_node_id = None
    # don't let a variable be used more than once for a decision.
    # list of ints (indices of variables).
    allowed_vars = None
    # keep track of types of variables to speed up for booleans.
    # 1=numeric, 2=bool 0 or 1)
    var_types = None

    def __init__(self, data:List, max_depth:int, min_node_size:int, var_types:List[int]):
        self.root_node = Node(node_id=0,data=data)
        self.cur_node_id = 1
        self.allowed_vars = [*range(len(data[0])-1)]
        # TODO to not consider the categories, make this [*range(len(data[0])-16)]
        print(self.allowed_vars)
        self.max_depth = max_depth
        self.min_node_size = min_node_size
        self.var_types = var_types

    # we will be using gini index for the cost function.
    def get_gini(self, partition:List[Node]) -> float:
        #print("get_gini called")
        # we will always have two child nodes to compare
        tot_rows = float(len(partition[0].data) + len(partition[1].data))
        gini = 0.0
        # check each child node's uniformity
        for node in partition:
            num_rows = float(len(node.data))
            # prevent div by 0 error
            if num_rows == 0:
                continue
            # count number of failed & success in this node
            num_fail, num_succ = 0.0, 0.0
            for row in node.data:
                if int(row[-1]) == 1:
                    num_succ += 1.0
                else:
                    num_fail += 1.0
            # we can compute the proportion of each
            prop_succ = num_succ / num_rows
            prop_fail = num_fail / num_rows
            # the gini index for this node is then
            node_gini = 1.0 - (prop_succ**2 + prop_fail**2)
            # we then weight by the size of the node relative to the parent
            gini += node_gini * num_rows / tot_rows
        return gini

    # split the dataset and compare gini values of all splits.
    def split_group(self, parent:Node, var_to_split:int, threshold:float) -> Tuple[Node, Node]:
        #print("split_group called")
        # define child groups
        c1 = Node(node_id=self.cur_node_id,data=[],depth=parent.depth+1)
        c2 = Node(node_id=self.cur_node_id+1,data=[],depth=parent.depth+1)
        self.cur_node_id += 2
        # check variable type
        if self.var_types[var_to_split] == 1: # numeric
            for row in parent.data:
                if row[var_to_split] <= threshold:
                    c1.data.append(row)
                else:
                    c2.data.append(row)
        else: # boolean
            for row in parent.data:
                if int(row[var_to_split]) == threshold:
                    c1.data.append(row)
                else:
                    c2.data.append(row)
        return c1, c2
        
    # check the gini of all possible splits to find the best one
    def find_best_split(self, parent:Node, used_vars:List[int]) -> Node:
        print("find_best_split called")
        # need to iterate through all rows with each variable as threshold
        best_gini, split_var, split_thresh, children = 100, None, None, [None, None]
        # check all vars except the label (last column)
        for var_index in self.allowed_vars:
            if var_index in used_vars:
                continue
            # check var type
            if self.var_types[var_index] == 1: #numeric
                for row in parent.data:
                    # make a split
                    c1, c2 = self.split_group(parent, var_index, row[var_index])
                    # evaluate this split
                    gini = self.get_gini(partition=[c1,c2])
                    #print("Checked kids " + str(len(c1.data)) + "," + str(len(c2.data)) + " and got Gini " + str(gini))
                    # if this is the new best, update our info
                    if gini < best_gini:
                        print("found new best gini,"+ str(gini) +", with var " + str(var_index))
                        best_gini = gini
                        split_var, split_thresh = var_index, row[var_index]
                        children = [c1, c2]
                    else: # free up space
                        del c1, c2
            else: # self.var_types[var_index] == 2: #boolean, either 0 or 1
                for thresh in [0,1]:
                    # make a split
                    c1, c2 = self.split_group(parent, var_index, thresh)
                    # evaluate this split
                    gini = self.get_gini(partition=[c1,c2])
                    #print("Checked kids " + str(len(c1.data)) + "," + str(len(c2.data)) + " and got Gini " + str(gini))
                    # if this is the new best, update our info
                    if gini < best_gini:
                        print("found new best gini,"+ str(gini) +", with var " + str(var_index))
                        best_gini = gini
                        split_var, split_thresh = var_index, thresh
                        children = [c1, c2]
                    else: # free up space
                        del c1, c2
        # now that we know the best split, do it!
        parent.set_thresh(var=split_var,thresh=split_thresh,var_type=self.var_types[split_var])
        parent.set_children(children[0], children[1])
        # remove the chosen variable from future consideration
        #used_vars.append(var_index)
        return parent, used_vars+[split_var]
        
    def split(self, node:Node, used_vars:List[int]=None) -> Node:
        print("split called")
        # if we have reached max recursion depth, stop. 
        # if the node is almost entirely one label, stop.
        # prevents overfitting.
        if node.depth >= self.max_depth: #or node.purity < 0.05:
            node.set_terminal()
            return node
        # if used_vars is not provided, initialize it empty
        if used_vars is None:
            used_vars = []
        # first do the best split for this node
        node, new_used_vars = self.find_best_split(parent=node, used_vars=used_vars)
        print("have now used " + str(new_used_vars))
        # if either child is smaller than our min acceptable size, stop. prevents overfitting.
        # first check child 1.
        if len(node.c1.data) < self.min_node_size: #node.c1 is None or 
            node.c1.set_terminal()
        else:
            # we aren't done yet. recurse into the child node.
            node.c1 = self.split(node.c1, used_vars=new_used_vars)
        # check child 2.
        if len(node.c2.data) < self.min_node_size: #node.c2 is None or 
            node.c2.set_terminal()
        else:
            # recurse into the child node.
            node.c2 = self.split(node.c2, used_vars=new_used_vars)
        # when recursion has concluded, return the node
        return node


    # test our trained tree with an example row.
    # will return 0 (failed) or 1 (successful)
    def predict(self, root_node: Node, example: List[float]) -> int:
        return root_node.get_decision(example)

    # test our trained tree with an example list of rows.
    # will return predictions as list of 0s and 1s
    def predict_list(self, examples:List, root_node:Node=None) -> List[int]:
        if root_node is None:
            root_node = self.root_node
        num_examples = len(examples)
        decisions = [None for i in range(num_examples)]
        for i in range(num_examples):
            decisions[i] = self.predict(root_node,examples[i])
        return decisions

