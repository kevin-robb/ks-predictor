# This program will execute the optimal comparison, scikit-learn's 
# implementation of logistic regression, on our same datasets.
# This will give us an idea about what kind of accuracy might be possible.

from sklearn.linear_model import LogisticRegression as lr
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from csv import reader
from typing import List, Tuple
import numpy as np

## Read in and store the data
header = None
def get_data(filename:str) -> Tuple[List,List[int]]:
    global header
    filepath = "logistic-regression/data/" + filename + ".csv"
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
    return np.array(X).astype(np.float64), np.array(Y).astype(np.float64)

# main ------
X_train, Y_train = get_data("ks_train")
X_val, Y_val = get_data("ks_validate")
X_test, Y_test = get_data("ks_test")

# define the classifier w/ our training data
# do a grid search to find best model
clf = lr(random_state=5, C= .001)
#param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000] }
#search = GridSearchCV(clf, param_grid, cv=5)
clf = clf.fit(X_train, Y_train)

#best = clf.best_estimator_
best = clf

# use the model for probabilistic prediction
Y_pred_train = best.predict(X_train)
Y_pred_val = best.predict(X_val)

# Returns number of accurate predictions
accuracy_train = accuracy_score(Y_train, Y_pred_train)
accuracy_val = accuracy_score(Y_val, Y_pred_val)

print("Training Accuracy: " + str(accuracy_train))
print("Validation Accuracy: " + str(accuracy_val))

# # create a new dataset of both the training and validation data
X_tv = np.concatenate( (X_train, X_val))
Y_tv  = np.concatenate((Y_train, Y_val))

# define the classifier
clf = clf.fit(X_tv, Y_tv)

# probabilistic prediction
Y_test = clf.predict(X_tv)

accuracy_test = accuracy_score(Y_tv, Y_test)

print("Testing Accuracy: " + str(accuracy_test))
