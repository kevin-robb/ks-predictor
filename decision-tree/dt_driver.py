# Program to run which actually creates objects and does things
from dtnode import Node
from dtnode_storage import NodeStorage
from decision_tree import DecisionTree
import dt_util
import sys

## main -------
# specify necessary arguments passed from command line
print("Expecting suffix argument: full_cat, seg_cat, full, or seg.")
suffix = str(sys.argv[1])
# set tree name and get data
df_train, df_val, df_test = dt_util.init_dt_data(suffix)

# initialize the tree with the training data.
# now that we have finalized the tree, train with both training & validation data
tree = DecisionTree(data=df_train+df_val, max_depth=5, min_node_size=50)
print("tree initialization finished")
root_node = tree.split(node=tree.root_node)
print("tree split finished")

# display and store the tree
dtns = NodeStorage(root_node=root_node, fname=dt_util.get_filename(suffix), header=dt_util.header)
print("dtns initialization finished")
print("\nPrinting tree preorder")
dtns.print_tree_preorder(node=root_node)
#print("Printing tree inorder")
#dtns.print_tree_inorder(node=root_node)
print("\nComputing the accuracy")
test_labels = dt_util.get_labels(df_test)
test_pred = tree.predict_list(examples=df_test,root_node=root_node)
acc = dt_util.accuracy(test_labels,test_pred)
print("Accuracy is " + str(acc) + "\n")
print("attempting to write to file")
dtns.tree_to_file_readable(root_node=root_node, acc=acc)
print("finished writing tree to file")


