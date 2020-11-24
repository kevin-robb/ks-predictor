# define node class to make tree structure simpler
class Node:
    def __init__(self, data=None, depth=1, c1=None, c2=None, split_var=None, split_thresh=None, is_terminal=False):
        self.data = data
        self.c1 = c1
        self.c2 = c2
        self.depth = depth
        self.split_var = split_var
        self.split_thresh = split_thresh
        self.is_terminal = is_terminal
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