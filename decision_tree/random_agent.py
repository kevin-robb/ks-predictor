# this program will present an example row to the user, 
# prompt a guess, and record accuracy.

import dt_util
import sys
import random

# prompt the user for which testing set to use
data_options = ["full_cat", "seg_cat", "full", "seg", "big_cat"]
if len(sys.argv) < 2 or str(sys.argv[1]) not in data_options:
    print("Expecting argument in ", data_options)
    exit()
suffix = str(sys.argv[1])

# get the testing data and print the header
df_test = dt_util.init_dt_data(str(suffix))[2]
#print("\nVariables are ", dt_util.header[0:-1])

# store labels and predictions
y, p = [], []

for i in range(len(df_test)):
    # generate prediction at random
    guess = random.randint(0,1)
    # add it and the label to their lists
    y.append(int(df_test[i][-1]))
    p.append(guess)

# check the accuracy and give the number of items tested
print("Accuracy is " + str(dt_util.accuracy(y,p)))
print("over " + str(len(p)) + " predictions.")

