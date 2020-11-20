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
    for group in partition:
        group_size = len(group)
        # prevent div by 0 error
        if group_size == 0:
            continue
        # count number of failed & success in this group
        num_fail, num_succ = 0, 0
        for row in group:
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
    c1, c2 = [], []
    # check whether specified var is numeric or categorical
    if types[var_to_split] == "numeric":
        # numeric variable. simple to partition
        for row in parent:
            if row[var_to_split] < threshold:
                c1.append(row)
            else:
                c2.append(row)
        return c1, c2
    else:
        # categorical variable
        pass #TODO
	



# define node class to make tree structure simpler
class Node:
    data = None
    c1 = None
    c2 = None
    depth = None
    split_var = None
    split_thresh = None

    def __init__(self, data, depth):
        self.data = data
        self.c1 = None
        self.c2 = None
        self.depth = depth
        self.split_var = None
        self.split_thresh = None
    
    def set_thresh(self, var, thresh):
        self.split_var = var
        self.split_thresh = thresh

    def define_children(self, c1, c2):
        self.c1 = c1
        self.c2 = c2
        # no longer need to keep track of data
        del(self.data)