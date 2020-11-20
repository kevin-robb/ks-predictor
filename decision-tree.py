## Decision trees algorithm to predict Kickstarter project success

from math import pow

# keep track of each variable's index and its type
types = ["numeric","categorical"] #TODO fill in with var indexes corresponding to type
labels = ["successful","failed"]

# we will be using gini index for the cost function.
def get_gini(partition):
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
            if row[-1] == "successful":
                num_succ += 1
            else:
                num_fail += 1
        # update the group's score accordingly
        group_gini = pow(num_succ/group_size, 2) + pow(num_fail/group_size, 2)
        # update the overall gini score
        gini += (1.0 - group_gini) * (group_size / tot_rows)
    return gini

# split the dataset and compare gini values of all splits.
# need to take into account numeric vs categorical variables.
def split_group(parent, var_to_split, threshold):
    # define child groups
    c1, c2 = Node(data=[],depth=parent.depth+1), Node(data=[],depth=parent.depth+1)
    # check whether specified var is numeric or categorical
    if types[var_to_split] == "numeric":
        # numeric variable. simple to partition
        for row in parent.data:
            if row[var_to_split] < threshold:
                c1.data.append(row)
            else:
                c2.data.append(row)
        return c1, c2
    else:
        # categorical variable
        pass #TODO
	
# check the gini of all possible splits to find the best one
def find_best_split(parent):
    # need to iterate through all rows with each variable as threshold
    best_gini, split_var, split_thresh, children = 100, None, None, [None, None]
    for var_index in range(len(parent.data[0])-1):
        for row in parent.data:
            # make a split
            c1, c2 = split_group(parent, var_index, row[var_index])
            # evaluate this split
            gini = get_gini(partition=[c1,c2])
            # if this is the new best, update our info
            if gini < best_gini:
                best_gini = gini
                split_var, split_thresh = var_index, row[var_index]
                children = [c1, c2]
    # now that we know the best split, do it!
    parent.set_thresh(var=split_var,thresh=split_thresh)
    parent.set_children(children[0], children[1])
    return parent
    
def split(node, max_depth, min_node_size):
    # if we have reached max recursion depth, stop. prevents overfitting.
    if node.depth >= max_depth:
        node.set_terminal()
        return node
    # first do the best split for this node
    node = find_best_split(parent=node)
    # if either child is smaller than our min acceptable size, stop. prevents overfitting.
    # first check child 1.
    if len(node.c1.data) < min_node_size:
        node.c1.set_terminal()
    else:
        # we aren't done yet. recurse into the child node.
        node.c1 = split(node.c1, max_depth, min_node_size)
    # check child 2.
    if len(node.c2.data) < min_node_size:
        node.c2.set_terminal()
    else:
        # recurse into the child node.
        node.c2 = split(node.c2, max_depth, min_node_size)
    # when recursion has concluded, return the node
    return node


# test our trained tree with an example row
def test_example(root_node, example):
    return root_node.get_decision(example)



# define node class to make tree structure simpler
class Node:
    def __init__(self, data, depth):
        self.data = data
        self.c1 = None
        self.c2 = None
        self.depth = depth
        self.split_var = None
        self.split_thresh = None
        self.is_terminal = False
        self.decision = None
    
    def set_thresh(self, var, thresh):
        self.split_var = var
        self.split_thresh = thresh

    def set_children(self, c1, c2):
        self.c1 = c1
        self.c2 = c2
        # no longer need to keep track of data
        del self.data
    
    def set_terminal(self):
        # this node has no children.
        self.is_terminal = True
        # thus, it must choose a label based on the majority of its data.

        # count number of failed & success in this group.
        num_fail, num_succ = 0, 0
        for row in self.data:
            if row[-1] == "successful":
                num_succ += 1
            else:
                num_fail += 1
        # proclaim a decision based on majority.
        if num_succ > num_fail:
            self.decision = "successful"
        else:
            self.decision = "failed"

    def get_decision(self, example):
        # given one row, follow the tree to a decision recursively
        if self.is_terminal:
            return self.decision
        else:
            # evaluate the example row and check the relevant child node
            if example[self.split_var] < self.split_thresh:
                return self.c1.get_decision(example)
            else:
                return self.c2.get_decision(example)