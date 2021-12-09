from collections import defaultdict
import re
import math
import numpy as np
from numpy.core.fromnumeric import sort
from matplotlib import pyplot as plt
from matplotlib import colors


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
        return

    # set node (this is my method of keeping track)
    hMap[i,j] = marker
    
    # flood_fill neighbours
    if i+1 < len(hMap):
        flood_fill(i+1, j, hMap, marker)
    if i-1 >= 0:
        flood_fill(i-1, j, hMap, marker)
    if j+1 < len(hMap[0]):
        flood_fill(i, j+1, hMap, marker)
    if j-1 >= 0:
        flood_fill(i, j-1, hMap, marker)
    return


# if coord not in basin already or not on max(9) then fill basin
for i in range(len(hMap)):
    for j in range(len(hMap[0])):
        if hMap[i,j] < 9:
            flood_fill(i, j, hMap, np.max(hMap) + 1)

# get sorted list of basin sizes
basinSizes = sorted([np.count_nonzero(hMap == h) for h in range(10, np.max(hMap) + 1)])
print(basinSizes[-1] * basinSizes[-2] * basinSizes[-3])

# plot with random colors
colorSet = np.random.rand(len(basinSizes), 3)
colorSet[0] = [0, 0, 0]
cmap = colors.ListedColormap(colorSet)
plt.imshow(hMap, interpolation='nearest', cmap=cmap)
plt.show()

