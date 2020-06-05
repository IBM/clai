import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
import os
import time

# Start timer
start_time = time.time()

# Read bash history as list of lists
homedir = os.path.expanduser('~')
# Open bash_history file
bash_history = open(homedir+"/.bash_history",'r')
# Read contents of bash history
bash_text = bash_history.read()
# Put text into list for apyori
bash_list = [line for line in bash_text.splitlines()]
# Create a list of tuples
bash_tuple = zip(bash_list,bash_list[1:])

# Will iterate over list of tuples and place subsequent commands in a sublist to the current command
# t is the tuple being passed in, takes form of [(1,2),(2,3),(3,4),...] to compare subsequent values
def create_associations(tup):
    # Local variables
    l = []
    valFound = -1
    index = -1
    newC1 = ''
    for c1, c2 in tup:
        newC1 = stemming(c1)
        # Check whether c1 already exists
        valFound,index = in_list(newC1,l)
        if valFound:
            # True, append that sublist to include the form [newC1,...,c2]
            l[index].append(c2)
        else:
            # False, create new list of form [newC1,c2]
            l.append([newC1,c2])
    return l

# Checks whether value is already present inside list as key
# c is the value to search for, l is the list
def in_list(c, l):
    compare_list = extract(l)
    return [1,compare_list.index(c)] if c in compare_list else [0,0]

# Returns the first item in each sublist
def extract(l):
    return [item[0] for item in l]

# In cases like 'cd ', we don't care what comes after it
# Shorten these commands to what's essential
def stemming(c1):
    newC1 = ''
    if c1[:3] == 'cd ':
        newC1 = 'cd '
    else:
        newC1 = c1
    # Can add to this list if neccesary
    return newC1

# Convert list to dataframe for Apyori
def to_dataframe(ls):
    return pd.DataFrame(ls)

# Create NxM list that includes all 'None' values
def to_list(df):
    return df.values.tolist()

def main():
    associationList = create_associations(bash_tuple)
    df = to_dataframe(associationList)

    print(df)

#    records = to_list(df)
#    rules = list(apriori(records))
#    for rule in rules:
#        print(rule,"\n")

    """ # T E S T
    transactions = [
            ['beer','nuts'],
            ['beer','cheese'],
            ]
    rules = list(apriori(transactions))
    print("len(rules)")
    print(len(rules))

    print("\nrules")
    for rule in rules:
        print(rule,"\n")
    
    print("\nlen(rules[0])")
    print(len(rules[0]))
    
    print("\nrules[0]")
    print(rules[0])
    """

    """ I N S T R U C T I O N S

    min_support: /.bash_history keeps up to 500 lines, so if a certain command
    is used at least 5x or 0.01% of the time, I want to include it

    min_confidence: I want command B to follow command A at least 50% of the time
    to imply correlation

    min_lift: I want there to be a 5x ratio that command B will follow command A

    min_len: At least 2 commands in the rules
    """

    # Run Apyori library then convert to list for easier viewing
#    association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_len=2)
#    association_results = list(association_rules)

    #print(len(association_rules))
    #print(association_results[0])

    print("--- %.2f seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()


