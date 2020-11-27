## Decision trees algorithm to predict Kickstarter project success

# get our custom classes/functions
from dtnode import Node
from dtnode_storage import NodeStorage
# regular imports
from math import pow
from typing import List, Tuple

class DecisionTree:
    root_node = None

    def __init__(self, data: List):
        self.root_node = Node(data=data)

    # we will be using gini index for the cost function.
    def get_gini(self, partition: List[Node]) -> float:
        #print("get_gini called")
        tot_rows = len(partition)
        gini = 0.0
        # check each group's uniformity
        for node in partition:
            group_size = len(node.data)
            # prevent div by 0 error
            if group_size == 0:
                continue
            # count number of failed & success in this group
            num_fail, num_succ = 0, 0
            for row in node.data:
                if row[-1] == 1:
                    num_succ += 1
                else:
                    num_fail += 1
            # update the group's score accordingly
            group_gini = pow(num_succ/group_size, 2) + pow(num_fail/group_size, 2)
            # update the overall gini score
            gini += (1.0 - group_gini) * (group_size / tot_rows)
        return gini

    # split the dataset and compare gini values of all splits.
    def split_group(self, parent: Node, var_to_split: int, threshold: float) -> Tuple[Node, Node]:
        #print("split_group called")
        # define child groups
        c1, c2 = Node(data=[],depth=parent.depth+1), Node(data=[],depth=parent.depth+1)
        # only numeric vars for now
        for row in parent.data:
            if row[var_to_split] <= threshold:
                c1.data.append(row)
            else:
                c2.data.append(row)
        return c1, c2
        
    # check the gini of all possible splits to find the best one
    def find_best_split(self, parent: Node) -> Node:
        print("find_best_split called")
        # need to iterate through all rows with each variable as threshold
        best_gini, split_var, split_thresh, children = 100, None, None, [None, None]
        # check all vars except 0=index and -1=label
        for var_index in range(1, len(parent.data[0])-1):
            for row in parent.data:
                # make a split
                c1, c2 = self.split_group(parent, var_index, row[var_index])
                # evaluate this split
                gini = self.get_gini(partition=[c1,c2])
                # if this is the new best, update our info
                if gini < best_gini:
                    print("found new best gini")
                    best_gini = gini
                    split_var, split_thresh = var_index, row[var_index]
                    children = [c1, c2]
                else: # free up space
                    del c1, c2
        # now that we know the best split, do it!
        parent.set_thresh(var=split_var,thresh=split_thresh)
        parent.set_children(children[0], children[1])
        return parent
        
    def split(self, node: Node, max_depth: int, min_node_size: int) -> Node:
        print("split called")
        # if we have reached max recursion depth, stop. prevents overfitting.
        if node.depth >= max_depth:
            node.set_terminal()
            return node
        # first do the best split for this node
        node = self.find_best_split(parent=node)
        # if either child is smaller than our min acceptable size, stop. prevents overfitting.
        # first check child 1.
        if len(node.c1.data) < min_node_size:
            node.c1.set_terminal()
        else:
            # we aren't done yet. recurse into the child node.
            node.c1 = self.split(node.c1, max_depth, min_node_size)
        # check child 2.
        if len(node.c2.data) < min_node_size:
            node.c2.set_terminal()
        else:
            # recurse into the child node.
            node.c2 = self.split(node.c2, max_depth, min_node_size)
        # when recursion has concluded, return the node
        return node


    # test our trained tree with an example row.
    # will return 0 (failed) or 1 (successful)
    def predict(self, root_node: Node, example: List[float]) -> int:
        return root_node.get_decision(example)

    # test our trained tree with an example list of rows.
    # will return predictions as list of 0s and 1s
    def predict_list(self, root_node: Node, examples: List) -> List[int]:
        num_examples = len(examples)
        decisions = [None for i in range(num_examples)]
        for i in range(num_examples):
            decisions[i] = self.predict(root_node,examples[i])
        return decisions

