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
        if y[i] == p[i]:
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

def get_filename(suffix:str):
    # Generate a unique filename to save the tree (based on datetime).
    # this is mainly for testing so files don't get overwritten.
    dt = datetime.now()
    fname = "ks_" + suffix
    fname += dt.strftime("%Y-%m-%d-%H-%M")
    print("Tree will be stored as " + fname + ".txt")
    return fname

def init_dt_data(fname_suffix:str=""):
    # make it less annoying to change which set of files we are using.
    df_train = get_data("ks_train"+fname_suffix)
    df_val = get_data("ks_validate"+fname_suffix)
    df_test = get_data("ks_test"+fname_suffix)
    return df_train, df_val, df_test

def get_labels(df:List) -> List[int]:
    # get the labels (last column) of dataframe df as a list
    lab = []
    for line in df:
        lab.append(int(line[-1]))
    return lab

## main -------
# set tree name and get data
run_seg = True
run_cats = True
suffix = "" + "_seg" if run_seg else "_full"
suffix += "_cat" if run_cats else ""
df_train, df_val, df_test = init_dt_data(suffix)

# initialize the tree with the training data.
# now that we have finalized the tree, train with both training & validation data
tree = DecisionTree(data=df_train+df_val, max_depth=5, min_node_size=50)
print("tree initialization finished")
root_node = tree.split(node=tree.root_node)
print("tree split finished")

# display and store the tree
dtns = NodeStorage(root_node=root_node, fname=get_filename(suffix), header=header)
print("dtns initialization finished")
print("\nPrinting tree preorder")
dtns.print_tree_preorder(node=root_node)
#print("Printing tree inorder")
#dtns.print_tree_inorder(node=root_node)
print("\nComputing the accuracy")
test_labels = get_labels(df_test)
test_pred = tree.predict_list(examples=df_test,root_node=root_node)
acc = accuracy(test_labels,test_pred)
print("Accuracy is " + str(acc) + "\n")
print("attempting to write to file")
dtns.tree_to_file_readable(root_node=root_node, acc=acc)
print("finished writing tree to file")


