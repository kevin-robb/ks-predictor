# Program to run which actually creates objects and does things
from dtnode import Node
from dtnode_storage import NodeStorage
from decision_tree import DecisionTree
import dt_util
import sys

def write_file(suffix:str,recoverable:bool=True, readable:bool=False):
    # set tree name and get data
    df_train, df_val, df_test = dt_util.init_dt_data(suffix)
    # make the tree
    tree = DecisionTree(data=df_train+df_val, max_depth=5, min_node_size=50, var_types=dt_util.var_types)
    root_node = tree.split(node=tree.root_node)
    # display tree to console
    dtns = NodeStorage(root_node=root_node, fname=dt_util.get_filename(suffix), header=dt_util.header, var_types=dt_util.var_types)
    dtns.print_tree_preorder(node=root_node)
    if recoverable:
        # write tree to file (recoverable)
        dtns.tree_to_file(root_node=root_node)
    if readable:
        # write tree to file (readable)
        test_pred = tree.predict_list(examples=df_test,root_node=root_node)
        acc = dt_util.accuracy(dt_util.get_labels(df_test),test_pred)
        dtns.tree_to_file_readable(root_node=root_node, acc=acc)
    

def read_file(fname:str) -> Node:
    # read recoverable file and return the root node
    dtns = NodeStorage(fname=fname,header=dt_util.get_header(), var_types=dt_util.var_types)
    root_node = dtns.file_to_tree()
    # print tree to console to see if it worked
    dtns.print_tree_preorder(root_node)
    return root_node

## main -------
# specify necessary arguments passed from command line
print("First argument: read or write")
print("If write: Second argument: full_cat, seg_cat, full, or seg.")
print("If read: Second argument: filename.")
mode = str(sys.argv[1])
if mode == "write":
    write_file(suffix=str(sys.argv[2]), recoverable=True, readable=True)
elif mode == "read":
    root_node = read_file(fname=str(sys.argv[2]))




