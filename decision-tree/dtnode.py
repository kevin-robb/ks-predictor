
from typing import List, Tuple
# allow us to type hint c1 and c2 as Node
#from __future__ import annotations #only works in python 3.7 and up
# define node class to make tree structure simpler
class Node:
    node_id=None #unique id to make debugging easier
    data = None
    c1, c2 = None, None
    depth = None
    split_var, split_thresh = None, None
    is_terminal = False
    decision = None
    purity = None

    def __init__(self, node_id:int=-1, data:List=None, depth:int=1, c1:'Node'=None, c2:'Node'=None, split_var:int=None, split_thresh:float=None):
        self.node_id=node_id
        self.data = data
        self.c1 = c1
        self.c2 = c2
        self.depth = depth
        self.split_var = split_var
        self.split_thresh = split_thresh
        # check the size and set terminal if too small
        # if len(self.data) < self.min_node_size:
        #     self.set_terminal()
        # compute the purity
        self.purity = self.compute_purity()

    def compute_purity(self):
        if len(self.data) <= 1:
            return 0
        # count number of success in this group.
        num_succ = 0
        for row in self.data:
            if int(row[-1]) == 1:
                num_succ += 1
        # set the purity
        purity = float(num_succ) / float(len(self.data))
        # could be purely success or failure
        if purity > 0.5:
            purity = 1 - purity
        return purity
    
    def set_thresh(self, var:int, thresh:float):
        self.split_var = var
        self.split_thresh = thresh

    def set_children(self, c1:'Node', c2:'Node'):
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
            if int(row[-1]) == 1:
                num_succ += 1
            else:
                num_fail += 1
        # make the decision based on majority.
        if num_succ > num_fail:
            self.decision = 1
        else:
            self.decision = 0

    def get_decision(self, example:List[float]) -> int:
        # given one row, follow the tree to a decision recursively
        if self.is_terminal:
            return self.decision
        else:
            # evaluate the example row and check the relevant child node
            if example[self.split_var] <= self.split_thresh:
                return self.c1.get_decision(example)
            else:
                return self.c2.get_decision(example)