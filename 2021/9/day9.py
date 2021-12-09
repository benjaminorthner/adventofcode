from collections import defaultdict
import re
import math
import numpy as np
from numpy.core.fromnumeric import sort

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

hMap = np.zeros(shape=(len(lines), len(lines[0])), dtype=int)

for i,line in enumerate(lines):
    for j,c in enumerate(line):
        hMap[i,j] = int(c)

totalRiskLevel = 0

for i in range(len(hMap)):
    for j in range(len(hMap[0])):

        currentHeight = hMap[i, j]
        isLowPoint = True
        for ii in range(-1 , 2):
            for jj in range(-1, 2):
                if (0 <= i+ii < len(hMap)) and (0 <= j+jj < len(hMap[0])):
                    neighbour = hMap[i+ii, j+jj]
                    if (neighbour <= currentHeight) and (np.abs(ii) != np.abs(jj)):
                        isLowPoint = False


        
        if isLowPoint:
            totalRiskLevel += 1 + currentHeight

print(totalRiskLevel)


# PART 2

def flood_fill(i, j, hMap, marker):
    currentHeight = hMap[i,j]
    # return if not inside
    if currentHeight >= 9:
        return hMap

    # set node (this is my method of keeping track)
    hMap[i,j] = marker
    
    
    # flood_fill neighbours
    if i+1 < len(hMap):
        hMap = flood_fill(i+1, j, hMap, marker)
    if i-1 >= 0:
        hMap = flood_fill(i-1, j, hMap, marker)
    if j+1 < len(hMap[0]):
        hMap = flood_fill(i, j+1, hMap, marker)
    if j-1 >= 0:
        hMap = flood_fill(i, j-1, hMap, marker)

    return hMap


for i in range(len(hMap)):
    for j in range(len(hMap[0])):

        currentHeight = hMap[i,j]
        if currentHeight < 9:
            hMap = flood_fill(i, j, hMap, np.max(hMap) + 1)

basinSizes = []
for h in range(10, np.max(hMap)+1):
    basinSizes.append(np.count_nonzero(hMap == h))

basinSizes = sorted(basinSizes)
print(basinSizes[-1] * basinSizes[-2] * basinSizes[-3])