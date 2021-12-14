from collections import defaultdict, deque
import re
from copy import deepcopy
import math
import numpy as np
from numpy.core.fromnumeric import sort
from matplotlib import pyplot as plt
from matplotlib import colors

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

# READ DATA
polymer = lines[0]

rules = {}
for line in lines[2:]:
    pair, insert = line.split(" -> ")
    rules[pair] = insert

# FUNCTIONS
def tostring(l):
    s = ''
    for i in l:
        s += i
    return s

def insert(pairs, occurances):
    newpairs = deepcopy(pairs)

    # for every pair
    for pair in pairs.keys():
        # if it has an insertion rule
        if pair in rules.keys():
            # perform insertions by creating two new pairs and removing all the current ones
            ins = rules[pair]
            newpairs[pair] -= pairs[pair]
            newpairs[tostring([ins, pair[1]])] += pairs[pair]
            newpairs[tostring([pair[0], ins])] += pairs[pair]
            # count how many of a particular letter was added
            occurances[ins] += pairs[pair]
        
    return newpairs, occurances

# PART1 AND PART2

# init list of pairs
pairs = defaultdict(lambda: 0)
for pair in zip(lines[0], lines[0][1:]):
    pairs[tostring(pair)] += 1

# init list of letter counts/occurances
occurances = defaultdict(lambda: 0)
for letter in lines[0]:
    occurances[letter] += 1

# perform 10 and 40 insertions
for i in range(40):
    pairs, occurances = insert(pairs, occurances)
    
    if i == 10-1 or i == 40-1: 
        print(max(occurances.values()) - min(occurances.values()))