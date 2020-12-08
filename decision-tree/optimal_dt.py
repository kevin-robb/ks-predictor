# This program will execute the optimal comparison, scikit-learn's 
# implementation of the decision tree, on our same datasets.
# This will give us an idea about which variables are probably most 
# important, and what kind of accuracy might be possible.

# As a side note, I am referencing my code for homework 4.

from sklearn import tree
from csv import reader
from math import log
from typing import List, Tuple
import sys

### Define functions to use later
## Calculate the cross-entropy of predictions and true labels.
def cross_entropy(y:List[int], p:List) -> float:
    # y[i] is list of real labels.
    # p[i][1] is the probability of predicting 1.
    m = len(y)
    sum_vals = 0
    for i in range(m):
        #print("Values are y[i]=" + str(y[i]) + " and p[i][1]=" + str(p[i][1]))
        sum_vals += float(y[i]) * float(log(p[i][1])) + (1 - float(y[i])) * float(log(p[i][1]))
    R = -1/m * sum_vals
    return R

def accuracy(y:List[int], p:List) -> float:
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
## Characterisitics of our dataframe, df
# - row 0 is the header
header = None
# - column 0 is a useless index
# - columns 1-9 are data
# - final column (10) is the target
def get_data(filename:str) -> Tuple[List,List[int]]:
    global header
    filepath = "data/" + filename + ".csv"
    with open(filepath, 'r') as read_obj:
        # pass the file object to reader() to get a reader object, and
        # pass the reader object to list() to get a list of lists.
        df = list(reader(read_obj))
    # save and remove the header
    header = df[0]
    del df[0]

    # define X (training samples) and Y (labels)
    X = df
    Y = []
    for line in X:
        # add the target to Y
        Y.append(line[len(line)-1])
        # remove the target from X_train
        del line[len(line)-1]
        # remove the first var as well (the useless index)
        del line[0]
    # reflect the var removal in the header
    del header[0]
    return X, Y

## Store the decision tree graphically for later reference.
# assumes tree has already been exported to string using
# t = tree.export_text(clf,feature_names=header[0:len(header)-1])
def write_tree_to_file(tree:str, acc:float, fname:str=""):
    # w=write, a=append
    file1=open("trees/optimal_dt_"+fname+".txt","w")
    file1.write(tree + "\nThe Accuracy is " + str(acc) + "\n")
    file1.close()
    print(tree)
    print("The Accuracy is " + str(acc))


# main ------
# we should be getting the filename as an argument with the function call
print("Expecting argument in format full_cat, seg_cat, full, or seg.")
fname = str(sys.argv[1])
X_train, Y_train = get_data("ks_train_" + fname)
X_val, Y_val = get_data("ks_validate_" + fname)
X_test, Y_test = get_data("ks_test_" + fname)

# define the classifier w/ our training data
clf = tree.DecisionTreeClassifier(criterion="gini", max_depth=5)
clf = clf.fit(X_train, Y_train)

# use the model for probabilistic prediction
Y_pred = clf.predict_proba(X_val)

#print("The Cross Entropy is " + str(cross_entropy(Y_val, Y_pred)))
print("The Accuracy is " + str(accuracy(Y_val, Y_pred)))

# create a new dataset of both the training and validation data
X_tv = X_train + X_val
Y_tv = Y_train + Y_val

# define the classifier
clf = tree.DecisionTreeClassifier(criterion="gini", max_depth=5)
clf = clf.fit(X_tv, Y_tv)
# export the tree as text
t = tree.export_text(clf,feature_names=header[0:len(header)-1])
# probabilistic prediction
Y_pred = clf.predict_proba(X_test)
# calculate the cross-entropy
#print("The Cross Entropy is " + str(cross_entropy(Y_test, Y_pred)))
# calculate the accuracy
acc = accuracy(Y_test, Y_pred)
# write the tree + acc to a file, & print to console
write_tree_to_file(t, acc, fname)
