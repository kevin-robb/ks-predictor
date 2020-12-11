# This program will execute the optimal comparison, scikit-learn's 
# implementation of the decision tree, on our same datasets.
# This will give us an idea about which variables are probably most 
# important, and what kind of accuracy might be possible.

# As a side note, I am referencing my code for homework 4.


from numpy.lib.function_base import gradient
from sklearn.metrics import accuracy_score
from csv import reader
from math import log, exp
from typing import List, Tuple
import numpy as np

e = 2.718281


## Read in and store the data
## Characterisitics of our dataframe, df
# - row 0 is the header
header = None
# - column 0 is a useless index
# - columns 1-9 are data
# - final column (10) is the target
def get_data(filename:str) -> Tuple[List,List[int]]:
    global header
    filepath = "decision-tree/data/" + filename + ".csv"
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

class log_reg:
    def __init__(self, n_weights, learning_rate):
        self.weights = [0]*n_weights
        self.learning_rate = learning_rate

    def fit(self,X,Y):
        previous_weights = self.weights
        stopping_con = False
        i = 0
        m= len(X)
        while not stopping_con:
            # compute gradient
            z = 0
            grad = 0
            for xi in X:
                yi = Y[z]
                yxi = np.dot(yi,xi)
                wxi = np.dot((self.weights),xi)
                wyxi = np.dot(yi,wxi)
                if(-1*wyxi > 30):
                    grad += .999999
                elif(-1*wyxi < -30):
                    grad -= .00000009
                else:
                    grad += yxi/(1+exp(wyxi))
                z+=1

            grad /= m
            grad *=-1

            #update weights
            self.weights = self.weights - self.learning_rate*grad

            if(np.linalg.norm(self.weights - previous_weights) < .00001):
                stopping_con = True 
            elif (i > 1000):
                print("We reached max iterations")
                stopping_con = True 
            i+=1
            previous_weights = self.weights

    def predict(self,X):
        Y = [0]*len(X)
        i=0
        for x in X:
            s = sum(self.weights*x)
            sigma = 1/(1+np.exp(-1*s))
            #print(round(sigma))
            Y[i] = round(sigma)
            i+=i
        return Y

# main ------
X_train, Y_train = get_data("ks_train_full_cat")
X_val, Y_val = get_data("ks_validate_full_cat")
X_test, Y_test = get_data("ks_test_full_cat")

lr = log_reg(24,.01)

lr.fit(X_train, Y_train)

Y_pred_train = lr.predict(X_train)
Y_pred_val = lr.predict(X_val)
accuracy_train = accuracy_score(Y_train, Y_pred_train)
accuracy_val = accuracy_score(Y_val, Y_pred_val)

print("Training Accuracy: " + str(accuracy_train))
print("Validation Accuracy: " + str(accuracy_val))

X_tv = np.concatenate( (X_train, X_val))
Y_tv  = np.concatenate((Y_train, Y_val))

# define the classifier
lr.fit(X_tv, Y_tv)

# probabilistic prediction
Y_test = lr.predict(X_tv)

accuracy_test = accuracy_score(Y_tv, Y_test)

print("Testing Accuracy: " + str(accuracy_test))
