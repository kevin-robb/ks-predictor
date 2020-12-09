# helper functions used by drivers
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
    fname = "ks_" + suffix + "_"
    fname += dt.strftime("%Y-%m-%d-%H-%M")
    print("Tree will be stored as " + fname + ".txt")
    return fname

def init_dt_data(fname_suffix:str=""):
    # make it less annoying to change which set of files we are using.
    df_train = get_data("ks_train_"+fname_suffix)
    df_val = get_data("ks_validate_"+fname_suffix)
    df_test = get_data("ks_test_"+fname_suffix)
    return df_train, df_val, df_test

def get_labels(df:List) -> List[int]:
    # get the labels (last column) of dataframe df as a list
    lab = []
    for line in df:
        lab.append(int(line[-1]))
    return lab

def get_header():
    global header
    if header is None:
        header = ["goal","usd_goal_real","title_length","title_punc","title_caps_ratio","currency_is_usd","country_is_us","launched_epoch","open_epoch","Art","Comics","Crafts","Dance","Design","Fashion","Film & Video","Food","Games","Journalism","Music","Photography","Publishing","Technology","Theater","target"]
    return header

# Variable types, corresponding to header var_indexes. 1=numeric, 2=boolean
var_types = [1,1,1,1,1,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
