import re
import numpy as np
import math

def getID(line):
    row = [0, 127]
    col = [0, 7]

    for i,com in enumerate(line):
        if com == "F":
            row = [row[0], math.floor(np.mean(row))]
        if com == "B":
            row = [math.ceil(np.mean(row)), row[1]]
        
        if com == "L":
            col = [col[0], math.floor(np.mean(col))]
        if com == "R":
            col = [math.ceil(np.mean(col)), col[1]]

    return 8*row[1] + col[1]


with open("input.dat", "r") as file:
    lines = [line for line in file.readlines()]

maxid = 0
for line in lines:

    if getID(line) > maxid:
        maxid = getID(line)

print(maxid)


# PART 2

def getSeat(line):
    row = [0, 127]
    col = [0, 7]

    for i,com in enumerate(line):
        if com == "F":
            row = [row[0], math.floor(np.mean(row))]
        if com == "B":
            row = [math.ceil(np.mean(row)), row[1]]
        
        if com == "L":
            col = [col[0], math.floor(np.mean(col))]
        if com == "R":
            col = [math.ceil(np.mean(col)), col[1]]

    return row[1],col[1]


filled = np.empty(shape=(128,8))
filled.fill(False)

for line in lines:
    row, col = getSeat(line)
    filled[row, col] = True

for row in range(1,127):
    for col in range(8):

        if filled[row,col] == False:
            if filled[row+1,col] and filled[row-1,col]:
                print(8*row + col)
