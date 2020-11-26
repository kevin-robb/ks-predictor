# Program to run which actually creates objects and does things
from dtnode import Node
from dtnode_storage import NodeStorage
from decision_tree import DecisionTree
from csv import reader
from typing import List, Tuple

def accuracy(y, p):
    # y[i] is list of real labels.
    # p[i][1] is the probability of predicting 1.
    num_correct = 0
    num_labels = len(y)
    # we will say the model's guess is the choice with higher probability.
    for i in range(num_labels):
        #print("Values are y[i]=" + str(y[i]) + " and p[i][1]=" + str(p[i][1]))
        if float(y[i]) == round(p[i][1]):
            num_correct += 1
    return float(num_correct)/float(num_labels)


## Read in and store the data
header = None
def get_data(filename:str) -> List:
    global header
    filepath = "data/" + filename + ".csv"
    with open(filepath, 'r') as read_obj:
        df = list(reader(read_obj)) # list of lists
    # save and remove the header
    header = df[0]
    del df[0]

    for line in df:
        # remove the first var (the useless index)
        del line[0]
    # reflect the var removal in the header
    del header[0]
    return df

## main -------
df_train = get_data("ks_train")
df_val = get_data("ks_validate")
df_test = get_data("ks_test")

# initialize the tree with the training data
tree = DecisionTree(data=df_train)
root_node = tree.split(node=tree.root_node, max_depth=5, min_node_size=100)

# display and store the tree
dtns = NodeStorage(root_node=root_node, fname="ks_train")
dtns.print_tree_preorder(node=root_node)


