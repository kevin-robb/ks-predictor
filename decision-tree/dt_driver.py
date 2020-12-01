# Program to run which actually creates objects and does things
from dtnode import Node
from dtnode_storage import NodeStorage
from decision_tree import DecisionTree
from csv import reader
from typing import List, Tuple
from datetime import datetime

def accuracy(y, p):
    # Calculate the accuracy given the true labels and probabilistic predictions.
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

header = None
def get_data(filename:str) -> List:
    # Read in and store the data
    global header
    filepath = "data/" + filename + ".csv"
    with open(filepath, 'r') as read_obj:
        df = list(reader(read_obj)) # list of lists
    # save and remove the header
    header = df[0]
    del df[0]
    # remove the first var (useless index) from each line.
    # (can't be done in preproc bc it's the R index.)
    for line in df:
        del line[0]
    # reflect the var removal in the header
    del header[0]
    return df

def get_filename(run_full:bool):
    # Generate a unique filename to save the tree (based on datetime).
    # this is mainly for testing so files don't get overwritten.
    dt = datetime.now()
    fname = "ks_"
    if run_full:
        fname += "full_"
    else:
        fname += "seg_"
    fname += dt.strftime("%Y-%m-%d-%H-%M")
    print("Tree will be stored as " + fname + ".txt")
    return fname

def init_dt_data(fname_suffix:str=""):
    # make it less annoying to change which set of files we are using.
    df_train = get_data("ks_train"+fname_suffix)
    df_val = get_data("ks_validate"+fname_suffix)
    df_test = get_data("ks_test"+fname_suffix)
    return df_train, df_val, df_test

## main -------
run_full = False
# if run_full:
#     # run with full dataset (very slow)
#     df_train, df_val, df_tests = init_dt_data("_full")
# else:
#     # run with segmented dataset (faster)
#     df_train, df_val, df_tests = init_dt_data("_seg")
df_train, df_val, df_tests = init_dt_data("_full") if run_full else init_dt_data("_seg")

# initialize the tree with the training data
tree = DecisionTree(data=df_train, max_depth=5, min_node_size=50)
print("tree initialization finished")
root_node = tree.split(node=tree.root_node)
print("tree split finished")

# display and store the tree
dtns = NodeStorage(root_node=root_node, fname=get_filename(run_full), header=header)
print("dtns initialization finished")
print("Printing tree preorder")
dtns.print_tree_preorder(node=root_node)
#print("Printing tree inorder")
#dtns.print_tree_inorder(node=root_node)
print("attempting to write to file")
dtns.tree_to_file_readable(root_node=root_node)
print("finished writing tree to file")


